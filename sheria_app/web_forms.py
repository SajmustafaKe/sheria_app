# Sheria Web Forms Module
# Copyright (c) 2024, Sheria Legal Technologies
# For license information, please see license.txt

import frappe
from frappe import _

def get_web_forms():
	"""Get web form configurations for Sheria app"""
	return {
		"service_request": {
			"name": "Service Request",
			"title": _("Request Legal Services"),
			"doc_type": "Service Request",
			"login_required": 0,
			"allow_edit": 0,
			"allow_multiple": 1,
			"allow_delete": 0,
			"allow_print": 1,
			"web_form_fields": get_service_request_fields(),
			"success_message": _("Your service request has been submitted successfully. We will contact you within 24 hours."),
			"success_url": "/service-request-submitted"
		},
		"consultation_booking": {
			"name": "Consultation Booking",
			"title": _("Book a Consultation"),
			"doc_type": "Consultation",
			"login_required": 0,
			"allow_edit": 0,
			"allow_multiple": 1,
			"allow_delete": 0,
			"allow_print": 1,
			"web_form_fields": get_consultation_booking_fields(),
			"success_message": _("Your consultation has been booked successfully. You will receive a confirmation email shortly."),
			"success_url": "/consultation-booked"
		},
		"client_registration": {
			"name": "Client Registration",
			"title": _("Register as Client"),
			"doc_type": "Client",
			"login_required": 0,
			"allow_edit": 0,
			"allow_multiple": 0,
			"allow_delete": 0,
			"allow_print": 0,
			"web_form_fields": get_client_registration_fields(),
			"success_message": _("Your registration has been submitted successfully. We will review your application and contact you soon."),
			"success_url": "/registration-submitted"
		},
		"client_feedback": {
			"name": "Client Feedback",
			"title": _("Share Your Feedback"),
			"doc_type": "Client Feedback",
			"login_required": 0,
			"allow_edit": 0,
			"allow_multiple": 1,
			"allow_delete": 0,
			"allow_print": 0,
			"web_form_fields": get_client_feedback_fields(),
			"success_message": _("Thank you for your feedback. Your input helps us improve our services."),
			"success_url": "/feedback-submitted"
		},
		"document_request": {
			"name": "Document Request",
			"title": _("Request Legal Documents"),
			"doc_type": "Document Request",
			"login_required": 0,
			"allow_edit": 0,
			"allow_multiple": 1,
			"allow_delete": 0,
			"allow_print": 0,
			"web_form_fields": get_document_request_fields(),
			"success_message": _("Your document request has been submitted. We will process it and contact you soon."),
			"success_url": "/document-request-submitted"
		}
	}

def get_service_request_fields():
	"""Get fields for service request web form"""
	return [
		{
			"fieldname": "client_name",
			"fieldtype": "Data",
			"label": _("Full Name"),
			"reqd": 1,
			"max_length": 140
		},
		{
			"fieldname": "email",
			"fieldtype": "Data",
			"label": _("Email Address"),
			"reqd": 1,
			"options": "Email",
			"max_length": 140
		},
		{
			"fieldname": "phone",
			"fieldtype": "Data",
			"label": _("Phone Number"),
			"reqd": 1,
			"max_length": 20
		},
		{
			"fieldname": "service_type",
			"fieldtype": "Select",
			"label": _("Service Type"),
			"reqd": 1,
			"options": "\nLegal Consultation\nDocument Review\nContract Drafting\nCase Filing\nLegal Research\nOther"
		},
		{
			"fieldname": "priority",
			"fieldtype": "Select",
			"label": _("Priority"),
			"reqd": 1,
			"options": "Low\nMedium\nHigh\nUrgent"
		},
		{
			"fieldname": "description",
			"fieldtype": "Text",
			"label": _("Description"),
			"reqd": 1,
			"max_height": 150
		},
		{
			"fieldname": "preferred_contact_method",
			"fieldtype": "Select",
			"label": _("Preferred Contact Method"),
			"reqd": 0,
			"options": "Email\nPhone\nWhatsApp"
		},
		{
			"fieldname": "attachment",
			"fieldtype": "Attach",
			"label": _("Attach Documents (if any)"),
			"reqd": 0
		}
	]

