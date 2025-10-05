# Sheria App API Module
# Copyright (c) 2024, Coale Tech
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import now, getdate, add_days
import json

@frappe.whitelist()
def get_case_statistics():
	"""Get case statistics for dashboard"""
	try:
		# Get case counts by status
		case_stats = frappe.db.sql("""
			SELECT
				COUNT(*) as total_cases,
				SUM(CASE WHEN status = 'Active' THEN 1 ELSE 0 END) as active_cases,
				SUM(CASE WHEN status = 'Pending' THEN 1 ELSE 0 END) as pending_cases,
				SUM(CASE WHEN status = 'Closed' THEN 1 ELSE 0 END) as closed_cases
			FROM `tabLegal Case`
			WHERE docstatus = 1
		""", as_dict=True)[0]

		return {
			"total_cases": case_stats.total_cases or 0,
			"active_cases": case_stats.active_cases or 0,
			"pending_cases": case_stats.pending_cases or 0,
			"closed_cases": case_stats.closed_cases or 0
		}
	except Exception as e:
		frappe.log_error(f"Error getting case statistics: {str(e)}")
		return {"error": "Failed to get case statistics"}

@frappe.whitelist()
def get_upcoming_hearings(limit=5):
	"""Get upcoming case hearings"""
	try:
		hearings = frappe.db.sql("""
			SELECT
				ch.name,
				ch.case,
				lc.case_title,
				ch.court,
				ch.hearing_date,
				ch.hearing_time,
				ch.judge,
				ch.hearing_type
			FROM `tabCase Hearing` ch
			JOIN `tabLegal Case` lc ON lc.name = ch.case
			WHERE ch.hearing_date >= %s
				AND ch.docstatus = 1
				AND lc.docstatus = 1
			ORDER BY ch.hearing_date ASC, ch.hearing_time ASC
			LIMIT %s
		""", (getdate(), limit), as_dict=True)

		return hearings
	except Exception as e:
		frappe.log_error(f"Error getting upcoming hearings: {str(e)}")
		return []

@frappe.whitelist()
def get_recent_activities(limit=10):
	"""Get recent case activities"""
	try:
		activities = frappe.db.sql("""
			SELECT
				ca.name,
				ca.case,
				lc.case_title,
				ca.activity_type,
				ca.description,
				ca.creation as timestamp,
				ca.owner
			FROM `tabCase Activity` ca
			JOIN `tabLegal Case` lc ON lc.name = ca.case
			WHERE ca.docstatus = 1
				AND lc.docstatus = 1
			ORDER BY ca.creation DESC
			LIMIT %s
		""", (limit,), as_dict=True)

		# Format activities
		formatted_activities = []
		for activity in activities:
			formatted_activities.append({
				"activity": activity.activity_type,
				"description": activity.description,
				"case_title": activity.case_title,
				"timestamp": frappe.utils.format_datetime(activity.timestamp, "dd MMM yyyy HH:mm")
			})

		return formatted_activities
	except Exception as e:
		frappe.log_error(f"Error getting recent activities: {str(e)}")
		return []

@frappe.whitelist()
def get_client_services():
	"""Get available legal services for clients"""
	try:
		services = frappe.db.sql("""
			SELECT
				name,
				service_name,
				description,
				price,
				duration,
				category,
				is_active
			FROM `tabLegal Service`
			WHERE is_active = 1
				AND docstatus = 1
			ORDER BY category, service_name
		""", as_dict=True)

		return services
	except Exception as e:
		frappe.log_error(f"Error getting client services: {str(e)}")
		return []

@frappe.whitelist()
def get_service_requests(client=None):
	"""Get service requests for a client"""
	try:
		if not client:
			client = frappe.session.user

		requests = frappe.db.sql("""
			SELECT
				sr.name,
				sr.service,
				ls.service_name,
				sr.description,
				sr.status,
				sr.request_date,
				sr.preferred_date,
				sr.creation
			FROM `tabService Request` sr
			JOIN `tabLegal Service` ls ON ls.name = sr.service
			WHERE sr.client = %s
				AND sr.docstatus = 1
			ORDER BY sr.creation DESC
		""", (client,), as_dict=True)

		return requests
	except Exception as e:
		frappe.log_error(f"Error getting service requests: {str(e)}")
		return []

