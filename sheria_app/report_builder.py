# Sheria Report Builder Module
# Copyright (c) 2024, Sheria Legal Technologies
# For license information, please see license.txt

import frappe
from frappe import _

def get_custom_reports():
	"""Get custom report configurations for Sheria app"""
	return {
		"case_summary_report": {
			"name": "Case Summary Report",
			"report_type": "Report Builder",
			"ref_doctype": "Legal Case",
			"filters": get_case_summary_filters(),
			"columns": get_case_summary_columns(),
			"is_standard": "Yes"
		},
		"client_portfolio_report": {
			"name": "Client Portfolio Report",
			"report_type": "Report Builder",
			"ref_doctype": "Legal CRM Lead",
			"filters": get_client_portfolio_filters(),
			"columns": get_client_portfolio_columns(),
			"is_standard": "Yes"
		},
		"lawyer_performance_report": {
			"name": "Lawyer Performance Report",
			"report_type": "Report Builder",
			"ref_doctype": "Lawyer",
			"filters": get_lawyer_performance_filters(),
			"columns": get_lawyer_performance_columns(),
			"is_standard": "Yes"
		},
		"service_request_report": {
			"name": "Service Request Report",
			"report_type": "Report Builder",
			"ref_doctype": "Service Request",
			"filters": get_service_request_filters(),
			"columns": get_service_request_columns(),
			"is_standard": "Yes"
		},
		"financial_summary_report": {
			"name": "Financial Summary Report",
			"report_type": "Report Builder",
			"ref_doctype": "Legal Service",
			"filters": get_financial_summary_filters(),
			"columns": get_financial_summary_columns(),
			"is_standard": "Yes"
		},
		"hearing_schedule_report": {
			"name": "Hearing Schedule Report",
			"report_type": "Report Builder",
			"ref_doctype": "Case Hearing",
			"filters": get_hearing_schedule_filters(),
			"columns": get_hearing_schedule_columns(),
			"is_standard": "Yes"
		}
	}

def get_case_summary_filters():
	"""Get filters for case summary report"""
	return [
		{
			"fieldname": "status",
			"label": _("Status"),
			"fieldtype": "Select",
			"options": "\nActive\nPending\nClosed\nOn Hold"
		},
		{
			"fieldname": "priority",
			"label": _("Priority"),
			"fieldtype": "Select",
			"options": "\nLow\nMedium\nHigh\nUrgent"
		},
		{
			"fieldname": "practice_area",
			"label": _("Practice Area"),
			"fieldtype": "Link",
			"options": "Practice Area"
		},
		{
			"fieldname": "assigned_lawyer",
			"label": _("Assigned Lawyer"),
			"fieldtype": "Link",
			"options": "Lawyer"
		},
		{
			"fieldname": "client",
			"label": _("Client"),
			"fieldtype": "Link",
			"options": "Customer"
		},
		{
			"fieldname": "filing_date",
			"label": _("Filing Date From"),
			"fieldtype": "Date"
		},
		{
			"fieldname": "filing_date_to",
			"label": _("Filing Date To"),
			"fieldtype": "Date"
		}
	]

def get_case_summary_columns():
	"""Get columns for case summary report"""
	return [
		{
			"fieldname": "name",
			"label": _("Case Number"),
			"fieldtype": "Link",
			"options": "Legal Case",
			"width": 120
		},
		{
			"fieldname": "client_name",
			"label": _("Client"),
			"fieldtype": "Data",
			"width": 150
		},
		{
			"fieldname": "case_type",
			"label": _("Case Type"),
			"fieldtype": "Data",
			"width": 120
		},
		{
			"fieldname": "status",
			"label": _("Status"),
			"fieldtype": "Data",
			"width": 100
		},
		{
			"fieldname": "priority",
			"label": _("Priority"),
			"fieldtype": "Data",
			"width": 80
		},
		{
			"fieldname": "assigned_lawyer_name",
			"label": _("Assigned Lawyer"),
			"fieldtype": "Data",
			"width": 150
		},
		{
			"fieldname": "practice_area",
			"label": _("Practice Area"),
			"fieldtype": "Data",
			"width": 120
		},
		{
			"fieldname": "filing_date",
			"label": _("Filing Date"),
			"fieldtype": "Date",
			"width": 100
		},
		{
			"fieldname": "deadline_date",
			"label": _("Deadline"),
			"fieldtype": "Date",
			"width": 100
		},
		{
			"fieldname": "estimated_value",
			"label": _("Estimated Value"),
			"fieldtype": "Currency",
			"width": 120
		}
	]

