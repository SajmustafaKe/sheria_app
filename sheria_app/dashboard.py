# Sheria Dashboard Module
# Copyright (c) 2024, Sheria Legal Technologies
# For license information, please see license.txt

import frappe
from frappe import _

def get_dashboard_config():
	"""Get dashboard configuration for Sheria app"""
	return {
		"Legal Practice Dashboard": {
			"name": "Legal Practice Dashboard",
			"dashboard_name": "Legal Practice",
			"charts": get_legal_practice_charts(),
			"cards": get_legal_practice_cards(),
			"doctype": "Legal Case"
		},
		"Client Services Dashboard": {
			"name": "Client Services Dashboard",
			"dashboard_name": "Client Services",
			"charts": get_client_services_charts(),
			"cards": get_client_services_cards(),
			"doctype": "Service Request"
		},
		"Financial Dashboard": {
			"name": "Financial Dashboard",
			"dashboard_name": "Financial Overview",
			"charts": get_financial_charts(),
			"cards": get_financial_cards(),
			"doctype": "Legal Service"
		}
	}

def get_legal_practice_charts():
	"""Get charts for legal practice dashboard"""
	return [
		{
			"chart_name": "Case Status Distribution",
			"chart_type": "Donut",
			"document_type": "Legal Case",
			"based_on": "status",
			"value_based_on": "",
			"group_by_type": "Count",
			"group_by_based_on": "",
			"filters_json": "[]",
			"timespan": "Last Year",
			"time_interval": "Monthly",
			"timeseries": 0,
			"color": "#4CAF50"
		},
		{
			"chart_name": "Cases by Practice Area",
			"chart_type": "Bar",
			"document_type": "Legal Case",
			"based_on": "practice_area",
			"value_based_on": "",
			"group_by_type": "Count",
			"group_by_based_on": "",
			"filters_json": "[]",
			"timespan": "Last Year",
			"time_interval": "Monthly",
			"timeseries": 0,
			"color": "#2196F3"
		},
		{
			"chart_name": "Case Filing Trend",
			"chart_type": "Line",
			"document_type": "Legal Case",
			"based_on": "filing_date",
			"value_based_on": "",
			"group_by_type": "Count",
			"group_by_based_on": "",
			"filters_json": "[]",
			"timespan": "Last Year",
			"time_interval": "Monthly",
			"timeseries": 1,
			"color": "#FF9800"
		},
		{
			"chart_name": "Lawyer Case Load",
			"chart_type": "Bar",
			"document_type": "Legal Case",
			"based_on": "assigned_lawyer_name",
			"value_based_on": "",
			"group_by_type": "Count",
			"group_by_based_on": "",
			"filters_json": '[{"status": "Active"}]',
			"timespan": "Last Year",
			"time_interval": "Monthly",
			"timeseries": 0,
			"color": "#9C27B0"
		},
		{
			"chart_name": "Case Priority Distribution",
			"chart_type": "Pie",
			"document_type": "Legal Case",
			"based_on": "priority",
			"value_based_on": "",
			"group_by_type": "Count",
			"group_by_based_on": "",
			"filters_json": '[{"status": "Active"}]',
			"timespan": "Last Year",
			"time_interval": "Monthly",
			"timeseries": 0,
			"color": "#F44336"
		},
		{
			"chart_name": "Court Case Distribution",
			"chart_type": "Bar",
			"document_type": "Legal Case",
			"based_on": "court_name",
			"value_based_on": "",
			"group_by_type": "Count",
			"group_by_based_on": "",
			"filters_json": "[]",
			"timespan": "Last Year",
			"time_interval": "Monthly",
			"timeseries": 0,
			"color": "#607D8B"
		}
	]