def get_consultation_booking_fields():
	"""Get fields for consultation booking web form"""
	return [
		{
			"fieldname": "client_name",
			"fieldtype": "Data",
			"label": _("Full Name"),
			"reqd": 1,
			"max_length": 140
		},
		{
			"fieldname": "email",
			"fieldtype": "Data",
			"label": _("Email Address"),
			"reqd": 1,
			"options": "Email",
			"max_length": 140
		},
		{
			"fieldname": "phone",
			"fieldtype": "Data",
			"label": _("Phone Number"),
			"reqd": 1,
			"max_length": 20
		},
		{
			"fieldname": "consultation_type",
			"fieldtype": "Select",
			"label": _("Consultation Type"),
			"reqd": 1,
			"options": "\nInitial Consultation\nFollow-up Consultation\nLegal Advice\nCase Review\nOther"
		},
		{
			"fieldname": "practice_area",
			"fieldtype": "Select",
			"label": _("Practice Area"),
			"reqd": 1,
			"options": "\nCorporate Law\nCriminal Law\nFamily Law\nProperty Law\nEmployment Law\nIntellectual Property\nOther"
		},
		{
			"fieldname": "preferred_date",
			"fieldtype": "Date",
			"label": _("Preferred Date"),
			"reqd": 1
		},
		{
			"fieldname": "preferred_time",
			"fieldtype": "Select",
			"label": _("Preferred Time"),
			"reqd": 1,
			"options": "\n09:00 AM\n10:00 AM\n11:00 AM\n02:00 PM\n03:00 PM\n04:00 PM\n05:00 PM"
		},
		{
			"fieldname": "duration",
			"fieldtype": "Select",
			"label": _("Duration"),
			"reqd": 1,
			"options": "30 minutes\n60 minutes\n90 minutes"
		},
		{
			"fieldname": "description",
			"fieldtype": "Text",
			"label": _("Brief Description of Your Legal Matter"),
			"reqd": 1,
			"max_height": 150
		},
		{
			"fieldname": "consultation_mode",
			"fieldtype": "Select",
			"label": _("Consultation Mode"),
			"reqd": 1,
			"options": "In-Person\nVideo Call\nPhone Call"
		}
	]

def get_client_registration_fields():
	"""Get fields for client registration web form"""
	return [
		{
			"fieldname": "client_name",
			"fieldtype": "Data",
			"label": _("Full Name"),
			"reqd": 1,
			"max_length": 140
		},
		{
			"fieldname": "email",
			"fieldtype": "Data",
			"label": _("Email Address"),
			"reqd": 1,
			"options": "Email",
			"max_length": 140
		},
		{
			"fieldname": "phone",
			"fieldtype": "Data",
			"label": _("Phone Number"),
			"reqd": 1,
			"max_length": 20
		},
		{
			"fieldname": "client_type",
			"fieldtype": "Select",
			"label": _("Client Type"),
			"reqd": 1,
			"options": "Individual\nCompany\nOrganization"
		},
		{
			"fieldname": "id_number",
			"fieldtype": "Data",
			"label": _("ID/Passport Number"),
			"reqd": 1,
			"max_length": 20
		},
		{
			"fieldname": "address",
			"fieldtype": "Text",
			"label": _("Address"),
			"reqd": 1,
			"max_height": 100
		},
		{
			"fieldname": "date_of_birth",
			"fieldtype": "Date",
			"label": _("Date of Birth"),
			"reqd": 0
		},
		{
			"fieldname": "occupation",
			"fieldtype": "Data",
			"label": _("Occupation"),
			"reqd": 0,
			"max_length": 100
		},
		{
			"fieldname": "emergency_contact_name",
			"fieldtype": "Data",
			"label": _("Emergency Contact Name"),
			"reqd": 0,
			"max_length": 140
		},
		{
			"fieldname": "emergency_contact_phone",
			"fieldtype": "Data",
			"label": _("Emergency Contact Phone"),
			"reqd": 0,
			"max_length": 20
		},
		{
			"fieldname": "terms_accepted",
			"fieldtype": "Check",
			"label": _("I accept the terms and conditions"),
			"reqd": 1
		}
	]