def get_client_portfolio_filters():
	"""Get filters for client portfolio report"""
	return [
		{
			"fieldname": "client_type",
			"label": _("Client Type"),
			"fieldtype": "Select",
			"options": "\nIndividual\nCompany\nOrganization"
		},
		{
			"fieldname": "status",
			"label": _("Status"),
			"fieldtype": "Select",
			"options": "\nActive\nInactive\nSuspended"
		},
		{
			"fieldname": "registration_date",
			"label": _("Registration From"),
			"fieldtype": "Date"
		},
		{
			"fieldname": "registration_date_to",
			"label": _("Registration To"),
			"fieldtype": "Date"
		}
	]

def get_client_portfolio_columns():
	"""Get columns for client portfolio report"""
	return [
		{
			"fieldname": "name",
			"label": _("Lead ID"),
			"fieldtype": "Link",
			"options": "Legal CRM Lead",
			"width": 100
		},
		{
			"fieldname": "lead_name",
			"label": _("Client Name"),
			"fieldtype": "Data",
			"width": 150
		},
		{
			"fieldname": "client_type",
			"label": _("Type"),
			"fieldtype": "Data",
			"width": 100
		},
		{
			"fieldname": "email",
			"label": _("Email"),
			"fieldtype": "Data",
			"width": 150
		},
		{
			"fieldname": "phone",
			"label": _("Phone"),
			"fieldtype": "Data",
			"width": 120
		},
		{
			"fieldname": "status",
			"label": _("Status"),
			"fieldtype": "Data",
			"width": 80
		},
		{
			"fieldname": "registration_date",
			"label": _("Registration Date"),
			"fieldtype": "Date",
			"width": 120
		},
		{
			"fieldname": "total_cases",
			"label": _("Total Cases"),
			"fieldtype": "Int",
			"width": 100
		},
		{
			"fieldname": "active_cases",
			"label": _("Active Cases"),
			"fieldtype": "Int",
			"width": 100
		},
		{
			"fieldname": "total_revenue",
			"label": _("Total Revenue"),
			"fieldtype": "Currency",
			"width": 120
		}
	]

def get_lawyer_performance_filters():
	"""Get filters for lawyer performance report"""
	return [
		{
			"fieldname": "status",
			"label": _("Status"),
			"fieldtype": "Select",
			"options": "\nActive\nInactive\nOn Leave"
		},
		{
			"fieldname": "practice_areas",
			"label": _("Practice Areas"),
			"fieldtype": "Data"
		},
		{
			"fieldname": "joining_date",
			"label": _("Joining From"),
			"fieldtype": "Date"
		},
		{
			"fieldname": "joining_date_to",
			"label": _("Joining To"),
			"fieldtype": "Date"
		}
	]

def get_lawyer_performance_columns():
	"""Get columns for lawyer performance report"""
	return [
		{
			"fieldname": "name",
			"label": _("Lawyer ID"),
			"fieldtype": "Link",
			"options": "Lawyer",
			"width": 100
		},
		{
			"fieldname": "lawyer_name",
			"label": _("Lawyer Name"),
			"fieldtype": "Data",
			"width": 150
		},
		{
			"fieldname": "status",
			"label": _("Status"),
			"fieldtype": "Data",
			"width": 80
		},
		{
			"fieldname": "practice_areas",
			"label": _("Practice Areas"),
			"fieldtype": "Data",
			"width": 150
		},
		{
			"fieldname": "years_of_experience",
			"label": _("Experience (Years)"),
			"fieldtype": "Int",
			"width": 120
		},
		{
			"fieldname": "joining_date",
			"label": _("Joining Date"),
			"fieldtype": "Date",
			"width": 100
		},
		{
			"fieldname": "total_cases",
			"label": _("Total Cases"),
			"fieldtype": "Int",
			"width": 100
		},
		{
			"fieldname": "active_cases",
			"label": _("Active Cases"),
			"width": 100
		},
		{
			"fieldname": "won_cases",
			"label": _("Won Cases"),
			"fieldtype": "Int",
			"width": 100
		},
		{
			"fieldname": "success_rate",
			"label": _("Success Rate (%)"),
			"fieldtype": "Percent",
			"width": 120
		},
		{
			"fieldname": "total_revenue",
			"label": _("Revenue Generated"),
			"fieldtype": "Currency",
			"width": 130
		}
	]