@frappe.whitelist()
def request_service(service):
	"""Request a legal service"""
	try:
		if not frappe.db.exists("Legal Service", service):
			return {"error": "Service not found"}

		# Create service request
		service_request = frappe.get_doc({
			"doctype": "Service Request",
			"service": service,
			"client": frappe.session.user,
			"status": "Draft",
			"request_date": getdate()
		})
		service_request.insert()

		return {"success": True, "request_id": service_request.name}
	except Exception as e:
		frappe.log_error(f"Error requesting service: {str(e)}")
		return {"error": "Failed to request service"}

@frappe.whitelist()
def submit_service_booking(**kwargs):
	"""Submit service booking from web form"""
	try:
		# Validate required fields
		required_fields = ["service_name", "client_name", "client_email", "client_phone"]
		for field in required_fields:
			if not kwargs.get(field):
				return {"error": f"{field.replace('_', ' ').title()} is required"}

		# Find or create client
		client = find_or_create_client(kwargs)

		# Find service
		service = frappe.db.get_value("Legal Service", {"service_name": kwargs.get("service_name")})
		if not service:
			return {"error": "Service not found"}

		# Create service request
		service_request = frappe.get_doc({
			"doctype": "Service Request",
			"service": service,
			"client": client,
			"description": kwargs.get("description", ""),
			"preferred_date": kwargs.get("preferred_date"),
			"status": "Submitted",
			"request_date": getdate(),
			"source": "Web Form"
		})
		service_request.insert()
		service_request.submit()

		# Send confirmation email
		send_booking_confirmation(service_request, kwargs)

		return {"success": True, "request_id": service_request.name}
	except Exception as e:
		frappe.log_error(f"Error submitting service booking: {str(e)}")
		return {"error": "Failed to submit booking"}

@frappe.whitelist()
def submit_contact(**kwargs):
	"""Submit contact form"""
	try:
		# Validate required fields
		required_fields = ["name", "email", "message"]
		for field in required_fields:
			if not kwargs.get(field):
				return {"error": f"{field.title()} is required"}

		# Create contact record
		contact = frappe.get_doc({
			"doctype": "Contact",
			"first_name": kwargs.get("name").split()[0],
			"last_name": " ".join(kwargs.get("name").split()[1:]) if len(kwargs.get("name").split()) > 1 else "",
			"email_id": kwargs.get("email"),
			"phone": kwargs.get("phone", ""),
			"address": kwargs.get("address", ""),
			"contact_type": "Customer"
		})
		contact.insert()

		# Send contact email
		send_contact_email(kwargs)

		return {"success": True, "contact_id": contact.name}
	except Exception as e:
		frappe.log_error(f"Error submitting contact: {str(e)}")
		return {"error": "Failed to submit contact"}

def find_or_create_client(data):
	"""Find existing client or create new one"""
	try:
		# Try to find existing client by email
		existing_client = frappe.db.get_value("Client", {"email": data.get("client_email")})
		if existing_client:
			return existing_client

		# Create new client
		client = frappe.get_doc({
			"doctype": "Client",
			"client_name": data.get("client_name"),
			"email": data.get("client_email"),
			"phone": data.get("client_phone"),
			"address": data.get("client_address", ""),
			"client_type": "Individual",
			"status": "Active"
		})
		client.insert()

		return client.name
	except Exception as e:
		frappe.log_error(f"Error finding/creating client: {str(e)}")
		return None

def send_booking_confirmation(service_request, data):
	"""Send booking confirmation email"""
	try:
		subject = _("Legal Service Booking Confirmation")
		message = frappe.render_template("sheria/templates/emails/booking_confirmation.html", {
			"service_request": service_request,
			"data": data
		})

		frappe.sendmail(
			recipients=[data.get("client_email")],
			subject=subject,
			message=message
		)
	except Exception as e:
		frappe.log_error(f"Error sending booking confirmation: {str(e)}")

def send_contact_email(data):
	"""Send contact form email"""
	try:
		subject = _("New Contact Form Submission")
		message = frappe.render_template("sheria/templates/emails/contact_form.html", {
			"data": data
		})

		# Send to admin
		admin_email = frappe.db.get_single_value("Sheria Settings", "admin_email") or "admin@sheria_app.co.ke"

		frappe.sendmail(
			recipients=[admin_email],
			subject=subject,
			message=message
		)
	except Exception as e:
		frappe.log_error(f"Error sending contact email: {str(e)}")

