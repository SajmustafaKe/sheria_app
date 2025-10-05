# Sheria App Tasks Module
# Copyright (c) 2024, Coale Tech
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import now, getdate, add_days, now_datetime

def all():
	"""Run all scheduled tasks"""
	try:
		# Update case deadlines
		update_case_deadlines()

		# Send service reminders
		send_service_reminders()

		# Update case statuses
		update_case_statuses()

		# Clean up old logs
		cleanup_old_logs()

	except Exception as e:
		frappe.log_error(f"Error in all() task: {str(e)}")

def daily():
	"""Run daily scheduled tasks"""
	try:
		# Send daily case reminders
		send_daily_case_reminders()

		# Update client communication logs
		update_client_communication_logs()

		# Generate daily reports
		generate_daily_reports()

	except Exception as e:
		frappe.log_error(f"Error in daily() task: {str(e)}")

def hourly():
	"""Run hourly scheduled tasks"""
	try:
		# Check for urgent case updates
		check_urgent_case_updates()

		# Update real-time notifications
		update_realtime_notifications()

	except Exception as e:
		frappe.log_error(f"Error in hourly() task: {str(e)}")

def weekly():
	"""Run weekly scheduled tasks"""
	try:
		# Generate weekly case performance report
		generate_weekly_case_report()

		# Send weekly client updates
		send_weekly_client_updates()

		# Update lawyer performance metrics
		update_lawyer_performance_metrics()

	except Exception as e:
		frappe.log_error(f"Error in weekly() task: {str(e)}")

def monthly():
	"""Run monthly scheduled tasks"""
	try:
		# Generate monthly firm performance report
		generate_monthly_firm_report()

		# Update case statistics
		update_case_statistics()

		# Send monthly client newsletters
		send_monthly_client_newsletters()

		# Archive old cases
		archive_old_cases()

	except Exception as e:
		frappe.log_error(f"Error in monthly() task: {str(e)}")

def update_case_deadlines():
	"""Update case deadlines and send notifications"""
	try:
		# Get cases with upcoming deadlines
		upcoming_deadlines = frappe.db.sql("""
			SELECT name, case_title, deadline_date, client_name, assigned_lawyer
			FROM `tabLegal Case`
			WHERE deadline_date IS NOT NULL
				AND deadline_date >= %s
				AND deadline_date <= %s
				AND status IN ('Active', 'Pending')
				AND docstatus = 1
		""", (getdate(), add_days(getdate(), 7)), as_dict=True)

		for case in upcoming_deadlines:
			days_remaining = (case.deadline_date - getdate()).days

			# Send reminder based on days remaining
			if days_remaining <= 1:
				send_deadline_reminder(case, "urgent")
			elif days_remaining <= 3:
				send_deadline_reminder(case, "warning")
			else:
				send_deadline_reminder(case, "info")

	except Exception as e:
		frappe.log_error(f"Error updating case deadlines: {str(e)}")

def send_service_reminders():
	"""Send reminders for pending service requests"""
	try:
		# Get pending service requests older than 3 days
		pending_requests = frappe.db.sql("""
			SELECT name, service, client, request_date, preferred_date
			FROM `tabService Request`
			WHERE status = 'Submitted'
				AND DATE(request_date) <= %s
				AND docstatus = 1
		""", (add_days(getdate(), -3),), as_dict=True)

		for request in pending_requests:
			send_service_request_reminder(request)

	except Exception as e:
		frappe.log_error(f"Error sending service reminders: {str(e)}")

def update_case_statuses():
	"""Update case statuses based on current date and activities"""
	try:
		# Auto-close cases that have been resolved
		resolved_cases = frappe.db.sql("""
			SELECT name
			FROM `tabLegal Case`
			WHERE status = 'Resolved'
				AND resolution_date IS NOT NULL
				AND resolution_date <= %s
				AND docstatus = 1
		""", (add_days(getdate(), -30),), as_dict=True)

		for case in resolved_cases:
			case_doc = frappe.get_doc("Legal Case", case.name)
			case_doc.status = "Closed"
			case_doc.save()

		# Update overdue cases
		overdue_cases = frappe.db.sql("""
			SELECT name
			FROM `tabLegal Case`
			WHERE deadline_date < %s
				AND status IN ('Active', 'Pending')
				AND docstatus = 1
		""", (getdate(),), as_dict=True)

		for case in overdue_cases:
			case_doc = frappe.get_doc("Legal Case", case.name)
			case_doc.status = "Overdue"
			case_doc.save()

	except Exception as e:
		frappe.log_error(f"Error updating case statuses: {str(e)}")