def get_legal_practice_cards():
	"""Get cards for legal practice dashboard"""
	return [
		{
			"card_name": "Total Active Cases",
			"label": _("Total Active Cases"),
			"function": "Count",
			"document_type": "Legal Case",
			"filters_json": '[{"status": "Active"}]',
			"color": "#4CAF50"
		},
		{
			"card_name": "Cases This Month",
			"label": _("Cases This Month"),
			"function": "Count",
			"document_type": "Legal Case",
			"filters_json": '[{"filing_date": [">=", "2024-01-01"]}]',
			"color": "#2196F3"
		},
		{
			"card_name": "Pending Hearings",
			"label": _("Pending Hearings"),
			"function": "Count",
			"document_type": "Case Hearing",
			"filters_json": '[{"status": "Scheduled"}, {"hearing_date": [">=", "today"]}]',
			"color": "#FF9800"
		},
		{
			"card_name": "Overdue Cases",
			"label": _("Overdue Cases"),
			"function": "Count",
			"document_type": "Legal Case",
			"filters_json": '[{"deadline_date": ["<", "today"]}, {"status": ["in", ["Active", "Pending"]]}]',
			"color": "#F44336"
		}
	]

def get_client_services_charts():
	"""Get charts for client services dashboard"""
	return [
		{
			"chart_name": "Service Request Status",
			"chart_type": "Donut",
			"document_type": "Service Request",
			"based_on": "status",
			"value_based_on": "",
			"group_by_type": "Count",
			"group_by_based_on": "",
			"filters_json": "[]",
			"timespan": "Last Month",
			"time_interval": "Weekly",
			"timeseries": 0,
			"color": "#4CAF50"
		},
		{
			"chart_name": "Service Types Distribution",
			"chart_type": "Bar",
			"document_type": "Service Request",
			"based_on": "service_type",
			"value_based_on": "",
			"group_by_type": "Count",
			"group_by_based_on": "",
			"filters_json": "[]",
			"timespan": "Last Month",
			"time_interval": "Weekly",
			"timeseries": 0,
			"color": "#2196F3"
		},
		{
			"chart_name": "Service Request Trend",
			"chart_type": "Line",
			"document_type": "Service Request",
			"based_on": "request_date",
			"value_based_on": "",
			"group_by_type": "Count",
			"group_by_based_on": "",
			"filters_json": "[]",
			"timespan": "Last 3 Months",
			"time_interval": "Weekly",
			"timeseries": 1,
			"color": "#FF9800"
		},
		{
			"chart_name": "Client Feedback Ratings",
			"chart_type": "Bar",
			"document_type": "Client Feedback",
			"based_on": "overall_rating",
			"value_based_on": "",
			"group_by_type": "Count",
			"group_by_based_on": "",
			"filters_json": "[]",
			"timespan": "Last 3 Months",
			"time_interval": "Monthly",
			"timeseries": 0,
			"color": "#9C27B0"
		}
	]

def get_client_services_cards():
	"""Get cards for client services dashboard"""
	return [
		{
			"card_name": "Total Service Requests",
			"label": _("Total Service Requests"),
			"function": "Count",
			"document_type": "Service Request",
			"filters_json": "[]",
			"color": "#4CAF50"
		},
		{
			"card_name": "Pending Requests",
			"label": _("Pending Requests"),
			"function": "Count",
			"document_type": "Service Request",
			"filters_json": '[{"status": ["in", ["Submitted", "In Progress"]]}]',
			"color": "#FF9800"
		},
		{
			"card_name": "Completed This Month",
			"label": _("Completed This Month"),
			"function": "Count",
			"document_type": "Service Request",
			"filters_json": '[{"status": "Completed"}, {"completion_date": [">=", "2024-01-01"]}]',
			"color": "#2196F3"
		},
		{
			"card_name": "Average Response Time",
			"label": _("Avg Response Time (Days)"),
			"function": "Average",
			"document_type": "Service Request",
			"field": "response_time_days",
			"filters_json": '[{"status": "Completed"}]',
			"color": "#9C27B0"
		}
	]