def get_service_request_filters():
	"""Get filters for service request report"""
	return [
		{
			"fieldname": "status",
			"label": _("Status"),
			"fieldtype": "Select",
			"options": "\nSubmitted\nIn Progress\nApproved\nCompleted\nRejected"
		},
		{
			"fieldname": "priority",
			"label": _("Priority"),
			"fieldtype": "Select",
			"options": "\nLow\nMedium\nHigh\nUrgent"
		},
		{
			"fieldname": "service_type",
			"label": _("Service Type"),
			"fieldtype": "Select",
			"options": "\nLegal Consultation\nDocument Review\nContract Drafting\nCase Filing\nLegal Research\nOther"
		},
		{
			"fieldname": "request_date",
			"label": _("Request From"),
			"fieldtype": "Date"
		},
		{
			"fieldname": "request_date_to",
			"label": _("Request To"),
			"fieldtype": "Date"
		}
	]

def get_service_request_columns():
	"""Get columns for service request report"""
	return [
		{
			"fieldname": "name",
			"label": _("Request ID"),
			"fieldtype": "Link",
			"options": "Service Request",
			"width": 120
		},
		{
			"fieldname": "client_name",
			"label": _("Client Name"),
			"fieldtype": "Data",
			"width": 150
		},
		{
			"fieldname": "email",
			"label": _("Email"),
			"fieldtype": "Data",
			"width": 150
		},
		{
			"fieldname": "service_type",
			"label": _("Service Type"),
			"fieldtype": "Data",
			"width": 130
		},
		{
			"fieldname": "status",
			"label": _("Status"),
			"fieldtype": "Data",
			"width": 100
		},
		{
			"fieldname": "priority",
			"label": _("Priority"),
			"fieldtype": "Data",
			"width": 80
		},
		{
			"fieldname": "request_date",
			"label": _("Request Date"),
			"fieldtype": "Date",
			"width": 100
		},
		{
			"fieldname": "assigned_to_name",
			"label": _("Assigned To"),
			"fieldtype": "Data",
			"width": 120
		},
		{
			"fieldname": "due_date",
			"label": _("Due Date"),
			"fieldtype": "Date",
			"width": 100
		},
		{
			"fieldname": "completion_date",
			"label": _("Completion Date"),
			"fieldtype": "Date",
			"width": 120
		}
	]

def get_financial_summary_filters():
	"""Get filters for financial summary report"""
	return [
		{
			"fieldname": "status",
			"label": _("Status"),
			"fieldtype": "Select",
			"options": "\nDraft\nSubmitted\nPaid\nOverdue\nCancelled"
		},
		{
			"fieldname": "service_type",
			"label": _("Service Type"),
			"fieldtype": "Select",
			"options": "\nLegal Consultation\nDocument Review\nContract Drafting\nCase Representation\nLegal Research\nOther"
		},
		{
			"fieldname": "client",
			"label": _("Client"),
			"fieldtype": "Link",
			"options": "Customer"
		},
		{
			"fieldname": "invoice_date",
			"label": _("Invoice From"),
			"fieldtype": "Date"
		},
		{
			"fieldname": "invoice_date_to",
			"label": _("Invoice To"),
			"fieldtype": "Date"
		}
	]

def get_financial_summary_columns():
	"""Get columns for financial summary report"""
	return [
		{
			"fieldname": "name",
			"label": _("Service ID"),
			"fieldtype": "Link",
			"options": "Legal Service",
			"width": 120
		},
		{
			"fieldname": "client_name",
			"label": _("Client"),
			"fieldtype": "Data",
			"width": 150
		},
		{
			"fieldname": "service_type",
			"label": _("Service Type"),
			"fieldtype": "Data",
			"width": 130
		},
		{
			"fieldname": "status",
			"label": _("Status"),
			"fieldtype": "Data",
			"width": 100
		},
		{
			"fieldname": "invoice_date",
			"label": _("Invoice Date"),
			"fieldtype": "Date",
			"width": 100
		},
		{
			"fieldname": "due_date",
			"label": _("Due Date"),
			"fieldtype": "Date",
			"width": 100
		},
		{
			"fieldname": "total_amount",
			"label": _("Total Amount"),
			"fieldtype": "Currency",
			"width": 120
		},
		{
			"fieldname": "paid_amount",
			"label": _("Paid Amount"),
			"fieldtype": "Currency",
			"width": 120
		},
		{
			"fieldname": "outstanding_amount",
			"label": _("Outstanding"),
			"fieldtype": "Currency",
			"width": 120
		},
		{
			"fieldname": "payment_status",
			"label": _("Payment Status"),
			"fieldtype": "Data",
			"width": 120
		}
	]

