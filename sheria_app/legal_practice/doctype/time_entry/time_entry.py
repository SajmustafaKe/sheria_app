# Time Entry DocType
# Copyright (c) 2024, Sheria Legal Technologies
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import time_diff_in_hours, get_datetime, flt


class TimeEntry(Document):
	def validate(self):
		self.validate_times()
		self.calculate_hours()
		self.calculate_billing_amount()
		self.set_employee_name()
		self.set_case_title()

	def validate_times(self):
		"""Validate start and end times"""
		if self.start_time and self.end_time:
			if self.start_time >= self.end_time:
				frappe.throw(_("End Time must be after Start Time"))

	def calculate_hours(self):
		"""Calculate hours from start and end time"""
		if self.start_time and self.end_time:
			start_datetime = get_datetime(f"{self.date} {self.start_time}")
			end_datetime = get_datetime(f"{self.date} {self.end_time}")
			self.hours = flt(time_diff_in_hours(end_datetime, start_datetime))
		elif self.hours and self.hours <= 0:
			frappe.throw(_("Hours must be greater than 0"))

	def calculate_billing_amount(self):
		"""Calculate billing amount based on hours and rate"""
		if self.hours and self.billing_rate and self.is_billable:
			self.billing_amount = flt(self.hours * self.billing_rate)
		else:
			self.billing_amount = 0

	def set_employee_name(self):
		"""Set employee name from Employee doctype"""
		if self.employee:
			self.employee_name = frappe.db.get_value("Employee", self.employee, "employee_name")

	def set_case_title(self):
		"""Set case title from Legal Case doctype"""
		if self.case:
			self.case_title = frappe.db.get_value("Legal Case", self.case, "case_details_title")

	def on_submit(self):
		"""Actions when time entry is submitted"""
		self.status = "Submitted"
		self.notify_approver()

	def on_cancel(self):
		"""Actions when time entry is cancelled"""
		if self.billed:
			frappe.throw(_("Cannot cancel a billed Time Entry"))

	def notify_approver(self):
		"""Send notification to approver"""
		if self.employee:
			# Find the employee's supervisor or managing partner
			employee = frappe.get_doc("Employee", self.employee)
			approver = employee.reports_to or frappe.db.get_single_value("Legal Settings", "default_time_approver")

			if approver:
				frappe.sendmail(
					recipients=[approver],
					subject=_("Time Entry Approval Required"),
					template="time_entry_approval",
					args={
						"employee": self.employee_name,
						"activity": self.activity_type,
						"hours": self.hours,
						"date": self.date,
						"time_entry": self.name
					}
				)


@frappe.whitelist()
def approve_time_entry(time_entry, approved=1):
	"""Approve or reject time entry"""
	if not frappe.has_permission("Time Entry", "write"):
		frappe.throw(_("Not permitted"))

	doc = frappe.get_doc("Time Entry", time_entry)
	doc.status = "Approved" if approved else "Rejected"
	doc.approved_by = frappe.session.user
	doc.approved_date = frappe.utils.now()
	doc.save()

	return {"status": "success", "message": _("Time Entry {0}").format("approved" if approved else "rejected")}


@frappe.whitelist()
def get_employee_billing_rate(employee, case=None):
	"""Get billing rate for employee, optionally based on case"""
	if not employee:
		return 0

	# First check if there's a case-specific rate
	if case:
		case_doc = frappe.get_doc("Legal Case", case)
		if case_doc.lawyer_table:
			for lawyer in case_doc.lawyer_table:
				if lawyer.lawyer == employee:
					return flt(lawyer.rate or 0)

	# Get default employee billing rate
	employee_doc = frappe.get_doc("Employee", employee)
	return flt(employee_doc.billing_rate or 0)


@frappe.whitelist()
def get_time_entries_for_case(case, start_date=None, end_date=None):
	"""Get time entries for a specific case within date range"""
	filters = {"case": case, "docstatus": 1}

	if start_date:
		filters["date"] >= start_date
	if end_date:
		filters["date"] <= end_date

	entries = frappe.get_all("Time Entry",
		filters=filters,
		fields=["name", "date", "activity_type", "hours", "billing_amount", "employee_name", "status"],
		order_by="date desc"
	)

	return entries