def get_financial_charts():
	"""Get charts for financial dashboard"""
	return [
		{
			"chart_name": "Revenue by Service Type",
			"chart_type": "Bar",
			"document_type": "Legal Service",
			"based_on": "service_type",
			"value_based_on": "total_amount",
			"group_by_type": "Sum",
			"group_by_based_on": "",
			"filters_json": '[{"status": "Paid"}]',
			"timespan": "Last Year",
			"time_interval": "Monthly",
			"timeseries": 0,
			"color": "#4CAF50"
		},
		{
			"chart_name": "Monthly Revenue Trend",
			"chart_type": "Line",
			"document_type": "Legal Service",
			"based_on": "invoice_date",
			"value_based_on": "total_amount",
			"group_by_type": "Sum",
			"group_by_based_on": "",
			"filters_json": '[{"status": "Paid"}]',
			"timespan": "Last Year",
			"time_interval": "Monthly",
			"timeseries": 1,
			"color": "#2196F3"
		},
		{
			"chart_name": "Payment Status Distribution",
			"chart_type": "Donut",
			"document_type": "Legal Service",
			"based_on": "status",
			"value_based_on": "",
			"group_by_type": "Count",
			"group_by_based_on": "",
			"filters_json": "[]",
			"timespan": "Last 3 Months",
			"time_interval": "Monthly",
			"timeseries": 0,
			"color": "#FF9800"
		},
		{
			"chart_name": "Outstanding Payments",
			"chart_type": "Bar",
			"document_type": "Legal Service",
			"based_on": "client_name",
			"value_based_on": "outstanding_amount",
			"group_by_type": "Sum",
			"group_by_based_on": "",
			"filters_json": '[{"outstanding_amount": [">", 0]}]',
			"timespan": "Last 3 Months",
			"time_interval": "Monthly",
			"timeseries": 0,
			"color": "#F44336"
		}
	]

def get_financial_cards():
	"""Get cards for financial dashboard"""
	return [
		{
			"card_name": "Total Revenue",
			"label": _("Total Revenue"),
			"function": "Sum",
			"document_type": "Legal Service",
			"field": "total_amount",
			"filters_json": '[{"status": "Paid"}]',
			"color": "#4CAF50"
		},
		{
			"card_name": "Outstanding Amount",
			"label": _("Outstanding Amount"),
			"function": "Sum",
			"document_type": "Legal Service",
			"field": "outstanding_amount",
			"filters_json": '[{"outstanding_amount": [">", 0]}]',
			"color": "#F44336"
		},
		{
			"card_name": "Revenue This Month",
			"label": _("Revenue This Month"),
			"function": "Sum",
			"document_type": "Legal Service",
			"field": "total_amount",
			"filters_json": '[{"status": "Paid"}, {"invoice_date": [">=", "2024-01-01"]}]',
			"color": "#2196F3"
		},
		{
			"card_name": "Overdue Invoices",
			"label": _("Overdue Invoices"),
			"function": "Count",
			"document_type": "Legal Service",
			"filters_json": '[{"due_date": ["<", "today"]}, {"outstanding_amount": [">", 0]}]',
			"color": "#FF9800"
		}
	]

def create_default_dashboards():
	"""Create default dashboards for Sheria app"""
	try:
		dashboards = get_dashboard_config()

		for dashboard_key, dashboard_data in dashboards.items():
			if not frappe.db.exists("Dashboard", dashboard_data["name"]):
				dashboard = frappe.get_doc({
					"doctype": "Dashboard",
					"name": dashboard_data["name"],
					"dashboard_name": dashboard_data["dashboard_name"],
					"doctype": dashboard_data["doctype"]
				})

				# Add charts
				for chart in dashboard_data["charts"]:
					dashboard.append("charts", chart)

				# Add cards
				for card in dashboard_data["cards"]:
					dashboard.append("cards", card)

				dashboard.insert(ignore_permissions=True)
				frappe.db.commit()

	except Exception as e:
		frappe.log_error(f"Error creating dashboards: {str(e)}")

@frappe.whitelist()
def create_default_dashboards():
	"""Create default dashboard components for Sheria app"""
	try:
		# Create Number Cards
		create_number_cards()

		# Create Dashboard Charts
		create_dashboard_charts()

		frappe.msgprint(_("Default dashboards created successfully"))

	except Exception as e:
		frappe.log_error(f"Error creating default dashboards: {str(e)}")
		frappe.msgprint(_("Error creating default dashboards: {0}").format(str(e)))