def cleanup_old_logs():
	"""Clean up old system logs"""
	try:
		# Delete logs older than 90 days
		frappe.db.sql("""
			DELETE FROM `tabError Log`
			WHERE creation < %s
		""", (add_days(getdate(), -90),))

		frappe.db.sql("""
			DELETE FROM `tabActivity Log`
			WHERE creation < %s
		""", (add_days(getdate(), -90),))

	except Exception as e:
		frappe.log_error(f"Error cleaning up logs: {str(e)}")

def send_daily_case_reminders():
	"""Send daily case reminders to lawyers"""
	try:
		# Get lawyers with active cases
		lawyers = frappe.db.sql("""
			SELECT DISTINCT assigned_lawyer
			FROM `tabLegal Case`
			WHERE assigned_lawyer IS NOT NULL
				AND status IN ('Active', 'Pending')
				AND docstatus = 1
		""", as_dict=True)

		for lawyer in lawyers:
			send_lawyer_daily_reminder(lawyer.assigned_lawyer)

	except Exception as e:
		frappe.log_error(f"Error sending daily case reminders: {str(e)}")

def update_client_communication_logs():
	"""Update client communication logs"""
	try:
		# Log communications from the past day
		yesterday = add_days(getdate(), -1)

		communications = frappe.db.sql("""
			SELECT COUNT(*) as count
			FROM `tabCommunication`
			WHERE communication_date = %s
				AND reference_doctype IN ('Legal Case', 'Service Request')
		""", (yesterday,), as_dict=True)

		if communications[0].count > 0:
			# Create communication log entry
			log = frappe.get_doc({
				"doctype": "Communication Log",
				"log_date": yesterday,
				"communications_count": communications[0].count,
				"log_type": "Daily Summary"
			})
			log.insert()

	except Exception as e:
		frappe.log_error(f"Error updating communication logs: {str(e)}")

def generate_daily_reports():
	"""Generate daily reports"""
	try:
		# Generate case activity report
		case_activities = frappe.db.sql("""
			SELECT
				COUNT(*) as total_activities,
				COUNT(DISTINCT case) as cases_with_activity
			FROM `tabCase Activity`
			WHERE DATE(creation) = %s
				AND docstatus = 1
		""", (getdate(),), as_dict=True)

		if case_activities[0].total_activities > 0:
			report = frappe.get_doc({
				"doctype": "Daily Report",
				"report_date": getdate(),
				"report_type": "Case Activity",
				"total_activities": case_activities[0].total_activities,
				"cases_with_activity": case_activities[0].cases_with_activity
			})
			report.insert()

	except Exception as e:
		frappe.log_error(f"Error generating daily reports: {str(e)}")

def check_urgent_case_updates():
	"""Check for urgent case updates"""
	try:
		# Check for cases that need immediate attention
		urgent_cases = frappe.db.sql("""
			SELECT name, case_title, priority, status
			FROM `tabLegal Case`
			WHERE priority = 'High'
				AND status IN ('Active', 'Pending')
				AND (
					deadline_date <= %s
					OR last_activity_date <= %s
				)
				AND docstatus = 1
		""", (add_days(getdate(), 1), add_days(getdate(), -3)), as_dict=True)

		for case in urgent_cases:
			send_urgent_case_notification(case)

	except Exception as e:
		frappe.log_error(f"Error checking urgent case updates: {str(e)}")

def update_realtime_notifications():
	"""Update real-time notifications"""
	try:
		# Clear old notifications
		frappe.db.sql("""
			DELETE FROM `tabNotification Log`
			WHERE creation < %s
		""", (add_days(getdate(), -7),))

	except Exception as e:
		frappe.log_error(f"Error updating notifications: {str(e)}")