def get_hearing_schedule_filters():
	"""Get filters for hearing schedule report"""
	return [
		{
			"fieldname": "status",
			"label": _("Status"),
			"fieldtype": "Select",
			"options": "\nScheduled\nCompleted\nPostponed\nCancelled"
		},
		{
			"fieldname": "hearing_type",
			"label": _("Hearing Type"),
			"fieldtype": "Select",
			"options": "\nInitial Hearing\nPre-Trial\nTrial\nAppeal\nOther"
		},
		{
			"fieldname": "court",
			"label": _("Court"),
			"fieldtype": "Link",
			"options": "Court"
		},
		{
			"fieldname": "hearing_date",
			"label": _("Hearing From"),
			"fieldtype": "Date"
		},
		{
			"fieldname": "hearing_date_to",
			"label": _("Hearing To"),
			"fieldtype": "Date"
		}
	]

def get_hearing_schedule_columns():
	"""Get columns for hearing schedule report"""
	return [
		{
			"fieldname": "name",
			"label": _("Hearing ID"),
			"fieldtype": "Link",
			"options": "Case Hearing",
			"width": 120
		},
		{
			"fieldname": "case_name",
			"label": _("Case Number"),
			"fieldtype": "Data",
			"width": 120
		},
		{
			"fieldname": "client_name",
			"label": _("Client"),
			"fieldtype": "Data",
			"width": 150
		},
		{
			"fieldname": "court_name",
			"label": _("Court"),
			"fieldtype": "Data",
			"width": 120
		},
		{
			"fieldname": "hearing_date",
			"label": _("Hearing Date"),
			"fieldtype": "Date",
			"width": 100
		},
		{
			"fieldname": "hearing_time",
			"label": _("Time"),
			"fieldtype": "Data",
			"width": 80
		},
		{
			"fieldname": "hearing_type",
			"label": _("Type"),
			"fieldtype": "Data",
			"width": 100
		},
		{
			"fieldname": "judge_name",
			"label": _("Judge"),
			"fieldtype": "Data",
			"width": 120
		},
		{
			"fieldname": "status",
			"label": _("Status"),
			"fieldtype": "Data",
			"width": 100
		},
		{
			"fieldname": "outcome",
			"label": _("Outcome"),
			"fieldtype": "Data",
			"width": 120
		}
	]

def create_default_reports():
	"""Create default custom reports for Sheria app"""
	try:
		reports = get_custom_reports()

		for report_key, report_data in reports.items():
			if not frappe.db.exists("Report", report_data["name"]):
				report = frappe.get_doc({
					"doctype": "Report",
					"name": report_data["name"],
					"report_type": report_data["report_type"],
					"ref_doctype": report_data["ref_doctype"],
					"is_standard": report_data["is_standard"]
				})

				# Add filters
				for filter_item in report_data["filters"]:
					report.append("filters", filter_item)

				# Add columns
				for column in report_data["columns"]:
					report.append("columns", column)

				report.insert(ignore_permissions=True)
				frappe.db.commit()

	except Exception as e:
		frappe.log_error(f"Error creating custom reports: {str(e)}")

# Custom report query functions

