# Case Activity DocType
# Copyright (c) 2024, Sheria Legal Technologies
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class CaseActivity(Document):
	def validate(self):
		self.set_case_title()
		self.validate_date()
		self.update_case_last_activity()

	def set_case_title(self):
		"""Set case title from Legal Case doctype"""
		if self.case:
			self.case_title = frappe.db.get_value("Legal Case", self.case, "case_details_title")

	def validate_date(self):
		"""Validate activity date is not in the future"""
		from frappe.utils import nowdate
		if self.date and self.date > nowdate():
			frappe.throw(_("Activity date cannot be in the future"))

	def update_case_last_activity(self):
		"""Update the last activity date on the case"""
		if self.case and self.date:
			frappe.db.set_value("Legal Case", self.case, "last_activity_date", self.date)

	def on_update(self):
		"""Actions on update"""
		self.create_time_entry_if_needed()

	def create_time_entry_if_needed(self):
		"""Create time entry if time is logged"""
		if self.time_spent and self.time_spent > 0 and self.performed_by:
			# Check if time entry already exists for this activity
			existing_entry = frappe.db.exists("Time Entry", {
				"case": self.case,
				"date": self.date,
				"activity_type": self.activity_type,
				"hours": self.time_spent
			})

			if not existing_entry:
				# Check if employee exists for this user
				employee = frappe.db.get_value("Employee", {"user_id": self.performed_by}, "name")
				if employee:
					time_entry = frappe.get_doc({
						"doctype": "Time Entry",
						"employee": employee,
						"case": self.case,
						"activity_type": self.activity_type,
						"date": self.date,
						"hours": self.time_spent,
						"description": f"Activity: {self.description}",
						"is_billable": 1
					})
					time_entry.insert()


@frappe.whitelist()
def get_case_activities(case, limit=50):
	"""Get activities for a specific case"""
	activities = frappe.get_all("Case Activity",
		filters={"case": case, "docstatus": 1},
		fields=["name", "activity_type", "date", "description", "performed_by", "time_spent", "status"],
		order_by="date desc, creation desc",
		limit=limit
	)

	return activities


@frappe.whitelist()
def get_recent_activities(days=30):
	"""Get recent case activities across all cases"""
	from frappe.utils import add_days, nowdate

	start_date = add_days(nowdate(), -days)

	activities = frappe.db.sql("""
		SELECT
			ca.name,
			ca.case,
			lc.case_title,
			ca.activity_type,
			ca.date,
			ca.description,
			ca.performed_by,
			ca.time_spent
		FROM `tabCase Activity` ca
		JOIN `tabLegal Case` lc ON lc.name = ca.case
		WHERE ca.date >= %s
			AND ca.docstatus = 1
			AND lc.docstatus = 1
		ORDER BY ca.date DESC, ca.creation DESC
		LIMIT 100
	""", (start_date,), as_dict=True)

	return activities


@frappe.whitelist()
def get_activity_summary(case=None, start_date=None, end_date=None):
	"""Get activity summary for reporting"""
	filters = {"docstatus": 1}

	if case:
		filters["case"] = case
	if start_date:
		filters["date"] >= start_date
	if end_date:
		filters["date"] <= end_date

	summary = frappe.db.sql("""
		SELECT
			activity_type,
			COUNT(*) as count,
			SUM(time_spent) as total_time,
			SUM(cost_incurred) as total_cost
		FROM `tabCase Activity`
		WHERE {conditions}
		GROUP BY activity_type
		ORDER BY count DESC
	""".format(conditions=" AND ".join([f"{k} = %s" if not isinstance(v, str) or not v.startswith(('>=', '<=')) else f"{k} {v[:2]} %s" for k, v in filters.items()])), tuple(filters.values()), as_dict=True)

	return summary


@frappe.whitelist()
def get_user_activities(user=None, start_date=None, end_date=None):
	"""Get activities performed by a specific user"""
	if not user:
		user = frappe.session.user

	filters = {"performed_by": user, "docstatus": 1}

	if start_date:
		filters["date"] >= start_date
	if end_date:
		filters["date"] <= end_date

	activities = frappe.get_all("Case Activity",
		filters=filters,
		fields=["name", "case", "case_title", "activity_type", "date", "description", "time_spent", "cost_incurred"],
		order_by="date desc"
	)

	return activities