@frappe.whitelist()
def get_legal_fees(case=None, service=None):
	"""Get legal fees for case or service"""
	try:
		if case:
			fees = frappe.db.sql("""
				SELECT
					lf.fee_type,
					lf.amount,
					lf.currency,
					lf.description,
					lf.creation
				FROM `tabLegal Fee` lf
				WHERE lf.case = %s
					AND lf.docstatus = 1
				ORDER BY lf.creation DESC
			""", (case,), as_dict=True)
		elif service:
			fees = frappe.db.sql("""
				SELECT
					price as amount,
					currency,
					description
				FROM `tabLegal Service`
				WHERE name = %s
					AND docstatus = 1
			""", (service,), as_dict=True)
		else:
			return {"error": "Either case or service must be specified"}

		return fees
	except Exception as e:
		frappe.log_error(f"Error getting legal fees: {str(e)}")
		return {"error": "Failed to get fees"}

@frappe.whitelist()
def get_case_timeline(case):
	"""Get case timeline"""
	try:
		timeline = frappe.db.sql("""
			SELECT
				ct.activity_date,
				ct.activity_type,
				ct.description,
				ct.created_by,
				ct.creation
			FROM `tabCase Timeline` ct
			WHERE ct.case = %s
				AND ct.docstatus = 1
			ORDER BY ct.activity_date DESC, ct.creation DESC
		""", (case,), as_dict=True)

		return timeline
	except Exception as e:
		frappe.log_error(f"Error getting case timeline: {str(e)}")
		return []

@frappe.whitelist()
def get_case_documents(case):
	"""Get case documents"""
	try:
		documents = frappe.db.sql("""
			SELECT
				cd.document_name,
				cd.document_type,
				cd.file_url,
				cd.description,
				cd.upload_date,
				cd.created_by
			FROM `tabCase Document` cd
			WHERE cd.case = %s
				AND cd.docstatus = 1
			ORDER BY cd.upload_date DESC
		""", (case,), as_dict=True)

		return documents
	except Exception as e:
		frappe.log_error(f"Error getting case documents: {str(e)}")
		return []

# Time Entry APIs
@frappe.whitelist()
def get_time_entries(employee=None, case=None, date_from=None, date_to=None, status=None):
	"""Get time entries with optional filters"""
	try:
		filters = {"docstatus": 1}
		if employee:
			filters["employee"] = employee
		if case:
			filters["case"] = case
		if status:
			filters["status"] = status

		# Date range filter
		date_condition = ""
		if date_from and date_to:
			date_condition = f" AND date BETWEEN '{date_from}' AND '{date_to}'"
		elif date_from:
			date_condition = f" AND date >= '{date_from}'"
		elif date_to:
			date_condition = f" AND date <= '{date_to}'"

		time_entries = frappe.db.sql(f"""
			SELECT
				name,
				employee,
				employee_name,
				case,
				task,
				date,
				start_time,
				end_time,
				hours,
				description,
				status,
				billable,
				billing_rate,
				total_amount,
				creation
			FROM `tabTime Entry`
			WHERE docstatus = 1
			{date_condition}
			ORDER BY date DESC, creation DESC
		""", as_dict=True)

		return time_entries
	except Exception as e:
		frappe.log_error(f"Error getting time entries: {str(e)}")
		return []

@frappe.whitelist()
def create_time_entry(**kwargs):
	"""Create a new time entry"""
	try:
		# Validate required fields
		required_fields = ["employee", "date", "hours", "description"]
		for field in required_fields:
			if not kwargs.get(field):
				return {"error": f"{field.replace('_', ' ').title()} is required"}

		time_entry = frappe.get_doc({
			"doctype": "Time Entry",
			"employee": kwargs.get("employee"),
			"case": kwargs.get("case"),
			"task": kwargs.get("task"),
			"date": kwargs.get("date"),
			"start_time": kwargs.get("start_time"),
			"end_time": kwargs.get("end_time"),
			"hours": kwargs.get("hours"),
			"description": kwargs.get("description"),
			"billable": kwargs.get("billable", 1),
			"billing_rate": kwargs.get("billing_rate"),
			"status": "Draft"
		})
		time_entry.insert()

		return {"success": True, "time_entry_id": time_entry.name}
	except Exception as e:
		frappe.log_error(f"Error creating time entry: {str(e)}")
		return {"error": "Failed to create time entry"}

@frappe.whitelist()
def submit_time_entry(time_entry_id):
	"""Submit time entry for approval"""
	try:
		time_entry = frappe.get_doc("Time Entry", time_entry_id)
		time_entry.submit()

		return {"success": True}
	except Exception as e:
		frappe.log_error(f"Error submitting time entry: {str(e)}")
		return {"error": "Failed to submit time entry"}