def get_case_summary_data(filters=None):
	"""Get data for case summary report"""
	if not filters:
		filters = {}

	conditions = []
	values = []

	# Build conditions based on filters
	if filters.get("status"):
		conditions.append("lc.status = %s")
		values.append(filters["status"])

	if filters.get("priority"):
		conditions.append("lc.priority = %s")
		values.append(filters["priority"])

	if filters.get("practice_area"):
		conditions.append("lc.practice_area = %s")
		values.append(filters["practice_area"])

	if filters.get("assigned_lawyer"):
		conditions.append("lc.assigned_lawyer = %s")
		values.append(filters["assigned_lawyer"])

	if filters.get("client"):
		conditions.append("lc.client = %s")
		values.append(filters["client"])

	if filters.get("filing_date"):
		conditions.append("lc.filing_date >= %s")
		values.append(filters["filing_date"])

	if filters.get("filing_date_to"):
		conditions.append("lc.filing_date <= %s")
		values.append(filters["filing_date_to"])

	where_clause = " AND ".join(conditions) if conditions else "1=1"

	query = f"""
		SELECT
			lc.name,
			lc.client_name,
			lc.case_type,
			lc.status,
			lc.priority,
			lc.assigned_lawyer_name,
			lc.practice_area,
			lc.filing_date,
			lc.deadline_date,
			lc.estimated_value
		FROM `tabLegal Case` lc
		WHERE {where_clause}
		ORDER BY lc.filing_date DESC
	"""

	return frappe.db.sql(query, values, as_dict=True)

def get_client_portfolio_data(filters=None):
	"""Get data for client portfolio report"""
	if not filters:
		filters = {}

	conditions = []
	values = []

	# Build conditions based on filters
	if filters.get("client_type"):
		conditions.append("c.client_type = %s")
		values.append(filters["client_type"])

	if filters.get("status"):
		conditions.append("c.status = %s")
		values.append(filters["status"])

	if filters.get("registration_date"):
		conditions.append("c.registration_date >= %s")
		values.append(filters["registration_date"])

	if filters.get("registration_date_to"):
		conditions.append("c.registration_date <= %s")
		values.append(filters["registration_date_to"])

	where_clause = " AND ".join(conditions) if conditions else "1=1"

	query = f"""
		SELECT
			c.name,
			c.lead_name as client_name,
			c.client_type,
			c.email,
			c.phone,
			c.status,
			c.creation as registration_date,
			COUNT(DISTINCT lc.name) as total_cases,
			COUNT(DISTINCT CASE WHEN lc.status IN ('Active', 'Pending') THEN lc.name END) as active_cases,
			COALESCE(SUM(d.deal_amount), 0) as total_revenue
		FROM `tabLegal CRM Lead` c
		LEFT JOIN `tabLegal Case` lc ON lc.client = c.name
		LEFT JOIN `tabLegal CRM Deal` d ON d.lead = c.name AND d.status = 'Won'
		WHERE {where_clause}
		GROUP BY c.name
		ORDER BY c.creation DESC
	"""

	return frappe.db.sql(query, values, as_dict=True)

def get_lawyer_performance_data(filters=None):
	"""Get data for lawyer performance report"""
	if not filters:
		filters = {}

	conditions = []
	values = []

	# Build conditions based on filters
	if filters.get("status"):
		conditions.append("l.status = %s")
		values.append(filters["status"])

	if filters.get("practice_areas"):
		conditions.append("l.practice_areas LIKE %s")
		values.append(f"%{filters['practice_areas']}%")

	if filters.get("joining_date"):
		conditions.append("l.joining_date >= %s")
		values.append(filters["joining_date"])

	if filters.get("joining_date_to"):
		conditions.append("l.joining_date <= %s")
		values.append(filters["joining_date_to"])

	where_clause = " AND ".join(conditions) if conditions else "1=1"

	query = f"""
		SELECT
			l.name,
			l.lawyer_name,
			l.status,
			l.practice_areas,
			l.years_of_experience,
			l.joining_date,
			COUNT(DISTINCT lc.name) as total_cases,
			COUNT(DISTINCT CASE WHEN lc.status IN ('Active', 'Pending') THEN lc.name END) as active_cases,
			COUNT(DISTINCT CASE WHEN lc.status = 'Closed' AND lc.outcome = 'Won' THEN lc.name END) as won_cases,
			ROUND(
				(CASE WHEN COUNT(DISTINCT lc.name) > 0
					THEN (COUNT(DISTINCT CASE WHEN lc.status = 'Closed' AND lc.outcome = 'Won' THEN lc.name END) * 100.0 / COUNT(DISTINCT lc.name))
					ELSE 0 END), 2
			) as success_rate,
			COALESCE(SUM(ls.total_amount), 0) as total_revenue
		FROM `tabLawyer` l
		LEFT JOIN `tabLegal Case` lc ON lc.assigned_lawyer = l.name
		LEFT JOIN `tabLegal Service` ls ON ls.assigned_lawyer = l.name AND ls.status = 'Paid'
		WHERE {where_clause}
		GROUP BY l.name
		ORDER BY l.joining_date DESC
	"""

	return frappe.db.sql(query, values, as_dict=True)

