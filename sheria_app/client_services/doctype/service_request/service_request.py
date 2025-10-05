# Service Request DocType
# Copyright (c) 2024, Sheria Legal Technologies
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import nowdate, add_days


class ServiceRequest(Document):
	def validate(self):
		self.set_service_details()
		self.set_client_details()
		self.set_creation_details()
		self.set_priority_based_on_urgency()
		self.validate_dates()

	def set_service_details(self):
		"""Set service details from Legal Service doctype"""
		if self.service:
			service_doc = frappe.get_doc("Legal Service", self.service)
			self.service_name = service_doc.service_name
			self.service_fee = service_doc.price
			self.billing_type = service_doc.billing_type

	def set_client_details(self):
		"""Set client details from Client doctype"""
		if self.client:
			self.client_name = frappe.db.get_value("Client", self.client, "client_name")

	def set_creation_details(self):
		"""Set creation details"""
		if self.is_new():
			self.created_by = frappe.session.user
			self.creation_date = nowdate()

	def set_priority_based_on_urgency(self):
		"""Set priority based on urgency"""
		priority_map = {
			"Normal": "Medium",
			"Urgent": "High",
			"Critical": "Critical"
		}
		if self.urgency:
			self.priority = priority_map.get(self.urgency, "Medium")

	def validate_dates(self):
		"""Validate preferred date is not in the past"""
		if self.preferred_date and self.preferred_date < nowdate():
			frappe.throw(_("Preferred completion date cannot be in the past"))

	def on_update(self):
		"""Actions on update"""
		self.notify_status_change()
		self.create_case_if_approved()
		self.update_completion_date()

	def notify_status_change(self):
		"""Send notification on status change"""
		if self.has_value_changed("status"):
			self.send_status_notification()

	def send_status_notification(self):
		"""Send status change notification to client"""
		if self.client and self.status in ["Approved", "In Progress", "Completed", "Rejected"]:
			client_email = frappe.db.get_value("Client", self.client, "email_address")
			if client_email:
				frappe.sendmail(
					recipients=[client_email],
					subject=_("Service Request Status Update: {0}").format(self.service_name),
					template="service_request_status",
					args={
						"service_name": self.service_name,
						"status": self.status,
						"request_id": self.name,
						"client_name": self.client_name
					}
				)

	def create_case_if_approved(self):
		"""Create legal case when service request is approved"""
		if self.status == "Approved" and not self.has_value_changed("status"):
			return

		if self.status == "Approved":
			# Create a legal case for this service request
			case = frappe.get_doc({
				"doctype": "Legal Case",
				"case_title": f"{self.service_name} - {self.client_name}",
				"client": self.client,
				"case_type": self.get_case_type_from_service(),
				"description": self.description,
				"status": "Open",
				"service_request": self.name
			})
			case.insert()

			# Link the case back to this service request
			self.db_set("case", case.name)

	def get_case_type_from_service(self):
		"""Get case type based on service category"""
		service_category = frappe.db.get_value("Legal Service", self.service, "category")

		category_case_type_map = {
			"Corporate Law": "Corporate Litigation",
			"Commercial Law": "Commercial Dispute",
			"Litigation": "General Litigation",
			"Family Law": "Family Dispute",
			"Property Law": "Property Dispute",
			"Employment Law": "Employment Dispute",
			"Intellectual Property": "IP Dispute",
			"Tax Law": "Tax Dispute",
			"Immigration Law": "Immigration Matter",
			"Criminal Law": "Criminal Case",
			"Constitutional Law": "Constitutional Matter",
			"Administrative Law": "Administrative Matter"
		}

		return category_case_type_map.get(service_category, "General Legal Matter")

	def update_completion_date(self):
		"""Update actual completion date when status changes to completed"""
		if self.status == "Completed" and not self.actual_completion:
			self.actual_completion = nowdate()

	def on_submit(self):
		"""Actions when service request is submitted"""
		self.status = "Submitted"
		self.notify_submission()

	def notify_submission(self):
		"""Notify relevant staff about new service request"""
		# Find users with appropriate roles to notify
		admin_users = frappe.get_all("Has Role",
			filters={"role": ["in", ["Legal Admin", "Lawyer"]]},
			fields=["parent"]
		)

		recipients = [user.parent for user in admin_users]

		if recipients:
			frappe.sendmail(
				recipients=recipients,
				subject=_("New Service Request: {0}").format(self.service_name),
				template="new_service_request",
				args={
					"service_name": self.service_name,
					"client_name": self.client_name,
					"description": self.description,
					"urgency": self.urgency,
					"request_id": self.name
				}
			)


@frappe.whitelist()
def get_client_service_requests(client=None, status=None):
	"""Get service requests for a client"""
	if not client:
		client = frappe.session.user

	filters = {"docstatus": 1}
	if client:
		filters["client"] = client
	if status:
		filters["status"] = status

	requests = frappe.get_all("Service Request",
		filters=filters,
		fields=["name", "service", "service_name", "request_date", "preferred_date",
				"status", "service_fee", "payment_status", "estimated_completion"],
		order_by="request_date desc"
	)

	return requests


@frappe.whitelist()
def get_pending_service_requests():
	"""Get all pending service requests for staff"""
	requests = frappe.get_all("Service Request",
		filters={
			"status": ["in", ["Submitted", "Under Review", "Approved", "In Progress"]],
			"docstatus": 1
		},
		fields=["name", "service", "service_name", "client", "client_name",
				"request_date", "urgency", "priority", "status"],
		order_by="priority desc, request_date asc"
	)

	return requests


@frappe.whitelist()
def update_service_request_status(request_id, status, notes=None):
	"""Update service request status"""
	if not frappe.has_permission("Service Request", "write"):
		frappe.throw(_("Not permitted"))

	doc = frappe.get_doc("Service Request", request_id)
	old_status = doc.status
	doc.status = status

	if notes:
		doc.internal_notes = f"{doc.internal_notes or ''}\n{nowdate()}: {notes}".strip()

	doc.save()

	return {"status": "success", "message": _("Service request status updated")}


@frappe.whitelist()
def submit_service_feedback(request_id, rating, comments=None):
	"""Submit client feedback for completed service"""
	doc = frappe.get_doc("Service Request", request_id)

	# Check if user is the client
	client_user = frappe.db.get_value("Client", doc.client, "user")
	if frappe.session.user != client_user:
		frappe.throw(_("Not permitted to submit feedback for this service request"))

	doc.feedback_rating = rating
	if comments:
		doc.feedback_comments = comments

	doc.save()

	return {"status": "success", "message": _("Feedback submitted successfully")}