def get_client_feedback_fields():
	"""Get fields for client feedback web form"""
	return [
		{
			"fieldname": "client_name",
			"fieldtype": "Data",
			"label": _("Your Name"),
			"reqd": 1,
			"max_length": 140
		},
		{
			"fieldname": "email",
			"fieldtype": "Data",
			"label": _("Email Address"),
			"reqd": 1,
			"options": "Email",
			"max_length": 140
		},
		{
			"fieldname": "service_type",
			"fieldtype": "Select",
			"label": _("Service Received"),
			"reqd": 1,
			"options": "\nLegal Consultation\nDocument Review\nContract Drafting\nCase Representation\nLegal Research\nOther"
		},
		{
			"fieldname": "overall_rating",
			"fieldtype": "Rating",
			"label": _("Overall Rating (1-5)"),
			"reqd": 1
		},
		{
			"fieldname": "timeliness_rating",
			"fieldtype": "Rating",
			"label": _("Timeliness of Service"),
			"reqd": 0
		},
		{
			"fieldname": "quality_rating",
			"fieldtype": "Rating",
			"label": _("Quality of Service"),
			"reqd": 0
		},
		{
			"fieldname": "communication_rating",
			"fieldtype": "Rating",
			"label": _("Communication"),
			"reqd": 0
		},
		{
			"fieldname": "value_rating",
			"fieldtype": "Rating",
			"label": _("Value for Money"),
			"reqd": 0
		},
		{
			"fieldname": "feedback",
			"fieldtype": "Text",
			"label": _("Detailed Feedback"),
			"reqd": 0,
			"max_height": 150
		},
		{
			"fieldname": "suggestions",
			"fieldtype": "Text",
			"label": _("Suggestions for Improvement"),
			"reqd": 0,
			"max_height": 100
		},
		{
			"fieldname": "would_recommend",
			"fieldtype": "Select",
			"label": _("Would you recommend our services?"),
			"reqd": 1,
			"options": "Yes\nNo\nMaybe"
		}
	]

def get_document_request_fields():
	"""Get fields for document request web form"""
	return [
		{
			"fieldname": "client_name",
			"fieldtype": "Data",
			"label": _("Full Name"),
			"reqd": 1,
			"max_length": 140
		},
		{
			"fieldname": "email",
			"fieldtype": "Data",
			"label": _("Email Address"),
			"reqd": 1,
			"options": "Email",
			"max_length": 140
		},
		{
			"fieldname": "phone",
			"fieldtype": "Data",
			"label": _("Phone Number"),
			"reqd": 1,
			"max_length": 20
		},
		{
			"fieldname": "document_type",
			"fieldtype": "Select",
			"label": _("Document Type"),
			"reqd": 1,
			"options": "\nContract Templates\nLegal Forms\nCourt Documents\nAgreement Templates\nPolicy Documents\nOther"
		},
		{
			"fieldname": "specific_document",
			"fieldtype": "Data",
			"label": _("Specific Document Name"),
			"reqd": 0,
			"max_length": 200
		},
		{
			"fieldname": "purpose",
			"fieldtype": "Text",
			"label": _("Purpose/Description"),
			"reqd": 1,
			"max_height": 100
		},
		{
			"fieldname": "urgency",
			"fieldtype": "Select",
			"label": _("Urgency"),
			"reqd": 1,
			"options": "Normal\nUrgent\nVery Urgent"
		},
		{
			"fieldname": "delivery_method",
			"fieldtype": "Select",
			"label": _("Preferred Delivery Method"),
			"reqd": 1,
			"options": "Email\nPhysical Copy\nBoth"
		}
	]