def get_service_request_data(filters=None):
	"""Get data for service request report"""
	if not filters:
		filters = {}

	conditions = []
	values = []

	# Build conditions based on filters
	if filters.get("status"):
		conditions.append("sr.status = %s")
		values.append(filters["status"])

	if filters.get("priority"):
		conditions.append("sr.priority = %s")
		values.append(filters["priority"])

	if filters.get("service_type"):
		conditions.append("sr.service_type = %s")
		values.append(filters["service_type"])

	if filters.get("request_date"):
		conditions.append("sr.request_date >= %s")
		values.append(filters["request_date"])

	if filters.get("request_date_to"):
		conditions.append("sr.request_date <= %s")
		values.append(filters["request_date_to"])

	where_clause = " AND ".join(conditions) if conditions else "1=1"

	query = f"""
		SELECT
			sr.name,
			sr.client_name,
			sr.email,
			sr.service_type,
			sr.status,
			sr.priority,
			sr.request_date,
			sr.assigned_to_name,
			sr.due_date,
			sr.completion_date
		FROM `tabService Request` sr
		WHERE {where_clause}
		ORDER BY sr.request_date DESC
	"""

	return frappe.db.sql(query, values, as_dict=True)

def get_financial_summary_data(filters=None):
	"""Get data for financial summary report"""
	if not filters:
		filters = {}

	conditions = []
	values = []

	# Build conditions based on filters
	if filters.get("status"):
		conditions.append("ls.status = %s")
		values.append(filters["status"])

	if filters.get("service_type"):
		conditions.append("ls.service_type = %s")
		values.append(filters["service_type"])

	if filters.get("client"):
		conditions.append("ls.client = %s")
		values.append(filters["client"])

	if filters.get("invoice_date"):
		conditions.append("ls.invoice_date >= %s")
		values.append(filters["invoice_date"])

	if filters.get("invoice_date_to"):
		conditions.append("ls.invoice_date <= %s")
		values.append(filters["invoice_date_to"])

	where_clause = " AND ".join(conditions) if conditions else "1=1"

	query = f"""
		SELECT
			ls.name,
			ls.client_name,
			ls.service_type,
			ls.status,
			ls.invoice_date,
			ls.due_date,
			ls.total_amount,
			ls.paid_amount,
			(ls.total_amount - COALESCE(ls.paid_amount, 0)) as outstanding_amount,
			CASE
				WHEN ls.status = 'Paid' THEN 'Paid'
				WHEN ls.due_date < CURDATE() AND (ls.total_amount - COALESCE(ls.paid_amount, 0)) > 0 THEN 'Overdue'
				WHEN COALESCE(ls.paid_amount, 0) > 0 THEN 'Partially Paid'
				ELSE 'Unpaid'
			END as payment_status
		FROM `tabLegal Service` ls
		WHERE {where_clause}
		ORDER BY ls.invoice_date DESC
	"""

	return frappe.db.sql(query, values, as_dict=True)

def get_hearing_schedule_data(filters=None):
	"""Get data for hearing schedule report"""
	if not filters:
		filters = {}

	conditions = []
	values = []

	# Build conditions based on filters
	if filters.get("status"):
		conditions.append("ch.status = %s")
		values.append(filters["status"])

	if filters.get("hearing_type"):
		conditions.append("ch.hearing_type = %s")
		values.append(filters["hearing_type"])

	if filters.get("court"):
		conditions.append("ch.court = %s")
		values.append(filters["court"])

	if filters.get("hearing_date"):
		conditions.append("ch.hearing_date >= %s")
		values.append(filters["hearing_date"])

	if filters.get("hearing_date_to"):
		conditions.append("ch.hearing_date <= %s")
		values.append(filters["hearing_date_to"])

	where_clause = " AND ".join(conditions) if conditions else "1=1"

	query = f"""
		SELECT
			ch.name,
			ch.case_name,
			ch.client_name,
			ch.court_name,
			ch.hearing_date,
			ch.hearing_time,
			ch.hearing_type,
			ch.judge_name,
			ch.status,
			ch.outcome
		FROM `tabCase Hearing` ch
		WHERE {where_clause}
		ORDER BY ch.hearing_date ASC, ch.hearing_time ASC
	"""

	return frappe.db.sql(query, values, as_dict=True)