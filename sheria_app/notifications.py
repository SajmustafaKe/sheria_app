# Sheria Notifications Module
# Copyright (c) 2024, Sheria Legal Technologies
# For license information, please see license.txt

import frappe
from frappe import _

def get_notification_config():
	"""Get notification configuration for Sheria app"""
	return {
		"for_doctype": {
			"Legal Case": {
				"case_assigned": {
					"doc_type": "Legal Case",
					"send_to_all_assigned": 1,
					"subject": _("New Case Assigned: {0}"),
					"message": _("You have been assigned a new case: {0}"),
					"attach_print": 1
				},
				"case_status_changed": {
					"doc_type": "Legal Case",
					"send_to_all_assigned": 1,
					"subject": _("Case Status Changed: {0}"),
					"message": _("Case status has been changed to: {0}"),
					"attach_print": 0
				},
				"case_deadline_approaching": {
					"doc_type": "Legal Case",
					"send_to_all_assigned": 1,
					"subject": _("Case Deadline Approaching: {0}"),
					"message": _("Case deadline is approaching: {0}"),
					"attach_print": 0
				},
				"case_closed": {
					"doc_type": "Legal Case",
					"send_to_client": 1,
					"subject": _("Case Closed: {0}"),
					"message": _("Your case has been closed. Please find the details attached."),
					"attach_print": 1
				}
			},
			"Service Request": {
				"service_submitted": {
					"doc_type": "Service Request",
					"send_to_assigned": 1,
					"subject": _("New Service Request: {0}"),
					"message": _("A new service request has been submitted: {0}"),
					"attach_print": 1
				},
				"service_approved": {
					"doc_type": "Service Request",
					"send_to_client": 1,
					"subject": _("Service Request Approved: {0}"),
					"message": _("Your service request has been approved. We will contact you soon."),
					"attach_print": 0
				},
				"service_completed": {
					"doc_type": "Service Request",
					"send_to_client": 1,
					"subject": _("Service Completed: {0}"),
					"message": _("Your requested service has been completed. Please find the details attached."),
					"attach_print": 1
				}
			},
			"Legal Service": {
				"service_booked": {
					"doc_type": "Legal Service",
					"send_to_client": 1,
					"subject": _("Service Booking Confirmation: {0}"),
					"message": _("Your service booking has been confirmed. Reference: {0}"),
					"attach_print": 1
				}
			}
		},
		"for_module": {
			"Legal Practice": {
				"daily_case_summary": {
					"subject": _("Daily Case Summary"),
					"message": _("Daily summary of case activities and updates"),
					"doctype": "Legal Case",
					"event": "daily",
					"send_to": ["Legal Admin", "Lawyer"]
				},
				"weekly_performance_report": {
					"subject": _("Weekly Performance Report"),
					"message": _("Weekly performance report for legal practice"),
					"doctype": "Legal Case",
					"event": "weekly",
					"send_to": ["Legal Admin"]
				}
			},
			"Client Services": {
				"client_feedback_received": {
					"subject": _("New Client Feedback"),
					"message": _("New feedback received from client"),
					"doctype": "Client Feedback",
					"event": "new",
					"send_to": ["Legal Admin", "Client Services"]
				},
				"service_request_overdue": {
					"subject": _("Overdue Service Request"),
					"message": _("Service request is overdue for response"),
					"doctype": "Service Request",
					"event": "overdue",
					"send_to": ["Legal Admin", "Client Services"]
				}
			}
		},
		"for_user": {
			"task_assigned": {
				"subject": _("New Task Assigned"),
				"message": _("You have been assigned a new task: {0}"),
				"doctype": "Task",
				"event": "new"
			},
			"mention": {
				"subject": _("You were mentioned"),
				"message": _("You were mentioned in: {0}"),
				"doctype": "Communication",
				"event": "mention"
			}
		}
	}

def get_notification_info(notification_name, doc, context=None):
	"""Get notification information for a specific notification"""
	config = get_notification_config()

	# Find notification in config
	for module, module_config in config.get("for_doctype", {}).items():
		if notification_name in module_config:
			notification = module_config[notification_name]
			break
	else:
		for module, module_config in config.get("for_module", {}).items():
			if notification_name in module_config:
				notification = module_config[notification_name]
				break
		else:
			for user_type, user_config in config.get("for_user", {}).items():
				if notification_name in user_config:
					notification = user_config[notification_name]
					break
			else:
				return None

	# Get recipients
	recipients = get_notification_recipients(notification, doc)

	# Get subject and message
	subject = notification.get("subject", "").format(doc.get_title() if hasattr(doc, 'get_title') else str(doc.name))
	message = notification.get("message", "").format(doc.get_title() if hasattr(doc, 'get_title') else str(doc.name))

	return {
		"recipients": recipients,
		"subject": subject,
		"message": message,
		"attach_print": notification.get("attach_print", 0)
	}

def get_notification_recipients(notification, doc):
	"""Get recipients for a notification"""
	recipients = []

	# Get recipients based on notification type
	if notification.get("send_to_all_assigned"):
		recipients.extend(get_assigned_users(doc))

	if notification.get("send_to_assigned"):
		recipients.extend(get_assigned_users(doc))

	if notification.get("send_to_client"):
		client_email = get_client_email(doc)
		if client_email:
			recipients.append(client_email)

	if notification.get("send_to"):
		for role in notification["send_to"]:
			recipients.extend(get_users_by_role(role))

	# Remove duplicates
	recipients = list(set(recipients))

	return recipients

