# Case Hearing DocType
# Copyright (c) 2024, Sheria Legal Technologies
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import nowdate, add_days, get_datetime


class CaseHearing(Document):
	def validate(self):
		self.set_case_title()
		self.validate_hearing_date()
		self.send_reminders()

	def set_case_title(self):
		"""Set case title from Legal Case doctype"""
		if self.case:
			self.case_title = frappe.db.get_value("Legal Case", self.case, "case_details_title")

	def validate_hearing_date(self):
		"""Validate hearing date is not in the past"""
		if self.hearing_date and self.hearing_date < nowdate():
			frappe.throw(_("Hearing date cannot be in the past"))

	def send_reminders(self):
		"""Send reminders for upcoming hearings"""
		if self.hearing_date and not self.reminder_sent:
			# Send reminder 7 days before hearing
			reminder_date = add_days(self.hearing_date, -7)
			if reminder_date <= nowdate():
				self.send_hearing_reminder()
				self.reminder_sent = 1
				self.reminder_date = get_datetime()

	def send_hearing_reminder(self):
		"""Send hearing reminder to assigned lawyers"""
		if not self.case:
			return

		# Get lawyers assigned to the case
		lawyers = frappe.get_all("Lawyer Table",
			filters={"parent": self.case, "parenttype": "Legal Case"},
			fields=["lawyer"]
		)

		recipients = []
		for lawyer in lawyers:
			user = frappe.db.get_value("Employee", lawyer.lawyer, "user_id")
			if user:
				recipients.append(user)

		if recipients:
			frappe.sendmail(
				recipients=recipients,
				subject=_("Hearing Reminder: {0}").format(self.case_title),
				template="hearing_reminder",
				args={
					"case_title": self.case_title,
					"hearing_date": self.hearing_date,
					"hearing_time": self.hearing_time,
					"court": frappe.db.get_value("Court", self.court, "court_name") if self.court else "",
					"hearing_type": self.hearing_type,
					"judge": frappe.db.get_value("Judge", self.judge, "judge_name") if self.judge else ""
				}
			)

	def on_update(self):
		"""Actions on update"""
		self.update_case_status()
		self.create_next_hearing()

	def update_case_status(self):
		"""Update case status based on hearing outcome"""
		if self.outcome and self.case:
			case_doc = frappe.get_doc("Legal Case", self.case)

			if self.outcome == "Case Closed":
				case_doc.status = "Closed"
			elif self.outcome == "Adjourned" and self.next_hearing_date:
				case_doc.status = "Hearing Scheduled"
			elif self.outcome in ["Granted", "Denied"]:
				case_doc.status = "Judgement Delivered"

			case_doc.save()

	def create_next_hearing(self):
		"""Create next hearing if scheduled"""
		if self.next_hearing_date and self.outcome == "Adjourned":
			next_hearing = frappe.get_doc({
				"doctype": "Case Hearing",
				"case": self.case,
				"court": self.court,
				"judge": self.judge,
				"hearing_date": self.next_hearing_date,
				"hearing_type": "Mention",  # Default to mention for adjourned hearings
				"status": "Scheduled",
				"hearing_purpose": f"Follow-up to hearing on {self.hearing_date}"
			})
			next_hearing.insert()

	def on_submit(self):
		"""Actions when hearing is submitted"""
		self.create_case_activity()

	def create_case_activity(self):
		"""Create case activity record"""
		if self.case:
			activity = frappe.get_doc({
				"doctype": "Case Activity",
				"case": self.case,
				"activity_type": f"Hearing - {self.hearing_type}",
				"description": f"Hearing held on {self.hearing_date}. Outcome: {self.outcome or 'Pending'}",
				"date": self.hearing_date
			})
			activity.insert()


@frappe.whitelist()
def get_upcoming_hearings(days=30):
	"""Get upcoming hearings within specified days"""
	from frappe.utils import add_days, nowdate

	end_date = add_days(nowdate(), days)

	hearings = frappe.db.sql("""
		SELECT
			ch.name,
			ch.case,
			lc.case_title,
			ch.hearing_date,
			ch.hearing_time,
			ch.hearing_type,
			ch.court,
			ch.judge,
			ch.status
		FROM `tabCase Hearing` ch
		JOIN `tabLegal Case` lc ON lc.name = ch.case
		WHERE ch.hearing_date BETWEEN %s AND %s
			AND ch.docstatus = 1
			AND lc.docstatus = 1
		ORDER BY ch.hearing_date ASC, ch.hearing_time ASC
	""", (nowdate(), end_date), as_dict=True)

	return hearings


@frappe.whitelist()
def get_hearings_for_case(case):
	"""Get all hearings for a specific case"""
	hearings = frappe.get_all("Case Hearing",
		filters={"case": case, "docstatus": 1},
		fields=["name", "hearing_date", "hearing_time", "hearing_type", "status", "outcome", "next_hearing_date"],
		order_by="hearing_date desc"
	)

	return hearings


@frappe.whitelist()
def get_court_schedule(court, date):
	"""Get hearing schedule for a specific court on a specific date"""
	hearings = frappe.db.sql("""
		SELECT
			ch.hearing_time,
			ch.hearing_type,
			lc.case_title,
			ch.status
		FROM `tabCase Hearing` ch
		JOIN `tabLegal Case` lc ON lc.name = ch.case
		WHERE ch.court = %s
			AND ch.hearing_date = %s
			AND ch.docstatus = 1
		ORDER BY ch.hearing_time ASC
	""", (court, date), as_dict=True)

	return hearings


@frappe.whitelist()
def postpone_hearing(hearing_id, new_date, new_time=None, reason=None):
	"""Postpone a hearing to a new date/time"""
	if not frappe.has_permission("Case Hearing", "write"):
		frappe.throw(_("Not permitted"))

	doc = frappe.get_doc("Case Hearing", hearing_id)
	doc.hearing_date = new_date
	if new_time:
		doc.hearing_time = new_time
	doc.status = "Postponed"

	if reason:
		doc.notes = f"{doc.notes or ''}\n\nPostponed: {reason}".strip()

	doc.save()

	return {"status": "success", "message": _("Hearing postponed successfully")}