def create_number_cards():
	"""Create default number cards"""
	# Legal Practice Cards
	legal_cards = get_legal_practice_cards()
	for card_data in legal_cards:
		if not frappe.db.exists("Number Card", card_data["card_name"]):
			try:
				doc = frappe.get_doc({
					"doctype": "Number Card",
					"name": card_data["card_name"],
					"label": card_data["label"],
					"document_type": card_data["document_type"],
					"function": card_data["function"],
					"filters_json": card_data["filters_json"],
					"color": card_data["color"]
				})
				if "field" in card_data:
					doc.field = card_data["field"]
				doc.insert()
			except Exception as e:
				frappe.log_error(f"Error creating card {card_data['card_name']}: {str(e)}")

	# Client Services Cards
	client_cards = get_client_services_cards()
	for card_data in client_cards:
		if not frappe.db.exists("Number Card", card_data["card_name"]):
			try:
				doc = frappe.get_doc({
					"doctype": "Number Card",
					"name": card_data["card_name"],
					"label": card_data["label"],
					"document_type": card_data["document_type"],
					"function": card_data["function"],
					"filters_json": card_data["filters_json"],
					"color": card_data["color"]
				})
				if "field" in card_data:
					doc.field = card_data["field"]
				doc.insert()
			except Exception as e:
				frappe.log_error(f"Error creating card {card_data['card_name']}: {str(e)}")

	# Financial Cards
	financial_cards = get_financial_cards()
	for card_data in financial_cards:
		if not frappe.db.exists("Number Card", card_data["card_name"]):
			try:
				doc = frappe.get_doc({
					"doctype": "Number Card",
					"name": card_data["card_name"],
					"label": card_data["label"],
					"document_type": card_data["document_type"],
					"function": card_data["function"],
					"filters_json": card_data["filters_json"],
					"color": card_data["color"]
				})
				if "field" in card_data:
					doc.field = card_data["field"]
				doc.insert()
			except Exception as e:
				frappe.log_error(f"Error creating card {card_data['card_name']}: {str(e)}")


def create_dashboard_charts():
	"""Create default dashboard charts"""
	# Legal Practice Charts
	legal_charts = get_legal_practice_charts()
	for chart_data in legal_charts:
		if not frappe.db.exists("Dashboard Chart", chart_data["chart_name"]):
			try:
				doc = frappe.get_doc({
					"doctype": "Dashboard Chart",
					"name": chart_data["chart_name"],
					"chart_name": chart_data["chart_name"],
					"chart_type": chart_data["chart_type"],
					"document_type": chart_data["document_type"],
					"based_on": chart_data["based_on"],
					"value_based_on": chart_data.get("value_based_on", ""),
					"group_by_type": chart_data["group_by_type"],
					"group_by_based_on": chart_data.get("group_by_based_on", ""),
					"filters_json": chart_data["filters_json"],
					"timespan": chart_data.get("timespan", "Last Year"),
					"time_interval": chart_data.get("time_interval", "Monthly"),
					"timeseries": chart_data.get("timeseries", 0),
					"color": chart_data.get("color", "#4CAF50")
				})
				doc.insert()
			except Exception as e:
				frappe.log_error(f"Error creating chart {chart_data['chart_name']}: {str(e)}")

	# Client Services Charts
	client_charts = get_client_services_charts()
	for chart_data in client_charts:
		if not frappe.db.exists("Dashboard Chart", chart_data["chart_name"]):
			try:
				doc = frappe.get_doc({
					"doctype": "Dashboard Chart",
					"name": chart_data["chart_name"],
					"chart_name": chart_data["chart_name"],
					"chart_type": chart_data["chart_type"],
					"document_type": chart_data["document_type"],
					"based_on": chart_data["based_on"],
					"value_based_on": chart_data.get("value_based_on", ""),
					"group_by_type": chart_data["group_by_type"],
					"group_by_based_on": chart_data.get("group_by_based_on", ""),
					"filters_json": chart_data["filters_json"],
					"timespan": chart_data.get("timespan", "Last Year"),
					"time_interval": chart_data.get("time_interval", "Monthly"),
					"timeseries": chart_data.get("timeseries", 0),
					"color": chart_data.get("color", "#4CAF50")
				})
				doc.insert()
			except Exception as e:
				frappe.log_error(f"Error creating chart {chart_data['chart_name']}: {str(e)}")

	# Financial Charts
	financial_charts = get_financial_charts()
	for chart_data in financial_charts:
		if not frappe.db.exists("Dashboard Chart", chart_data["chart_name"]):
			try:
				doc = frappe.get_doc({
					"doctype": "Dashboard Chart",
					"name": chart_data["chart_name"],
					"chart_name": chart_data["chart_name"],
					"chart_type": chart_data["chart_type"],
					"document_type": chart_data["document_type"],
					"based_on": chart_data["based_on"],
					"value_based_on": chart_data.get("value_based_on", ""),
					"group_by_type": chart_data["group_by_type"],
					"group_by_based_on": chart_data.get("group_by_based_on", ""),
					"filters_json": chart_data["filters_json"],
					"timespan": chart_data.get("timespan", "Last Year"),
					"time_interval": chart_data.get("time_interval", "Monthly"),
					"timeseries": chart_data.get("timeseries", 0),
					"color": chart_data.get("color", "#4CAF50")
				})
				doc.insert()
			except Exception as e:
				frappe.log_error(f"Error creating chart {chart_data['chart_name']}: {str(e)}")