# Task APIs
@frappe.whitelist()
def get_tasks(assigned_to=None, case=None, status=None, priority=None):
	"""Get tasks with optional filters"""
	try:
		filters = {"docstatus": 1}
		if assigned_to:
			filters["assigned_to"] = assigned_to
		if case:
			filters["case"] = case
		if status:
			filters["status"] = status
		if priority:
			filters["priority"] = priority

		tasks = frappe.db.sql("""
			SELECT
				name,
				subject,
				description,
				case,
				assigned_to,
				assigned_to_name,
				status,
				priority,
				due_date,
				progress,
				estimated_hours,
				actual_hours,
				creation,
				modified
			FROM `tabTask`
			WHERE docstatus = 1
			ORDER BY priority DESC, due_date ASC, creation DESC
		""", as_dict=True)

		return tasks
	except Exception as e:
		frappe.log_error(f"Error getting tasks: {str(e)}")
		return []

@frappe.whitelist()
def create_task(**kwargs):
	"""Create a new task"""
	try:
		# Validate required fields
		required_fields = ["subject", "assigned_to"]
		for field in required_fields:
			if not kwargs.get(field):
				return {"error": f"{field.replace('_', ' ').title()} is required"}

		task = frappe.get_doc({
			"doctype": "Task",
			"subject": kwargs.get("subject"),
			"description": kwargs.get("description"),
			"case": kwargs.get("case"),
			"assigned_to": kwargs.get("assigned_to"),
			"priority": kwargs.get("priority", "Medium"),
			"due_date": kwargs.get("due_date"),
			"estimated_hours": kwargs.get("estimated_hours"),
			"status": "Open"
		})
		task.insert()

		return {"success": True, "task_id": task.name}
	except Exception as e:
		frappe.log_error(f"Error creating task: {str(e)}")
		return {"error": "Failed to create task"}

@frappe.whitelist()
def update_task_progress(task_id, progress, status=None):
	"""Update task progress"""
	try:
		task = frappe.get_doc("Task", task_id)
		task.progress = progress
		if status:
			task.status = status
		task.save()

		return {"success": True}
	except Exception as e:
		frappe.log_error(f"Error updating task progress: {str(e)}")
		return {"error": "Failed to update task"}

# Case Hearing APIs
@frappe.whitelist()
def get_case_hearings(case=None, date_from=None, date_to=None, status=None):
	"""Get case hearings with optional filters"""
	try:
		filters = {"docstatus": 1}
		if case:
			filters["case"] = case
		if status:
			filters["status"] = status

		# Date range filter
		date_condition = ""
		if date_from and date_to:
			date_condition = f" AND hearing_date BETWEEN '{date_from}' AND '{date_to}'"
		elif date_from:
			date_condition = f" AND hearing_date >= '{date_from}'"
		elif date_to:
			date_condition = f" AND hearing_date <= '{date_to}'"

		hearings = frappe.db.sql(f"""
			SELECT
				name,
				case,
				hearing_date,
				hearing_time,
				court,
				judge,
				hearing_type,
				status,
				outcome,
				next_hearing_date,
				notes,
				creation
			FROM `tabCase Hearing`
			WHERE docstatus = 1
			{date_condition}
			ORDER BY hearing_date DESC, hearing_time DESC
		""", as_dict=True)

		return hearings
	except Exception as e:
		frappe.log_error(f"Error getting case hearings: {str(e)}")
		return []

@frappe.whitelist()
def create_case_hearing(**kwargs):
	"""Create a new case hearing"""
	try:
		# Validate required fields
		required_fields = ["case", "hearing_date", "court", "hearing_type"]
		for field in required_fields:
			if not kwargs.get(field):
				return {"error": f"{field.replace('_', ' ').title()} is required"}

		hearing = frappe.get_doc({
			"doctype": "Case Hearing",
			"case": kwargs.get("case"),
			"hearing_date": kwargs.get("hearing_date"),
			"hearing_time": kwargs.get("hearing_time"),
			"court": kwargs.get("court"),
			"judge": kwargs.get("judge"),
			"hearing_type": kwargs.get("hearing_type"),
			"notes": kwargs.get("notes"),
			"status": "Scheduled"
		})
		hearing.insert()

		return {"success": True, "hearing_id": hearing.name}
	except Exception as e:
		frappe.log_error(f"Error creating case hearing: {str(e)}")
		return {"error": "Failed to create hearing"}