def create_default_web_forms():
	"""Create default web forms for Sheria app"""
	try:
		forms = get_web_forms()

		for form_key, form_data in forms.items():
			if not frappe.db.exists("Web Form", form_data["name"]):
				web_form = frappe.get_doc({
					"doctype": "Web Form",
					"name": form_data["name"],
					"title": form_data["title"],
					"doc_type": form_data["doc_type"],
					"login_required": form_data["login_required"],
					"allow_edit": form_data["allow_edit"],
					"allow_multiple": form_data["allow_multiple"],
					"allow_delete": form_data["allow_delete"],
					"allow_print": form_data["allow_print"],
					"success_message": form_data["success_message"],
					"success_url": form_data["success_url"]
				})

				# Add web form fields
				for field in form_data["web_form_fields"]:
					web_form.append("web_form_fields", field)

				web_form.insert(ignore_permissions=True)
				frappe.db.commit()

	except Exception as e:
		frappe.log_error(f"Error creating web forms: {str(e)}")

# Web form validation functions

def validate_service_request(doc, method):
	"""Validate service request web form submission"""
	# Check for duplicate requests from same email in last 24 hours
	recent_requests = frappe.db.sql("""
		SELECT COUNT(*) as count
		FROM `tabService Request`
		WHERE email = %s
			AND creation >= DATE_SUB(NOW(), INTERVAL 1 DAY)
			AND docstatus = 0
	""", (doc.email,), as_dict=True)

	if recent_requests and recent_requests[0].count >= 3:
		frappe.throw(_("You have reached the maximum number of service requests allowed per day. Please try again tomorrow."))

def validate_consultation_booking(doc, method):
	"""Validate consultation booking web form submission"""
	# Check if preferred date is not in the past
	if doc.preferred_date and doc.preferred_date < frappe.utils.today():
		frappe.throw(_("Preferred date cannot be in the past. Please select a future date."))

	# Check for booking conflicts (basic validation)
	existing_bookings = frappe.db.sql("""
		SELECT COUNT(*) as count
		FROM `tabConsultation`
		WHERE preferred_date = %s
			AND preferred_time = %s
			AND docstatus = 0
	""", (doc.preferred_date, doc.preferred_time), as_dict=True)

	if existing_bookings and existing_bookings[0].count > 0:
		frappe.throw(_("This time slot is already booked. Please select a different time."))

def validate_client_registration(doc, method):
	"""Validate client registration web form submission"""
	# Check if email already exists
	existing_client = frappe.db.exists("Client", {"email": doc.email})
	if existing_client:
		frappe.throw(_("A client with this email address already exists. Please use a different email or contact us for assistance."))

	# Validate ID number format (basic Kenyan ID validation)
	if doc.id_number:
		import re
		if not re.match(r'^[0-9]{8}$', doc.id_number):
			frappe.throw(_("Please enter a valid 8-digit ID number."))

def validate_client_feedback(doc, method):
	"""Validate client feedback web form submission"""
	# Check for excessive feedback submissions
	recent_feedback = frappe.db.sql("""
		SELECT COUNT(*) as count
		FROM `tabClient Feedback`
		WHERE email = %s
			AND creation >= DATE_SUB(NOW(), INTERVAL 1 DAY)
	""", (doc.email,), as_dict=True)

	if recent_feedback and recent_feedback[0].count >= 5:
		frappe.throw(_("You have submitted too many feedback forms today. Please try again tomorrow."))

def validate_document_request(doc, method):
	"""Validate document request web form submission"""
	# Check for duplicate document requests
	recent_requests = frappe.db.sql("""
		SELECT COUNT(*) as count
		FROM `tabDocument Request`
		WHERE email = %s
			AND document_type = %s
			AND creation >= DATE_SUB(NOW(), INTERVAL 7 DAY)
	""", (doc.email, doc.document_type), as_dict=True)

	if recent_requests and recent_requests[0].count > 0:
		frappe.throw(_("You have already requested this type of document recently. Please check your email or contact us if you haven't received it."))

# Web form success actions

def service_request_success_action(doc, method):
	"""Actions to perform after successful service request submission"""
	# Send confirmation email
	from .email_templates import send_service_request_confirmation_email
	send_service_request_confirmation_email(doc)

	# Create a task for the service team
	create_service_request_task(doc)