def generate_weekly_case_report():
	"""Generate weekly case performance report"""
	try:
		# Calculate weekly statistics
		week_start = add_days(getdate(), -7)

		stats = frappe.db.sql("""
			SELECT
				COUNT(CASE WHEN status = 'Closed' THEN 1 END) as cases_closed,
				COUNT(CASE WHEN status = 'Active' THEN 1 END) as active_cases,
				COUNT(CASE WHEN creation >= %s THEN 1 END) as new_cases,
				AVG(CASE WHEN resolution_date IS NOT NULL THEN DATEDIFF(resolution_date, creation) END) as avg_resolution_days
			FROM `tabLegal Case`
			WHERE docstatus = 1
		""", (week_start,), as_dict=True)[0]

		# Create weekly report
		report = frappe.get_doc({
			"doctype": "Weekly Case Report",
			"week_start_date": week_start,
			"week_end_date": getdate(),
			"cases_closed": stats.cases_closed or 0,
			"active_cases": stats.active_cases or 0,
			"new_cases": stats.new_cases or 0,
			"avg_resolution_days": stats.avg_resolution_days or 0
		})
		report.insert()

	except Exception as e:
		frappe.log_error(f"Error generating weekly case report: {str(e)}")

def send_weekly_client_updates():
	"""Send weekly updates to clients"""
	try:
		# Get clients with active cases
		clients = frappe.db.sql("""
			SELECT DISTINCT lc.client, lc.client_name, lc.client_email
			FROM `tabLegal Case` lc
			WHERE lc.status IN ('Active', 'Pending')
				AND lc.client_email IS NOT NULL
				AND lc.docstatus = 1
		""", as_dict=True)

		for client in clients:
			send_client_weekly_update(client)

	except Exception as e:
		frappe.log_error(f"Error sending weekly client updates: {str(e)}")

def update_lawyer_performance_metrics():
	"""Update lawyer performance metrics"""
	try:
		# Get all lawyers
		lawyers = frappe.db.sql("""
			SELECT name, lawyer_name
			FROM `tabLawyer`
			WHERE docstatus = 1
		""", as_dict=True)

		for lawyer in lawyers:
			metrics = calculate_lawyer_metrics(lawyer.name)

			# Update or create performance record
			existing = frappe.db.exists("Lawyer Performance", {
				"lawyer": lawyer.name,
				"month": getdate().strftime("%Y-%m")
			})

			if existing:
				doc = frappe.get_doc("Lawyer Performance", existing)
			else:
				doc = frappe.get_doc({
					"doctype": "Lawyer Performance",
					"lawyer": lawyer.name,
					"month": getdate().strftime("%Y-%m")
				})

			doc.update(metrics)
			doc.save()

	except Exception as e:
		frappe.log_error(f"Error updating lawyer performance: {str(e)}")

def generate_monthly_firm_report():
	"""Generate monthly firm performance report"""
	try:
		# Calculate monthly statistics
		month_start = getdate().replace(day=1)

		stats = frappe.db.sql("""
			SELECT
				COUNT(*) as total_cases,
				SUM(CASE WHEN status = 'Closed' THEN 1 ELSE 0 END) as closed_cases,
				SUM(CASE WHEN status = 'Active' THEN 1 ELSE 0 END) as active_cases,
				SUM(CASE WHEN creation >= %s THEN 1 ELSE 0 END) as new_cases,
				AVG(CASE WHEN resolution_date IS NOT NULL THEN DATEDIFF(resolution_date, creation) END) as avg_resolution_time,
				SUM(total_fees) as total_revenue
			FROM `tabLegal Case`
			WHERE docstatus = 1
		""", (month_start,), as_dict=True)[0]

		# Create monthly report
		report = frappe.get_doc({
			"doctype": "Monthly Firm Report",
			"month": getdate().strftime("%Y-%m"),
			"total_cases": stats.total_cases or 0,
			"closed_cases": stats.closed_cases or 0,
			"active_cases": stats.active_cases or 0,
			"new_cases": stats.new_cases or 0,
			"avg_resolution_time": stats.avg_resolution_time or 0,
			"total_revenue": stats.total_revenue or 0
		})
		report.insert()

	except Exception as e:
		frappe.log_error(f"Error generating monthly firm report: {str(e)}")