@frappe.whitelist()
def update_hearing_outcome(hearing_id, outcome, next_hearing_date=None, notes=None):
	"""Update hearing outcome"""
	try:
		hearing = frappe.get_doc("Case Hearing", hearing_id)
		hearing.outcome = outcome
		hearing.status = "Completed"
		if next_hearing_date:
			hearing.next_hearing_date = next_hearing_date
		if notes:
			hearing.notes = notes
		hearing.save()

		return {"success": True}
	except Exception as e:
		frappe.log_error(f"Error updating hearing outcome: {str(e)}")
		return {"error": "Failed to update hearing"}

# Case Activity APIs
@frappe.whitelist()
def get_case_activities(case=None, activity_type=None, date_from=None, date_to=None):
	"""Get case activities with optional filters"""
	try:
		filters = {"docstatus": 1}
		if case:
			filters["case"] = case
		if activity_type:
			filters["activity_type"] = activity_type

		# Date range filter
		date_condition = ""
		if date_from and date_to:
			date_condition = f" AND date BETWEEN '{date_from}' AND '{date_to}'"
		elif date_from:
			date_condition = f" AND date >= '{date_from}'"
		elif date_to:
			date_condition = f" AND date <= '{date_to}'"

		activities = frappe.db.sql(f"""
			SELECT
				name,
				case,
				activity_type,
				date,
				time_spent,
				description,
				outcome,
				next_action,
				created_by,
				creation
			FROM `tabCase Activity`
			WHERE docstatus = 1
			{date_condition}
			ORDER BY date DESC, creation DESC
		""", as_dict=True)

		return activities
	except Exception as e:
		frappe.log_error(f"Error getting case activities: {str(e)}")
		return []

@frappe.whitelist()
def create_case_activity(**kwargs):
	"""Create a new case activity"""
	try:
		# Validate required fields
		required_fields = ["case", "activity_type", "date", "description"]
		for field in required_fields:
			if not kwargs.get(field):
				return {"error": f"{field.replace('_', ' ').title()} is required"}

		activity = frappe.get_doc({
			"doctype": "Case Activity",
			"case": kwargs.get("case"),
			"activity_type": kwargs.get("activity_type"),
			"date": kwargs.get("date"),
			"time_spent": kwargs.get("time_spent"),
			"description": kwargs.get("description"),
			"outcome": kwargs.get("outcome"),
			"next_action": kwargs.get("next_action")
		})
		activity.insert()

		return {"success": True, "activity_id": activity.name}
	except Exception as e:
		frappe.log_error(f"Error creating case activity: {str(e)}")
		return {"error": "Failed to create activity"}

# Legal Service APIs
@frappe.whitelist()
def get_legal_services(category=None, is_active=1):
	"""Get legal services with optional filters"""
	try:
		filters = {"docstatus": 1}
		if category:
			filters["category"] = category
		if is_active is not None:
			filters["is_active"] = is_active

		services = frappe.db.sql("""
			SELECT
				name,
				service_name,
				description,
				category,
				price,
				currency,
				duration,
				duration_unit,
				is_active,
				eligibility_criteria,
				creation
			FROM `tabLegal Service`
			WHERE docstatus = 1
			ORDER BY category, service_name
		""", as_dict=True)

		return services
	except Exception as e:
		frappe.log_error(f"Error getting legal services: {str(e)}")
		return []

@frappe.whitelist()
def create_legal_service(**kwargs):
	"""Create a new legal service"""
	try:
		# Validate required fields
		required_fields = ["service_name", "category", "price"]
		for field in required_fields:
			if not kwargs.get(field):
				return {"error": f"{field.replace('_', ' ').title()} is required"}

		service = frappe.get_doc({
			"doctype": "Legal Service",
			"service_name": kwargs.get("service_name"),
			"description": kwargs.get("description"),
			"category": kwargs.get("category"),
			"price": kwargs.get("price"),
			"currency": kwargs.get("currency", "KES"),
			"duration": kwargs.get("duration"),
			"duration_unit": kwargs.get("duration_unit", "Days"),
			"eligibility_criteria": kwargs.get("eligibility_criteria"),
			"is_active": kwargs.get("is_active", 1)
		})
		service.insert()

		return {"success": True, "service_id": service.name}
	except Exception as e:
		frappe.log_error(f"Error creating legal service: {str(e)}")
		return {"error": "Failed to create service"}

