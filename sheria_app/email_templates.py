# Sheria Email Templates Module
# Copyright (c) 2024, Sheria Legal Technologies
# For license information, please see license.txt

import frappe
from frappe import _

def get_email_templates():
	"""Get email template configurations for Sheria app"""
	return {
		"case_assigned": {
			"name": "Case Assigned",
			"subject": _("New Case Assigned: {{ doc.name }}"),
			"response": _("Dear {{ doc.assigned_lawyer_name }},<br><br>"
				"You have been assigned a new legal case. Please find the details below:<br><br>"
				"<strong>Case Details:</strong><br>"
				"Case Number: {{ doc.name }}<br>"
				"Client: {{ doc.client_name }}<br>"
				"Case Type: {{ doc.case_type }}<br>"
				"Priority: {{ doc.priority }}<br>"
				"Deadline: {{ doc.deadline_date }}<br><br>"
				"<strong>Description:</strong><br>{{ doc.description }}<br><br>"
				"Please review the case and take appropriate action.<br><br>"
				"Best regards,<br>Sheria Legal Management System")
		},
		"case_status_update": {
			"name": "Case Status Update",
			"subject": _("Case Status Updated: {{ doc.name }}"),
			"response": _("Dear {{ doc.client_name }},<br><br>"
				"We would like to inform you that the status of your case has been updated.<br><br>"
				"<strong>Case Details:</strong><br>"
				"Case Number: {{ doc.name }}<br>"
				"Current Status: {{ doc.status }}<br>"
				"Last Updated: {{ doc.modified }}<br><br>"
				"<strong>Update Notes:</strong><br>{{ doc.status_notes or 'No additional notes provided.' }}<br><br>"
				"If you have any questions, please contact us.<br><br>"
				"Best regards,<br>Sheria Legal Management System")
		},
		"case_closed": {
			"name": "Case Closed",
			"subject": _("Case Closed: {{ doc.name }}"),
			"response": _("Dear {{ doc.client_name }},<br><br>"
				"We are pleased to inform you that your case has been successfully closed.<br><br>"
				"<strong>Case Details:</strong><br>"
				"Case Number: {{ doc.name }}<br>"
				"Case Type: {{ doc.case_type }}<br>"
				"Closed Date: {{ doc.closure_date }}<br><br>"
				"<strong>Closure Summary:</strong><br>{{ doc.closure_notes }}<br><br>"
				"Thank you for choosing our legal services. We appreciate your trust in us.<br><br>"
				"Best regards,<br>Sheria Legal Management System")
		},
		"hearing_reminder": {
			"name": "Hearing Reminder",
			"subject": _("Hearing Reminder: {{ doc.case_name }} - {{ doc.hearing_date }}"),
			"response": _("Dear {{ doc.assigned_lawyer_name }},<br><br>"
				"This is a reminder for an upcoming hearing.<br><br>"
				"<strong>Hearing Details:</strong><br>"
				"Case: {{ doc.case_name }}<br>"
				"Court: {{ doc.court_name }}<br>"
				"Hearing Date: {{ doc.hearing_date }}<br>"
				"Hearing Time: {{ doc.hearing_time }}<br>"
				"Hearing Type: {{ doc.hearing_type }}<br><br>"
				"<strong>Notes:</strong><br>{{ doc.notes or 'No additional notes.' }}<br><br>"
				"Please ensure all preparations are complete.<br><br>"
				"Best regards,<br>Sheria Legal Management System")
		},
		"service_request_confirmation": {
			"name": "Service Request Confirmation",
			"subject": _("Service Request Confirmation: {{ doc.name }}"),
			"response": _("Dear {{ doc.client_name }},<br><br>"
				"Thank you for submitting your service request. We have received your request and will process it shortly.<br><br>"
				"<strong>Request Details:</strong><br>"
				"Request Number: {{ doc.name }}<br>"
				"Service Type: {{ doc.service_type }}<br>"
				"Priority: {{ doc.priority }}<br>"
				"Submission Date: {{ doc.request_date }}<br><br>"
				"<strong>Description:</strong><br>{{ doc.description }}<br><br>"
				"We will contact you within 24 hours with an update on your request.<br><br>"
				"Best regards,<br>Sheria Legal Management System")
		},
		"service_approved": {
			"name": "Service Approved",
			"subject": _("Service Request Approved: {{ doc.name }}"),
			"response": _("Dear {{ doc.client_name }},<br><br>"
				"Great news! Your service request has been approved and is now being processed.<br><br>"
				"<strong>Request Details:</strong><br>"
				"Request Number: {{ doc.name }}<br>"
				"Service Type: {{ doc.service_type }}<br>"
				"Approved Date: {{ doc.approval_date }}<br><br>"
				"<strong>Next Steps:</strong><br>{{ doc.approval_notes or 'Our team will contact you soon with further details.' }}<br><br>"
				"Thank you for choosing our services.<br><br>"
				"Best regards,<br>Sheria Legal Management System")
		},
		"service_completed": {
			"name": "Service Completed",
			"subject": _("Service Completed: {{ doc.name }}"),
			"response": _("Dear {{ doc.client_name }},<br><br>"
				"We are pleased to inform you that your requested service has been completed.<br><br>"
				"<strong>Service Details:</strong><br>"
				"Request Number: {{ doc.name }}<br>"
				"Service Type: {{ doc.service_type }}<br>"
				"Completion Date: {{ doc.completion_date }}<br><br>"
				"<strong>Service Summary:</strong><br>{{ doc.completion_notes }}<br><br>"
				"If you need any further assistance, please don't hesitate to contact us.<br><br>"
				"Best regards,<br>Sheria Legal Management System")
		},
		"consultation_booked": {
			"name": "Consultation Booked",
			"subject": _("Consultation Booking Confirmation: {{ doc.name }}"),
			"response": _("Dear {{ doc.client_name }},<br><br>"
				"Your consultation has been successfully booked. Please find the details below:<br><br>"
				"<strong>Consultation Details:</strong><br>"
				"Booking Reference: {{ doc.name }}<br>"
				"Lawyer: {{ doc.lawyer_name }}<br>"
				"Date: {{ doc.consultation_date }}<br>"
				"Time: {{ doc.consultation_time }}<br>"
				"Duration: {{ doc.duration }} minutes<br><br>"
				"<strong>Meeting Details:</strong><br>{{ doc.meeting_details or 'Details will be shared closer to the appointment.' }}<br><br>"
				"Please arrive 15 minutes early for your appointment.<br><br>"
				"Best regards,<br>Sheria Legal Management System")
		},
		"payment_reminder": {
			"name": "Payment Reminder",
			"subject": _("Payment Reminder: Invoice {{ doc.name }}"),
			"response": _("Dear {{ doc.client_name }},<br><br>"
				"This is a friendly reminder about an outstanding payment.<br><br>"
				"<strong>Invoice Details:</strong><br>"
				"Invoice Number: {{ doc.name }}<br>"
				"Amount Due: {{ doc.currency }} {{ doc.outstanding_amount }}<br>"
				"Due Date: {{ doc.due_date }}<br><br>"
				"<strong>Description:</strong><br>{{ doc.description or 'Legal services rendered.' }}<br><br>"
				"Please make the payment at your earliest convenience to avoid any delays in service.<br><br>"
				"Best regards,<br>Sheria Legal Management System")
		},
		"welcome_client": {
			"name": "Welcome Client",
			"subject": _("Welcome to Sheria Legal Services"),
			"response": _("Dear {{ doc.client_name }},<br><br>"
				"Welcome to Sheria Legal Management System! We are delighted to have you as our client.<br><br>"
				"Your client account has been successfully created with the following details:<br>"
				"Client ID: {{ doc.name }}<br>"
				"Registration Date: {{ doc.registration_date }}<br><br>"
				"<strong>Our Services:</strong><br>"
				"• Legal consultations and advice<br>"
				"• Case management and representation<br>"
				"• Document preparation and review<br>"
				"• Legal research and analysis<br><br>"
				"You can now access our client portal to:<br>"
				"• Submit service requests<br>"
				"• Track your cases<br>"
				"• View documents and updates<br>"
				"• Make payments online<br><br>"
				"If you have any questions, please don't hesitate to contact us.<br><br>"
				"Best regards,<br>Sheria Legal Management System")
		},
		"feedback_request": {
			"name": "Feedback Request",
			"subject": _("We Value Your Feedback: {{ doc.service_name }}"),
			"response": _("Dear {{ doc.client_name }},<br><br>"
				"Thank you for choosing Sheria Legal Services. We hope our service met your expectations.<br><br>"
				"We would greatly appreciate it if you could take a few moments to share your feedback about the service you received.<br><br>"
				"<strong>Service Details:</strong><br>"
				"Service: {{ doc.service_name }}<br>"
				"Completion Date: {{ doc.completion_date }}<br><br>"
				"Your feedback helps us improve our services and better serve you in the future.<br><br>"
				"[Feedback Link: {{ feedback_url }}]<br><br>"
				"Thank you for your time and continued trust in our services.<br><br>"
				"Best regards,<br>Sheria Legal Management System")
		},
		"newsletter": {
			"name": "Legal Newsletter",
			"subject": _("Legal Updates & Insights - {{ frappe.utils.format_date(frappe.utils.today()) }}"),
			"response": _("Dear Valued Client,<br><br>"
				"Welcome to our monthly legal newsletter. Here's what's new in the legal world:<br><br>"
				"<strong>Recent Legal Developments:</strong><br>"
				"{{ legal_updates }}<br><br>"
				"<strong>Case Law Updates:</strong><br>"
				"{{ case_law_updates }}<br><br>"
				"<strong>Practice Tips:</strong><br>"
				"{{ practice_tips }}<br><br>"
				"<strong>Upcoming Events:</strong><br>"
				"{{ upcoming_events }}<br><br>"
				"Stay informed and protected with Sheria Legal Services.<br><br>"
				"Best regards,<br>Sheria Legal Management System")
		}
	}

