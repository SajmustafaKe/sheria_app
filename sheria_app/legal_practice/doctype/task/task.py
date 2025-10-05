# Task DocType
# Copyright (c) 2024, Sheria Legal Technologies
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import nowdate


class Task(Document):
	def validate(self):
		self.set_case_title()
		self.validate_dates()
		self.update_progress_on_status_change()
		self.calculate_actual_hours()

	def set_case_title(self):
		"""Set case title from Legal Case doctype"""
		if self.case:
			self.case_title = frappe.db.get_value("Legal Case", self.case, "case_details_title")

	def validate_dates(self):
		"""Validate due date is not in the past for new tasks"""
		if self.due_date and self.due_date < nowdate() and self.is_new():
			frappe.msgprint(_("Due date is in the past. Consider updating the due date."), alert=True)

	def update_progress_on_status_change(self):
		"""Update progress based on status change"""
		if self.status == "Completed" and not self.completed_date:
			self.completed_date = nowdate()
			self.progress = 100
		elif self.status == "Open" and self.completed_date:
			self.completed_date = None
			self.progress = 0

	def calculate_actual_hours(self):
		"""Calculate actual hours from related time entries"""
		if self.name:
			actual_hours = frappe.db.sql("""
				SELECT SUM(hours) as total_hours
				FROM `tabTime Entry`
				WHERE task = %s AND docstatus = 1
			""", (self.name,))[0][0] or 0

			self.actual_hours = actual_hours

	def on_update(self):
		"""Actions on update"""
		self.notify_assigned_user()
		self.update_case_status()

	def notify_assigned_user(self):
		"""Send notification to assigned user"""
		if self.assigned_to and self.has_value_changed("assigned_to"):
			try:
				frappe.sendmail(
					recipients=[self.assigned_to],
					subject=_("New Task Assigned: {0}").format(self.subject),
					template="task_assignment",
					args={
						"task": self.subject,
						"description": self.description,
						"due_date": self.due_date,
						"assigned_by": self.assigned_by,
						"priority": self.priority
					}
				)
			except:
				# Skip email notification if template doesn't exist (for test data)
				pass

	def update_case_status(self):
		"""Update parent case status based on task completion"""
		if self.case and self.status == "Completed":
			# Check if all tasks for this case are completed
			incomplete_tasks = frappe.db.count("Task", {
				"case": self.case,
				"status": ["!=", "Completed"],
				"docstatus": 1
			})

			if incomplete_tasks == 0:
				case_doc = frappe.get_doc("Legal Case", self.case)
				case_doc.status = "Ready for Review"
				case_doc.save()

	def on_trash(self):
		"""Actions on delete"""
		# Remove task references from time entries
		frappe.db.sql("UPDATE `tabTime Entry` SET task = NULL WHERE task = %s", (self.name,))


@frappe.whitelist()
def get_tasks_for_user(user=None, status=None, priority=None):
	"""Get tasks for a specific user with optional filters"""
	if not user:
		user = frappe.session.user

	filters = {"assigned_to": user, "docstatus": 1}

	if status:
		filters["status"] = status
	if priority:
		filters["priority"] = priority

	tasks = frappe.get_all("Task",
		filters=filters,
		fields=["name", "subject", "case", "case_title", "priority", "status", "due_date", "progress"],
		order_by="due_date asc, priority desc"
	)

	return tasks


@frappe.whitelist()
def get_overdue_tasks():
	"""Get all overdue tasks"""
	tasks = frappe.db.sql("""
		SELECT name, subject, case, case_title, assigned_to, due_date, priority
		FROM `tabTask`
		WHERE due_date < %s
			AND status != 'Completed'
			AND docstatus = 1
		ORDER BY due_date asc
	""", (nowdate(),), as_dict=True)

	return tasks


@frappe.whitelist()
def update_task_progress(task, progress):
	"""Update task progress"""
	if not frappe.has_permission("Task", "write"):
		frappe.throw(_("Not permitted"))

	doc = frappe.get_doc("Task", task)
	doc.progress = progress

	if progress == 100:
		doc.status = "Completed"
		doc.completed_date = nowdate()

	doc.save()

	return {"status": "success", "message": _("Task progress updated")}


@frappe.whitelist()
def get_case_tasks(case):
	"""Get all tasks for a specific case"""
	tasks = frappe.get_all("Task",
		filters={"case": case, "docstatus": 1},
		fields=["name", "subject", "assigned_to", "status", "priority", "due_date", "progress", "actual_hours"],
		order_by="creation asc"
	)

	return tasks