def create_default_dashboards():
	"""Create default dashboards for Sheria app"""
	try:
		dashboards = get_dashboard_config()

		for dashboard_key, dashboard_data in dashboards.items():
			if not frappe.db.exists("Dashboard", dashboard_data["name"]):
				dashboard = frappe.get_doc({
					"doctype": "Dashboard",
					"name": dashboard_data["name"],
					"dashboard_name": dashboard_data["dashboard_name"],
					"doctype": dashboard_data["doctype"]
				})

				# Add charts
				for chart in dashboard_data["charts"]:
					dashboard.append("charts", chart)

				# Add cards
				for card in dashboard_data["cards"]:
					dashboard.append("cards", card)

				dashboard.insert(ignore_permissions=True)
				frappe.db.commit()

	except Exception as e:
		frappe.log_error(f"Error creating dashboards: {str(e)}")

# Dashboard data functions

def get_legal_practice_metrics():
	"""Get metrics for legal practice dashboard"""
	try:
		# Total active cases
		active_cases = frappe.db.count("Legal Case", {"status": "Active"})

		# Cases this month
		current_month = frappe.utils.formatdate(frappe.utils.today(), "MM")
		current_year = frappe.utils.formatdate(frappe.utils.today(), "YYYY")
		cases_this_month = frappe.db.sql("""
			SELECT COUNT(*) as count
			FROM `tabLegal Case`
			WHERE MONTH(filing_date) = %s AND YEAR(filing_date) = %s
		""", (current_month, current_year))[0][0]

		# Pending hearings
		pending_hearings = frappe.db.count("Case Hearing", {
			"status": "Scheduled",
			"hearing_date": [">=", frappe.utils.today()]
		})

		# Overdue cases
		overdue_cases = frappe.db.count("Legal Case", {
			"deadline_date": ["<", frappe.utils.today()],
			"status": ["in", ["Active", "Pending"]]
		})

		return {
			"active_cases": active_cases,
			"cases_this_month": cases_this_month,
			"pending_hearings": pending_hearings,
			"overdue_cases": overdue_cases
		}

	except Exception as e:
		frappe.log_error(f"Error getting legal practice metrics: {str(e)}")
		return {}