def consultation_booking_success_action(doc, method):
	"""Actions to perform after successful consultation booking"""
	# Send confirmation email
	from .email_templates import send_consultation_booked_email
	send_consultation_booked_email(doc)

	# Create calendar event
	create_consultation_calendar_event(doc)

def client_registration_success_action(doc, method):
	"""Actions to perform after successful client registration"""
	# Send welcome email
	from .email_templates import send_welcome_client_email
	send_welcome_client_email(doc)

	# Create welcome task
	create_client_welcome_task(doc)

def client_feedback_success_action(doc, method):
	"""Actions to perform after successful feedback submission"""
	# Send thank you email
	send_feedback_thank_you_email(doc)

def document_request_success_action(doc, method):
	"""Actions to perform after successful document request"""
	# Create processing task
	create_document_request_task(doc)

# Helper functions

def create_service_request_task(doc):
	"""Create a task for processing service request"""
	try:
		task = frappe.get_doc({
			"doctype": "Task",
			"subject": f"Process Service Request: {doc.name}",
			"description": f"Review and process service request from {doc.client_name} for {doc.service_type}",
			"priority": doc.priority,
			"exp_start_date": frappe.utils.today(),
			"exp_end_date": frappe.utils.add_days(frappe.utils.today(), 2)
		})
		task.insert(ignore_permissions=True)
		frappe.db.commit()
	except Exception as e:
		frappe.log_error(f"Error creating service request task: {str(e)}")

def create_consultation_calendar_event(doc):
	"""Create calendar event for consultation"""
	try:
		event = frappe.get_doc({
			"doctype": "Event",
			"subject": f"Consultation: {doc.client_name}",
			"description": f"Consultation booking for {doc.consultation_type}",
			"starts_on": f"{doc.preferred_date} {doc.preferred_time}",
			"ends_on": frappe.utils.add_to_date(f"{doc.preferred_date} {doc.preferred_time}", minutes=int(doc.duration.split()[0])),
			"event_type": "Public",
			"send_reminder": 1
		})
		event.insert(ignore_permissions=True)
		frappe.db.commit()
	except Exception as e:
		frappe.log_error(f"Error creating consultation calendar event: {str(e)}")

def create_client_welcome_task(doc):
	"""Create welcome task for new client"""
	try:
		task = frappe.get_doc({
			"doctype": "Task",
			"subject": f"Welcome New Client: {doc.client_name}",
			"description": f"Complete onboarding process for new client {doc.client_name}",
			"priority": "Medium",
			"exp_start_date": frappe.utils.today(),
			"exp_end_date": frappe.utils.add_days(frappe.utils.today(), 3)
		})
		task.insert(ignore_permissions=True)
		frappe.db.commit()
	except Exception as e:
		frappe.log_error(f"Error creating client welcome task: {str(e)}")

def send_feedback_thank_you_email(doc):
	"""Send thank you email for feedback"""
	try:
		frappe.sendmail(
			recipients=[doc.email],
			subject="Thank You for Your Feedback",
			message=f"Dear {doc.client_name},<br><br>Thank you for taking the time to share your feedback about our services. Your input is valuable to us and helps us improve.<br><br>Best regards,<br>Sheria Legal Management System"
		)
	except Exception as e:
		frappe.log_error(f"Error sending feedback thank you email: {str(e)}")

def create_document_request_task(doc):
	"""Create task for processing document request"""
	try:
		task = frappe.get_doc({
			"doctype": "Task",
			"subject": f"Process Document Request: {doc.name}",
			"description": f"Prepare and send requested document: {doc.document_type}",
			"priority": doc.urgency,
			"exp_start_date": frappe.utils.today(),
			"exp_end_date": frappe.utils.add_days(frappe.utils.today(), 1 if doc.urgency == "Urgent" else 3)
		})
		task.insert(ignore_permissions=True)
		frappe.db.commit()
	except Exception as e:
		frappe.log_error(f"Error creating document request task: {str(e)}")