# Service Request APIs
@frappe.whitelist()
def get_service_requests(client=None, status=None, service=None):
	"""Get service requests with optional filters"""
	try:
		filters = {"docstatus": 1}
		if client:
			filters["client"] = client
		if status:
			filters["status"] = status
		if service:
			filters["service"] = service

		requests = frappe.db.sql("""
			SELECT
				sr.name,
				sr.service,
				ls.service_name,
				ls.category,
				sr.client,
				sr.description,
				sr.status,
				sr.request_date,
				sr.preferred_date,
				sr.approved_date,
				sr.source,
				sr.creation
			FROM `tabService Request` sr
			JOIN `tabLegal Service` ls ON ls.name = sr.service
			WHERE sr.docstatus = 1
			ORDER BY sr.creation DESC
		""", as_dict=True)

		return requests
	except Exception as e:
		frappe.log_error(f"Error getting service requests: {str(e)}")
		return []

@frappe.whitelist()
def create_service_request(**kwargs):
	"""Create a new service request"""
	try:
		# Validate required fields
		required_fields = ["service", "client"]
		for field in required_fields:
			if not kwargs.get(field):
				return {"error": f"{field.replace('_', ' ').title()} is required"}

		request = frappe.get_doc({
			"doctype": "Service Request",
			"service": kwargs.get("service"),
			"client": kwargs.get("client"),
			"description": kwargs.get("description"),
			"preferred_date": kwargs.get("preferred_date"),
			"status": "Draft",
			"request_date": getdate(),
			"source": kwargs.get("source", "Internal")
		})
		request.insert()

		return {"success": True, "request_id": request.name}
	except Exception as e:
		frappe.log_error(f"Error creating service request: {str(e)}")
		return {"error": "Failed to create request"}

@frappe.whitelist()
def approve_service_request(request_id, approved_date=None):
	"""Approve a service request"""
	try:
		request = frappe.get_doc("Service Request", request_id)
		request.status = "Approved"
		request.approved_date = approved_date or getdate()
		request.save()

		return {"success": True}
	except Exception as e:
		frappe.log_error(f"Error approving service request: {str(e)}")
		return {"error": "Failed to approve request"}

@frappe.whitelist()
def reject_service_request(request_id, rejection_reason=None):
	"""Reject a service request"""
	try:
		request = frappe.get_doc("Service Request", request_id)
		request.status = "Rejected"
		request.rejection_reason = rejection_reason
		request.save()

		return {"success": True}
	except Exception as e:
		frappe.log_error(f"Error rejecting service request: {str(e)}")
		return {"error": "Failed to reject request"}

@frappe.whitelist()
def send_hearing_reminder(hearing_id):
	"""Send hearing reminder notifications"""
	try:
		hearing = frappe.get_doc("Case Hearing", hearing_id)

		# Get case details
		case = frappe.get_doc("Legal Case", hearing.case)

		# Get assigned lawyers and staff
		assigned_users = []
		if case.lawyer:
			assigned_users.append(case.lawyer)
		if case.paralegal:
			assigned_users.append(case.paralegal)

		# Send notifications
		for user in assigned_users:
			frappe.sendmail(
				recipients=[frappe.db.get_value("User", user, "email")],
				subject=_("Hearing Reminder - {0}").format(case.case_title),
				template="hearing_reminder",
				args={
					"case": case,
					"hearing": hearing
				}
			)

		# Create notification
		frappe.get_doc({
			"doctype": "Notification Log",
			"subject": _("Hearing Reminder: {0}").format(case.case_title),
			"email_content": _("Upcoming hearing on {0} at {1}").format(
				frappe.utils.format_date(hearing.hearing_date),
				hearing.hearing_time or ""
			),
			"document_type": "Case Hearing",
			"document_name": hearing_id,
			"for_user": ",".join(assigned_users)
		}).insert()

		return {"success": True}
	except Exception as e:
		frappe.log_error(f"Error sending hearing reminder: {str(e)}")
		return {"error": "Failed to send reminder"}