def update_case_statistics():
	"""Update overall case statistics"""
	try:
		# Calculate comprehensive statistics
		stats = frappe.db.sql("""
			SELECT
				COUNT(*) as total_cases,
				SUM(CASE WHEN status = 'Active' THEN 1 ELSE 0 END) as active_cases,
				SUM(CASE WHEN status = 'Closed' THEN 1 ELSE 0 END) as closed_cases,
				SUM(CASE WHEN status = 'Pending' THEN 1 ELSE 0 END) as pending_cases,
				SUM(CASE WHEN priority = 'High' THEN 1 ELSE 0 END) as high_priority_cases,
				AVG(CASE WHEN resolution_date IS NOT NULL THEN DATEDIFF(resolution_date, creation) END) as avg_resolution_days
			FROM `tabLegal Case`
			WHERE docstatus = 1
		""", as_dict=True)[0]

		# Update global statistics
		if frappe.db.exists("Case Statistics"):
			doc = frappe.get_doc("Case Statistics", "Case Statistics")
		else:
			doc = frappe.get_doc({
				"doctype": "Case Statistics",
				"name": "Case Statistics"
			})

		doc.update({
			"total_cases": stats.total_cases or 0,
			"active_cases": stats.active_cases or 0,
			"closed_cases": stats.closed_cases or 0,
			"pending_cases": stats.pending_cases or 0,
			"high_priority_cases": stats.high_priority_cases or 0,
			"avg_resolution_days": stats.avg_resolution_days or 0,
			"last_updated": now()
		})
		doc.save()

	except Exception as e:
		frappe.log_error(f"Error updating case statistics: {str(e)}")

def send_monthly_client_newsletters():
	"""Send monthly newsletters to clients"""
	try:
		# Get all active clients
		clients = frappe.db.sql("""
			SELECT DISTINCT client, client_name, client_email
			FROM `tabLegal Case`
			WHERE client_email IS NOT NULL
				AND status IN ('Active', 'Closed')
				AND docstatus = 1
		""", as_dict=True)

		for client in clients:
			send_client_newsletter(client)

	except Exception as e:
		frappe.log_error(f"Error sending monthly newsletters: {str(e)}")

def archive_old_cases():
	"""Archive old closed cases"""
	try:
		# Archive cases closed more than 2 years ago
		old_cases = frappe.db.sql("""
			SELECT name
			FROM `tabLegal Case`
			WHERE status = 'Closed'
				AND resolution_date <= %s
				AND archived = 0
				AND docstatus = 1
		""", (add_days(getdate(), -730),), as_dict=True)

		for case in old_cases:
			case_doc = frappe.get_doc("Legal Case", case.name)
			case_doc.archived = 1
			case_doc.save()

	except Exception as e:
		frappe.log_error(f"Error archiving old cases: {str(e)}")

# Helper functions

def send_deadline_reminder(case, priority):
	"""Send deadline reminder"""
	try:
		subject = f"Case Deadline Reminder: {case.case_title}"
		message = frappe.render_template("sheria/templates/emails/deadline_reminder.html", {
			"case": case,
			"priority": priority
		})

		recipients = []
		if case.assigned_lawyer:
			lawyer_email = frappe.db.get_value("Lawyer", case.assigned_lawyer, "email")
			if lawyer_email:
				recipients.append(lawyer_email)

		if recipients:
			frappe.sendmail(
				recipients=recipients,
				subject=subject,
				message=message
			)

	except Exception as e:
		frappe.log_error(f"Error sending deadline reminder: {str(e)}")

def send_service_request_reminder(request):
	"""Send service request reminder"""
	try:
		subject = f"Service Request Reminder - {request.name}"
		message = frappe.render_template("sheria/templates/emails/service_reminder.html", {
			"request": request
		})

		client_email = frappe.db.get_value("Client", request.client, "email")
		if client_email:
			frappe.sendmail(
				recipients=[client_email],
				subject=subject,
				message=message
			)

	except Exception as e:
		frappe.log_error(f"Error sending service reminder: {str(e)}")