def create_default_email_templates():
	"""Create default email templates for Sheria app"""
	try:
		templates = get_email_templates()

		for template_key, template_data in templates.items():
			if not frappe.db.exists("Email Template", template_data["name"]):
				template = frappe.get_doc({
					"doctype": "Email Template",
					"name": template_data["name"],
					"subject": template_data["subject"],
					"response": template_data["response"],
					"use_html": 1
				})
				template.insert(ignore_permissions=True)
				frappe.db.commit()

	except Exception as e:
		frappe.log_error(f"Error creating email templates: {str(e)}")

def get_email_template_content(template_name, doc=None, context=None):
	"""Get email template content with document context"""
	try:
		template = frappe.get_doc("Email Template", template_name)

		if doc:
			# Render template with document context
			subject = frappe.render_template(template.subject, {"doc": doc})
			message = frappe.render_template(template.response, {"doc": doc})
		else:
			subject = template.subject
			message = template.response

		if context:
			subject = frappe.render_template(subject, context)
			message = frappe.render_template(message, context)

		return {
			"subject": subject,
			"message": message
		}

	except Exception as e:
		frappe.log_error(f"Error getting email template content: {str(e)}")
		return None

def send_email_from_template(template_name, recipients, doc=None, context=None, attachments=None):
	"""Send email using a template"""
	try:
		template_content = get_email_template_content(template_name, doc, context)

		if not template_content:
			return False

		frappe.sendmail(
			recipients=recipients,
			subject=template_content["subject"],
			message=template_content["message"],
			reference_doctype=doc.doctype if doc else None,
			reference_name=doc.name if doc else None,
			attachments=attachments
		)

		return True

	except Exception as e:
		frappe.log_error(f"Error sending email from template: {str(e)}")
		return False