# Billing Integration APIs
@frappe.whitelist()
def generate_invoice_from_time_entries(time_entries, client=None, case=None):
	"""Generate sales invoice from approved time entries"""
	try:
		if isinstance(time_entries, str):
			time_entries = json.loads(time_entries)

		# Validate time entries
		valid_entries = []
		total_amount = 0
		total_hours = 0

		for entry_id in time_entries:
			entry = frappe.get_doc("Time Entry", entry_id)

			# Check if entry is approved and billable
			if entry.status != "Approved" or not entry.is_billable:
				continue

			# Check if already invoiced
			if entry.billed:
				continue

			valid_entries.append(entry)
			total_amount += entry.billing_amount or 0
			total_hours += entry.hours or 0

		if not valid_entries:
			return {"error": "No valid billable time entries found"}

		# Determine client and case
		if not client:
			# Get client from first time entry's case
			first_entry = valid_entries[0]
			if first_entry.case:
				case_doc = frappe.get_doc("Legal Case", first_entry.case)
				client = case_doc.client

		if not client:
			return {"error": "Client not found for time entries"}

		# Create sales invoice
		invoice = frappe.get_doc({
			"doctype": "Sales Invoice",
			"customer": client,
			"posting_date": getdate(),
			"due_date": add_days(getdate(), 30),  # 30 days payment terms
			"items": []
		})

		# Add items from time entries
		for entry in valid_entries:
			# Get case title for description
			case_title = ""
			if entry.case:
				case_title = frappe.db.get_value("Legal Case", entry.case, "case_title")

			invoice.append("items", {
				"item_code": "Legal Services",  # Default item code
				"item_name": f"Legal Services - {case_title or 'General'}",
				"description": f"{entry.description}\nDate: {entry.date}\nHours: {entry.hours}",
				"qty": entry.hours,
				"rate": entry.billing_rate,
				"amount": entry.billing_amount,
				"time_entry": entry.name  # Custom field to link back
			})

		# Set taxes if applicable
		company = frappe.db.get_single_value("Global Defaults", "default_company")
		if company:
			tax_template = frappe.db.get_value("Company", company, "default_sales_tax_template")
			if tax_template:
				invoice.taxes_and_charges = tax_template

		invoice.insert()

		# Mark time entries as invoiced
		for entry in valid_entries:
			entry.billed = 1
			entry.invoice_reference = invoice.name
			entry.save()

		return {
			"success": True,
			"invoice_id": invoice.name,
			"total_amount": total_amount,
			"total_hours": total_hours
		}

	except Exception as e:
		frappe.log_error(f"Error generating invoice: {str(e)}")
		return {"error": "Failed to generate invoice"}

@frappe.whitelist()
def get_billable_time_entries(client=None, case=None, date_from=None, date_to=None):
	"""Get approved billable time entries for invoicing"""
	try:
		filters = {
			"status": "Approved",
			"is_billable": 1,
			"billed": 0,
			"docstatus": 1
		}

		if client:
			filters["client"] = client
		if case:
			filters["case"] = case

		# Date range filter
		date_condition = ""
		if date_from and date_to:
			date_condition = f" AND date BETWEEN '{date_from}' AND '{date_to}'"
		elif date_from:
			date_condition = f" AND date >= '{date_from}'"
		elif date_to:
			date_condition = f" AND date <= '{date_to}'"

		entries = frappe.db.sql(f"""
			SELECT
				te.name,
				te.employee,
				te.employee_name,
				te.case,
				lc.case_title,
				te.date,
				te.hours,
				te.billing_rate,
				te.billing_amount,
				te.description
			FROM `tabTime Entry` te
			LEFT JOIN `tabLegal Case` lc ON lc.name = te.case
			WHERE te.status = 'Approved'
				AND te.is_billable = 1
				AND te.billed = 0
				AND te.docstatus = 1
			{date_condition}
			ORDER BY te.date DESC
		""", as_dict=True)

		# Group by client/case for easier invoicing
		grouped_entries = {}
		for entry in entries:
			key = entry.case or "general"
			if key not in grouped_entries:
				grouped_entries[key] = {
					"case_title": entry.case_title or "General Services",
					"client": client,
					"entries": [],
					"total_hours": 0,
					"total_amount": 0
				}

			grouped_entries[key]["entries"].append(entry)
			grouped_entries[key]["total_hours"] += entry.hours or 0
			grouped_entries[key]["total_amount"] += entry.total_amount or 0

		return grouped_entries

	except Exception as e:
		frappe.log_error(f"Error getting billable time entries: {str(e)}")
		return {"error": "Failed to get billable time entries"}