def send_lawyer_daily_reminder(lawyer):
	"""Send daily reminder to lawyer"""
	try:
		# Get lawyer's active cases
		cases = frappe.db.sql("""
			SELECT name, case_title, deadline_date, status
			FROM `tabLegal Case`
			WHERE assigned_lawyer = %s
				AND status IN ('Active', 'Pending')
				AND docstatus = 1
			ORDER BY deadline_date
			LIMIT 5
		""", (lawyer,), as_dict=True)

		if cases:
			subject = "Daily Case Reminder"
			message = frappe.render_template("sheria/templates/emails/daily_lawyer_reminder.html", {
				"lawyer": lawyer,
				"cases": cases
			})

			lawyer_email = frappe.db.get_value("Lawyer", lawyer, "email")
			if lawyer_email:
				frappe.sendmail(
					recipients=[lawyer_email],
					subject=subject,
					message=message
				)

	except Exception as e:
		frappe.log_error(f"Error sending lawyer reminder: {str(e)}")

def send_urgent_case_notification(case):
	"""Send urgent case notification"""
	try:
		subject = f"URGENT: Case Requires Attention - {case.case_title}"
		message = frappe.render_template("sheria/templates/emails/urgent_case_notification.html", {
			"case": case
		})

		# Send to assigned lawyer and legal admin
		recipients = []

		if case.assigned_lawyer:
			lawyer_email = frappe.db.get_value("Lawyer", case.assigned_lawyer, "email")
			if lawyer_email:
				recipients.append(lawyer_email)

		# Send to legal admins
		admins = frappe.db.sql("""
			SELECT DISTINCT u.email
			FROM `tabUser` u
			JOIN `tabHas Role` hr ON hr.parent = u.name
			WHERE hr.role = 'Legal Admin'
				AND u.enabled = 1
		""", as_dict=True)

		for admin in admins:
			if admin.email:
				recipients.append(admin.email)

		if recipients:
			frappe.sendmail(
				recipients=recipients,
				subject=subject,
				message=message
			)

	except Exception as e:
		frappe.log_error(f"Error sending urgent notification: {str(e)}")

def send_client_weekly_update(client):
	"""Send weekly update to client"""
	try:
		# Get client's active cases
		cases = frappe.db.sql("""
			SELECT name, case_title, status, last_updated
			FROM `tabLegal Case`
			WHERE client = %s
				AND status IN ('Active', 'Pending')
				AND docstatus = 1
		""", (client.client,), as_dict=True)

		if cases:
			subject = "Weekly Case Update"
			message = frappe.render_template("sheria/templates/emails/weekly_client_update.html", {
				"client": client,
				"cases": cases
			})

			frappe.sendmail(
				recipients=[client.client_email],
				subject=subject,
				message=message
			)

	except Exception as e:
		frappe.log_error(f"Error sending client update: {str(e)}")

def calculate_lawyer_metrics(lawyer):
	"""Calculate performance metrics for a lawyer"""
	try:
		metrics = frappe.db.sql("""
			SELECT
				COUNT(*) as total_cases,
				SUM(CASE WHEN status = 'Closed' THEN 1 ELSE 0 END) as closed_cases,
				SUM(CASE WHEN status = 'Active' THEN 1 ELSE 0 END) as active_cases,
				AVG(CASE WHEN resolution_date IS NOT NULL THEN DATEDIFF(resolution_date, creation) END) as avg_resolution_days,
				SUM(total_fees) as total_fees
			FROM `tabLegal Case`
			WHERE assigned_lawyer = %s
				AND docstatus = 1
				AND MONTH(creation) = MONTH(CURRENT_DATE())
				AND YEAR(creation) = YEAR(CURRENT_DATE())
		""", (lawyer,), as_dict=True)[0]

		return {
			"total_cases": metrics.total_cases or 0,
			"closed_cases": metrics.closed_cases or 0,
			"active_cases": metrics.active_cases or 0,
			"avg_resolution_days": metrics.avg_resolution_days or 0,
			"total_fees": metrics.total_fees or 0,
			"win_rate": (metrics.closed_cases / metrics.total_cases * 100) if metrics.total_cases > 0 else 0
		}

	except Exception as e:
		frappe.log_error(f"Error calculating lawyer metrics: {str(e)}")
		return {}

def send_client_newsletter(client):
	"""Send monthly newsletter to client"""
	try:
		subject = "Monthly Legal Update from Sheria"
		message = frappe.render_template("sheria/templates/emails/monthly_newsletter.html", {
			"client": client
		})

		frappe.sendmail(
			recipients=[client.client_email],
			subject=subject,
			message=message
		)

	except Exception as e:
		frappe.log_error(f"Error sending newsletter: {str(e)}")