def get_assigned_users(doc):
	"""Get users assigned to a document"""
	users = []

	# Check for assigned_to field
	if hasattr(doc, 'assigned_to') and doc.assigned_to:
		user_email = frappe.db.get_value("User", doc.assigned_to, "email")
		if user_email:
			users.append(user_email)

	# Check for assigned_lawyer field (Legal Case specific)
	if hasattr(doc, 'assigned_lawyer') and doc.assigned_lawyer:
		lawyer_email = frappe.db.get_value("Lawyer", doc.assigned_lawyer, "email")
		if lawyer_email:
			users.append(lawyer_email)

	# Check for _assign field
	if hasattr(doc, '_assign'):
		for user in doc._assign:
			user_email = frappe.db.get_value("User", user, "email")
			if user_email:
				users.append(user_email)

	return users

def get_client_email(doc):
	"""Get client email from document"""
	# Check for client field
	if hasattr(doc, 'client') and doc.client:
		client_email = frappe.db.get_value("Client", doc.client, "email")
		if client_email:
			return client_email

	# Check for client_email field
	if hasattr(doc, 'client_email') and doc.client_email:
		return doc.client_email

	return None

def get_users_by_role(role):
	"""Get users by role"""
	users = frappe.db.sql("""
		SELECT DISTINCT u.email
		FROM `tabUser` u
		JOIN `tabHas Role` hr ON hr.parent = u.name
		WHERE hr.role = %s
			AND u.enabled = 1
			AND u.email IS NOT NULL
	""", (role,), as_dict=True)

	return [user.email for user in users]

def send_notification(notification_name, doc, context=None):
	"""Send a notification"""
	try:
		notification_info = get_notification_info(notification_name, doc, context)

		if not notification_info:
			return

		# Send email notification
		if notification_info["recipients"]:
			frappe.sendmail(
				recipients=notification_info["recipients"],
				subject=notification_info["subject"],
				message=notification_info["message"],
				reference_doctype=doc.doctype,
				reference_name=doc.name,
				attach_print=notification_info.get("attach_print", 0)
			)

		# Log notification
		log_notification(notification_name, doc, notification_info)

	except Exception as e:
		frappe.log_error(f"Error sending notification {notification_name}: {str(e)}")

def log_notification(notification_name, doc, notification_info):
	"""Log notification for tracking"""
	try:
		log = frappe.get_doc({
			"doctype": "Notification Log",
			"notification_name": notification_name,
			"document_type": doc.doctype,
			"document_name": doc.name,
			"recipients": ", ".join(notification_info["recipients"]),
			"subject": notification_info["subject"],
			"sent_at": frappe.utils.now()
		})
		log.insert(ignore_permissions=True)

	except Exception as e:
		frappe.log_error(f"Error logging notification: {str(e)}")

# Custom notification triggers

def case_assigned_notification(doc, method):
	"""Send notification when case is assigned"""
	if doc.assigned_lawyer and doc.has_value_changed('assigned_lawyer'):
		send_notification("case_assigned", doc)

def case_status_changed_notification(doc, method):
	"""Send notification when case status changes"""
	if doc.has_value_changed('status'):
		send_notification("case_status_changed", doc)

def case_deadline_notification():
	"""Send deadline approaching notifications"""
	try:
		# Get cases with deadlines approaching
		cases = frappe.db.sql("""
			SELECT name
			FROM `tabLegal Case`
			WHERE deadline_date IS NOT NULL
				AND deadline_date >= CURDATE()
				AND deadline_date <= DATE_ADD(CURDATE(), INTERVAL 7 DAY)
				AND status IN ('Active', 'Pending')
				AND docstatus = 1
		""", as_dict=True)

		for case in cases:
			doc = frappe.get_doc("Legal Case", case.name)
			send_notification("case_deadline_approaching", doc)

	except Exception as e:
		frappe.log_error(f"Error sending deadline notifications: {str(e)}")

def service_request_notifications(doc, method):
	"""Handle service request notifications"""
	if doc.is_new():
		send_notification("service_submitted", doc)
	elif doc.has_value_changed('status'):
		if doc.status == "Approved":
			send_notification("service_approved", doc)
		elif doc.status == "Completed":
			send_notification("service_completed", doc)

def client_feedback_notification(doc, method):
	"""Send notification for new client feedback"""
	if doc.is_new():
		send_notification("client_feedback_received", doc)

def overdue_service_check():
	"""Check for overdue service requests"""
	try:
		# Get overdue service requests
		overdue_requests = frappe.db.sql("""
			SELECT name
			FROM `tabService Request`
			WHERE status = 'Submitted'
				AND DATE(request_date) <= DATE_SUB(CURDATE(), INTERVAL 7 DAY)
				AND docstatus = 1
		""", as_dict=True)

		for request in overdue_requests:
			doc = frappe.get_doc("Service Request", request.name)
			send_notification("service_request_overdue", doc)

	except Exception as e:
		frappe.log_error(f"Error checking overdue services: {str(e)}")