@frappe.whitelist()
def create_trust_account_transaction(client, amount, transaction_type, description, reference=None):
	"""Create trust account transaction for client funds"""
	try:
		# Validate client
		if not frappe.db.exists("Client", client):
			return {"error": "Client not found"}

		# Create trust account transaction
		transaction = frappe.get_doc({
			"doctype": "Trust Account Transaction",
			"client": client,
			"transaction_date": getdate(),
			"transaction_type": transaction_type,
			"amount": amount,
			"description": description,
			"reference": reference
		})
		transaction.insert()
		transaction.submit()

		# Update client trust balance
		update_client_trust_balance(client)

		return {"success": True, "transaction_id": transaction.name}

	except Exception as e:
		frappe.log_error(f"Error creating trust transaction: {str(e)}")
		return {"error": "Failed to create trust transaction"}

@frappe.whitelist()
def get_client_trust_balance(client):
	"""Get client's trust account balance"""
	try:
		balance = frappe.db.sql("""
			SELECT
				SUM(CASE
					WHEN transaction_type = 'Deposit' THEN amount
					WHEN transaction_type = 'Withdrawal' THEN -amount
					WHEN transaction_type = 'Payment' THEN -amount
					ELSE 0
				END) as balance
			FROM `tabTrust Account Transaction`
			WHERE client = %s
				AND docstatus = 1
		""", (client,), as_dict=True)

		return {"balance": balance[0].balance or 0}

	except Exception as e:
		frappe.log_error(f"Error getting trust balance: {str(e)}")
		return {"error": "Failed to get trust balance"}

@frappe.whitelist()
def get_client_billing_history(client, limit=50):
	"""Get client's billing and payment history"""
	try:
		# Get sales invoices
		invoices = frappe.db.sql("""
			SELECT
				'Invoice' as type,
				name,
				posting_date as date,
				grand_total as amount,
				outstanding_amount,
				status
			FROM `tabSales Invoice`
			WHERE customer = %s
				AND docstatus = 1
			ORDER BY posting_date DESC
			LIMIT %s
		""", (client, limit), as_dict=True)

		# Get trust account transactions
		transactions = frappe.db.sql("""
			SELECT
				CONCAT('Trust ', transaction_type) as type,
				name,
				transaction_date as date,
				CASE
					WHEN transaction_type = 'Deposit' THEN amount
					WHEN transaction_type = 'Withdrawal' THEN -amount
					WHEN transaction_type = 'Payment' THEN -amount
					ELSE 0
				END as amount,
				0 as outstanding_amount,
				'Completed' as status
			FROM `tabTrust Account Transaction`
			WHERE client = %s
				AND docstatus = 1
			ORDER BY transaction_date DESC
			LIMIT %s
		""", (client, limit), as_dict=True)

		# Combine and sort
		history = invoices + transactions
		history.sort(key=lambda x: x.date, reverse=True)

		return history[:limit]

	except Exception as e:
		frappe.log_error(f"Error getting billing history: {str(e)}")
		return {"error": "Failed to get billing history"}

@frappe.whitelist()
def apply_client_payment(client, amount, payment_type, reference=None, description=None):
	"""Apply payment from client (trust account or direct payment)"""
	try:
		if payment_type == "trust_account":
			# Deduct from trust account
			balance = get_client_trust_balance(client)["balance"]
			if balance < amount:
				return {"error": "Insufficient trust account balance"}

			# Create trust withdrawal
			result = create_trust_account_transaction(
				client=client,
				amount=amount,
				transaction_type="Payment",
				description=description or f"Payment applied - {reference}",
				reference=reference
			)

			if "error" in result:
				return result

			return {"success": True, "transaction_id": result["transaction_id"]}

		elif payment_type == "direct_payment":
			# Create payment entry
			payment = frappe.get_doc({
				"doctype": "Payment Entry",
				"payment_type": "Receive",
				"party_type": "Customer",
				"party": client,
				"paid_amount": amount,
				"received_amount": amount,
				"reference_no": reference,
				"reference_date": getdate(),
				"remarks": description
			})
			payment.insert()
			payment.submit()

			return {"success": True, "payment_id": payment.name}

		else:
			return {"error": "Invalid payment type"}

	except Exception as e:
		frappe.log_error(f"Error applying payment: {str(e)}")
		return {"error": "Failed to apply payment"}

def update_client_trust_balance(client):
	"""Update client's trust account balance"""
	try:
		balance = get_client_trust_balance(client)["balance"]

		# Update client record
		frappe.db.set_value("Client", client, "trust_balance", balance)

	except Exception as e:
		frappe.log_error(f"Error updating trust balance: {str(e)}")