# Template-specific helper functions

def send_case_assigned_email(doc):
	"""Send case assigned email"""
	if doc.assigned_lawyer:
		lawyer_email = frappe.db.get_value("Lawyer", doc.assigned_lawyer, "email")
		if lawyer_email:
			send_email_from_template("Case Assigned", [lawyer_email], doc)

def send_case_status_update_email(doc):
	"""Send case status update email to client"""
	if doc.client:
		client_email = frappe.db.get_value("Client", doc.client, "email")
		if client_email:
			send_email_from_template("Case Status Update", [client_email], doc)

def send_case_closed_email(doc):
	"""Send case closed email to client"""
	if doc.client:
		client_email = frappe.db.get_value("Client", doc.client, "email")
		if client_email:
			send_email_from_template("Case Closed", [client_email], doc)

def send_hearing_reminder_email(doc):
	"""Send hearing reminder email"""
	if doc.assigned_lawyer:
		lawyer_email = frappe.db.get_value("Lawyer", doc.assigned_lawyer, "email")
		if lawyer_email:
			send_email_from_template("Hearing Reminder", [lawyer_email], doc)

def send_service_request_confirmation_email(doc):
	"""Send service request confirmation email"""
	if doc.client:
		client_email = frappe.db.get_value("Client", doc.client, "email")
		if client_email:
			send_email_from_template("Service Request Confirmation", [client_email], doc)

def send_service_approved_email(doc):
	"""Send service approved email"""
	if doc.client:
		client_email = frappe.db.get_value("Client", doc.client, "email")
		if client_email:
			send_email_from_template("Service Approved", [client_email], doc)

def send_service_completed_email(doc):
	"""Send service completed email"""
	if doc.client:
		client_email = frappe.db.get_value("Client", doc.client, "email")
		if client_email:
			send_email_from_template("Service Completed", [client_email], doc)

def send_consultation_booked_email(doc):
	"""Send consultation booking confirmation email"""
	if doc.client:
		client_email = frappe.db.get_value("Client", doc.client, "email")
		if client_email:
			send_email_from_template("Consultation Booked", [client_email], doc)

def send_payment_reminder_email(doc):
	"""Send payment reminder email"""
	if doc.client:
		client_email = frappe.db.get_value("Client", doc.client, "email")
		if client_email:
			send_email_from_template("Payment Reminder", [client_email], doc)

def send_welcome_client_email(doc):
	"""Send welcome email to new client"""
	if doc.email:
		send_email_from_template("Welcome Client", [doc.email], doc)

def send_feedback_request_email(doc):
	"""Send feedback request email"""
	if doc.client:
		client_email = frappe.db.get_value("Client", doc.client, "email")
		if client_email:
			# Generate feedback URL
			feedback_url = f"/app/client-feedback?service={doc.name}"
			context = {"feedback_url": feedback_url}
			send_email_from_template("Feedback Request", [client_email], doc, context)

def send_newsletter_email(recipients, updates_data):
	"""Send newsletter email"""
	context = {
		"legal_updates": updates_data.get("legal_updates", "No updates this month."),
		"case_law_updates": updates_data.get("case_law_updates", "No case law updates."),
		"practice_tips": updates_data.get("practice_tips", "Check back next month for tips."),
		"upcoming_events": updates_data.get("upcoming_events", "No upcoming events.")
	}

	send_email_from_template("Legal Newsletter", recipients, context=context)