def get_client_services_metrics():
	"""Get metrics for client services dashboard"""
	try:
		# Total service requests
		total_requests = frappe.db.count("Service Request")

		# Pending requests
		pending_requests = frappe.db.count("Service Request", {
			"status": ["in", ["Submitted", "In Progress"]]
		})

		# Completed this month
		current_month = frappe.utils.formatdate(frappe.utils.today(), "MM")
		current_year = frappe.utils.formatdate(frappe.utils.today(), "YYYY")
		completed_this_month = frappe.db.sql("""
			SELECT COUNT(*) as count
			FROM `tabService Request`
			WHERE status = 'Completed'
			AND MONTH(completion_date) = %s AND YEAR(completion_date) = %s
		""", (current_month, current_year))[0][0]

		# Average response time
		avg_response_time = frappe.db.sql("""
			SELECT AVG(response_time_days) as avg_time
			FROM `tabService Request`
			WHERE status = 'Completed' AND response_time_days IS NOT NULL
		""")[0][0] or 0

		return {
			"total_requests": total_requests,
			"pending_requests": pending_requests,
			"completed_this_month": completed_this_month,
			"avg_response_time": round(avg_response_time, 1)
		}

	except Exception as e:
		frappe.log_error(f"Error getting client services metrics: {str(e)}")
		return {}

def get_financial_metrics():
	"""Get metrics for financial dashboard"""
	try:
		# Total revenue
		total_revenue = frappe.db.sql("""
			SELECT SUM(total_amount) as revenue
			FROM `tabLegal Service`
			WHERE status = 'Paid'
		""")[0][0] or 0

		# Outstanding amount
		outstanding_amount = frappe.db.sql("""
			SELECT SUM(outstanding_amount) as outstanding
			FROM `tabLegal Service`
			WHERE outstanding_amount > 0
		""")[0][0] or 0

		# Revenue this month
		current_month = frappe.utils.formatdate(frappe.utils.today(), "MM")
		current_year = frappe.utils.formatdate(frappe.utils.today(), "YYYY")
		revenue_this_month = frappe.db.sql("""
			SELECT SUM(total_amount) as revenue
			FROM `tabLegal Service`
			WHERE status = 'Paid'
			AND MONTH(invoice_date) = %s AND YEAR(invoice_date) = %s
		""", (current_month, current_year))[0][0] or 0

		# Overdue invoices
		overdue_invoices = frappe.db.count("Legal Service", {
			"due_date": ["<", frappe.utils.today()],
			"outstanding_amount": [">", 0]
		})

		return {
			"total_revenue": total_revenue,
			"outstanding_amount": outstanding_amount,
			"revenue_this_month": revenue_this_month,
			"overdue_invoices": overdue_invoices
		}

	except Exception as e:
		frappe.log_error(f"Error getting financial metrics: {str(e)}")
		return {}

# Dashboard API endpoints

@frappe.whitelist()
def get_dashboard_data(dashboard_type):
	"""API endpoint to get dashboard data"""
	if dashboard_type == "legal_practice":
		return get_legal_practice_metrics()
	elif dashboard_type == "client_services":
		return get_client_services_metrics()
	elif dashboard_type == "financial":
		return get_financial_metrics()
	else:
		return {}

@frappe.whitelist()
def get_case_status_summary():
	"""Get case status summary for dashboard"""
	try:
		data = frappe.db.sql("""
			SELECT status, COUNT(*) as count
			FROM `tabLegal Case`
			GROUP BY status
			ORDER BY count DESC
		""", as_dict=True)

		return data

	except Exception as e:
		frappe.log_error(f"Error getting case status summary: {str(e)}")
		return []

@frappe.whitelist()
def get_service_request_summary():
	"""Get service request summary for dashboard"""
	try:
		data = frappe.db.sql("""
			SELECT status, COUNT(*) as count
			FROM `tabService Request`
			GROUP BY status
			ORDER BY count DESC
		""", as_dict=True)

		return data

	except Exception as e:
		frappe.log_error(f"Error getting service request summary: {str(e)}")
		return []

@frappe.whitelist()
def get_revenue_trend():
	"""Get revenue trend data for dashboard"""
	try:
		data = frappe.db.sql("""
			SELECT
				DATE_FORMAT(invoice_date, '%Y-%m') as month,
				SUM(total_amount) as revenue
			FROM `tabLegal Service`
			WHERE status = 'Paid'
				AND invoice_date >= DATE_SUB(CURDATE(), INTERVAL 12 MONTH)
			GROUP BY DATE_FORMAT(invoice_date, '%Y-%m')
			ORDER BY month
		""", as_dict=True)

		return data

	except Exception as e:
		frappe.log_error(f"Error getting revenue trend: {str(e)}")
		return []