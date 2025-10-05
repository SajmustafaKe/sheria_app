# Copyright (c) 2025, Coale Tech and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import nowdate, add_months, add_days, getdate
import json

class LegalCRMDashboard(Document):
	def before_save(self):
		"""Calculate dashboard metrics before saving"""
		self.calculate_metrics()
		self.generate_charts()

	def calculate_metrics(self):
		"""Calculate key legal CRM metrics"""
		filters = self.get_date_filters()

		# Lead metrics
		self.total_leads = self.get_total_leads(filters)
		self.qualified_leads = self.get_qualified_leads(filters)
		self.conversion_rate = (self.qualified_leads / self.total_leads * 100) if self.total_leads > 0 else 0

		# Deal metrics
		self.total_deals = self.get_total_deals(filters)
		self.won_deals = self.get_won_deals(filters)
		self.pipeline_value = self.get_pipeline_value(filters)

	def get_date_filters(self):
		"""Get date filters based on selected range"""
		today = getdate(nowdate())

		if self.date_range == "This Month":
			start_date = today.replace(day=1)
			end_date = add_months(start_date, 1) - add_days(start_date, 1)
		elif self.date_range == "Last Month":
			end_date = today.replace(day=1) - add_days(today.replace(day=1), 1)
			start_date = end_date.replace(day=1)
		elif self.date_range == "This Quarter":
			quarter = (today.month - 1) // 3 + 1
			start_date = getdate(f"{today.year}-{3*quarter-2}-01")
			end_date = add_months(start_date, 3) - add_days(start_date, 1)
		else:  # Default to last 30 days
			start_date = add_days(today, -30)
			end_date = today

		return {
			"start_date": start_date,
			"end_date": end_date
		}

	def get_total_leads(self, filters):
		"""Get total leads count"""
		additional_filters = {}
		if self.practice_area_filter:
			additional_filters["practice_area"] = self.practice_area_filter
		if self.lawyer_filter:
			additional_filters["lead_owner"] = self.lawyer_filter
		if self.client_type_filter:
			additional_filters["client_type"] = self.client_type_filter

		query = """
			SELECT COUNT(*)
			FROM `tabLegal CRM Lead`
			WHERE creation >= %(start_date)s AND creation <= %(end_date)s
		"""
		params = {
			"start_date": filters["start_date"],
			"end_date": filters["end_date"]
		}

		if additional_filters:
			conditions = []
			for field, value in additional_filters.items():
				conditions.append(f"{field} = %({field})s")
				params[field] = value
			query += " AND " + " AND ".join(conditions)

		result = frappe.db.sql(query, params)
		return result[0][0] if result else 0

	def get_qualified_leads(self, filters):
		"""Get qualified leads count"""
		additional_filters = {}
		if self.practice_area_filter:
			additional_filters["practice_area"] = self.practice_area_filter
		if self.lawyer_filter:
			additional_filters["lead_owner"] = self.lawyer_filter
		if self.client_type_filter:
			additional_filters["client_type"] = self.client_type_filter

		query = """
			SELECT COUNT(*)
			FROM `tabLegal CRM Lead`
			WHERE status = 'Qualified' AND creation >= %(start_date)s AND creation <= %(end_date)s
		"""
		params = {
			"start_date": filters["start_date"],
			"end_date": filters["end_date"]
		}

		if additional_filters:
			conditions = []
			for field, value in additional_filters.items():
				conditions.append(f"{field} = %({field})s")
				params[field] = value
			query += " AND " + " AND ".join(conditions)

		result = frappe.db.sql(query, params)
		return result[0][0] if result else 0

	def get_total_deals(self, filters):
		"""Get total deals count"""
		additional_filters = {}
		if self.practice_area_filter:
			additional_filters["practice_area"] = self.practice_area_filter
		if self.lawyer_filter:
			additional_filters["deal_owner"] = self.lawyer_filter
		if self.client_type_filter:
			additional_filters["client_type"] = self.client_type_filter

		query = """
			SELECT COUNT(*)
			FROM `tabLegal CRM Deal`
			WHERE creation >= %(start_date)s AND creation <= %(end_date)s
		"""
		params = {
			"start_date": filters["start_date"],
			"end_date": filters["end_date"]
		}

		if additional_filters:
			conditions = []
			for field, value in additional_filters.items():
				conditions.append(f"{field} = %({field})s")
				params[field] = value
			query += " AND " + " AND ".join(conditions)

		result = frappe.db.sql(query, params)
		return result[0][0] if result else 0

	def get_won_deals(self, filters):
		"""Get won deals count"""
		additional_filters = {}
		if self.practice_area_filter:
			additional_filters["practice_area"] = self.practice_area_filter
		if self.lawyer_filter:
			additional_filters["deal_owner"] = self.lawyer_filter
		if self.client_type_filter:
			additional_filters["client_type"] = self.client_type_filter

		query = """
			SELECT COUNT(*)
			FROM `tabLegal CRM Deal`
			WHERE status = 'Won' AND creation >= %(start_date)s AND creation <= %(end_date)s
		"""
		params = {
			"start_date": filters["start_date"],
			"end_date": filters["end_date"]
		}

		if additional_filters:
			conditions = []
			for field, value in additional_filters.items():
				conditions.append(f"{field} = %({field})s")
				params[field] = value
			query += " AND " + " AND ".join(conditions)

		result = frappe.db.sql(query, params)
		return result[0][0] if result else 0

	def get_pipeline_value(self, filters):
		"""Get total pipeline value"""
		additional_filters = {}
		if self.practice_area_filter:
			additional_filters["practice_area"] = self.practice_area_filter
		if self.lawyer_filter:
			additional_filters["deal_owner"] = self.lawyer_filter
		if self.client_type_filter:
			additional_filters["client_type"] = self.client_type_filter

		query = """
			SELECT SUM(expected_deal_value)
			FROM `tabLegal CRM Deal`
			WHERE status IN ('Proposal', 'Negotiation') AND creation >= %(start_date)s AND creation <= %(end_date)s
		"""
		params = {
			"start_date": filters["start_date"],
			"end_date": filters["end_date"]
		}

		if additional_filters:
			conditions = []
			for field, value in additional_filters.items():
				conditions.append(f"{field} = %({field})s")
				params[field] = value
			query += " AND " + " AND ".join(conditions)

		result = frappe.db.sql(query, params)
		return result[0][0] if result and result[0][0] else 0

	def generate_charts(self):
		"""Generate chart data for dashboard"""
		self.leads_by_practice_area = self.get_leads_by_practice_area_chart()
		self.deals_by_status = self.get_deals_by_status_chart()
		self.monthly_revenue = self.get_monthly_revenue_chart()
		self.trust_balance_summary = self.get_trust_balance_summary()
		self.recent_leads = self.get_recent_leads()
		self.recent_deals = self.get_recent_deals()
		self.upcoming_deadlines = self.get_upcoming_deadlines()
		self.low_trust_balances = self.get_low_trust_balances()

	def get_leads_by_practice_area_chart(self):
		"""Generate leads by practice area chart data"""
		data = frappe.db.sql("""
			SELECT practice_area, COUNT(*) as count
			FROM `tabLegal CRM Lead`
			WHERE practice_area IS NOT NULL
			GROUP BY practice_area
			ORDER BY count DESC
			LIMIT 10
		""", as_dict=True)

		chart_data = {
			"type": "pie",
			"data": {
				"labels": [d.practice_area for d in data],
				"datasets": [{
					"data": [d.count for d in data]
				}]
			}
		}

		return json.dumps(chart_data)

	def get_deals_by_status_chart(self):
		"""Generate deals by status chart data"""
		data = frappe.db.sql("""
			SELECT status, COUNT(*) as count
			FROM `tabLegal CRM Deal`
			GROUP BY status
			ORDER BY count DESC
		""", as_dict=True)

		chart_data = {
			"type": "bar",
			"data": {
				"labels": [d.status for d in data],
				"datasets": [{
					"label": "Deals",
					"data": [d.count for d in data]
				}]
			}
		}

		return json.dumps(chart_data)

	def get_monthly_revenue_chart(self):
		"""Generate monthly revenue chart data"""
		data = frappe.db.sql("""
			SELECT DATE_FORMAT(closed_date, '%Y-%m') as month,
				   SUM(deal_value) as revenue
			FROM `tabLegal CRM Deal`
			WHERE status = 'Won' AND closed_date IS NOT NULL
			AND closed_date >= DATE_SUB(CURDATE(), INTERVAL 12 MONTH)
			GROUP BY month
			ORDER BY month
		""", as_dict=True)

		chart_data = {
			"type": "line",
			"data": {
				"labels": [d.month for d in data],
				"datasets": [{
					"label": "Revenue",
					"data": [d.revenue for d in data]
				}]
			}
		}

		return json.dumps(chart_data)

	def get_trust_balance_summary(self):
		"""Get trust balance summary"""
		data = frappe.db.sql("""
			SELECT
				SUM(trust_balance) as total_balance,
				COUNT(CASE WHEN trust_balance > 0 THEN 1 END) as positive_balances,
				COUNT(CASE WHEN trust_balance <= 0 THEN 1 END) as zero_negative_balances
			FROM `tabLegal CRM Lead`
			WHERE trust_balance IS NOT NULL
		""", as_dict=True)

		if data:
			summary = f"""
			<div class="trust-summary">
				<h4>Trust Account Summary</h4>
				<p><strong>Total Balance:</strong> {frappe.utils.fmt_money(data[0].total_balance or 0)}</p>
				<p><strong>Active Accounts:</strong> {data[0].positive_balances or 0}</p>
				<p><strong>Zero/Negative:</strong> {data[0].zero_negative_balances or 0}</p>
			</div>
			"""
			return summary

		return "<p>No trust balance data available</p>"

	def get_recent_leads(self):
		"""Get recent leads list"""
		leads = frappe.db.sql("""
			SELECT name, lead_name, status, creation
			FROM `tabLegal CRM Lead`
			ORDER BY creation DESC
			LIMIT 5
		""", as_dict=True)

		html = "<div class='recent-leads'><h4>Recent Leads</h4><ul>"
		for lead in leads:
			html += f"<li><a href='/app/legal-crm-lead/{lead.name}'>{lead.lead_name}</a> - {lead.status}</li>"
		html += "</ul></div>"

		return html

	def get_recent_deals(self):
		"""Get recent deals list"""
		deals = frappe.db.sql("""
			SELECT name, organization, status, expected_deal_value, creation
			FROM `tabLegal CRM Deal`
			ORDER BY creation DESC
			LIMIT 5
		""", as_dict=True)

		html = "<div class='recent-deals'><h4>Recent Deals</h4><ul>"
		for deal in deals:
			value = frappe.utils.fmt_money(deal.expected_deal_value or 0)
			html += f"<li><a href='/app/legal-crm-deal/{deal.name}'>{deal.organization or 'Unnamed'}</a> - {deal.status} ({value})</li>"
		html += "</ul></div>"

		return html

	def get_upcoming_deadlines(self):
		"""Get upcoming deal deadlines"""
		deadlines = frappe.db.sql("""
			SELECT name, organization, expected_closure_date, status, expected_deal_value
			FROM `tabLegal CRM Deal`
			WHERE expected_closure_date IS NOT NULL
			AND expected_closure_date >= CURDATE()
			AND expected_closure_date <= DATE_ADD(CURDATE(), INTERVAL 30 DAY)
			AND status IN ('Proposal', 'Negotiation')
			ORDER BY expected_closure_date
			LIMIT 5
		""", as_dict=True)

		html = "<div class='upcoming-deadlines'><h4>Upcoming Deal Deadlines</h4><ul>"
		for deadline in deadlines:
			date = deadline.expected_closure_date.strftime('%Y-%m-%d')
			value = frappe.utils.fmt_money(deadline.expected_deal_value or 0)
			html += f"<li>{date}: {deadline.organization or 'Unnamed Deal'} - {deadline.status} ({value})</li>"
		html += "</ul></div>"

		return html

	def get_low_trust_balances(self):
		"""Get clients with low trust balances"""
		low_balances = frappe.db.sql("""
			SELECT name, lead_name, trust_balance
			FROM `tabLegal CRM Lead`
			WHERE trust_balance IS NOT NULL
			AND trust_balance < 1000
			ORDER BY trust_balance ASC
			LIMIT 5
		""", as_dict=True)

		html = "<div class='low-balances'><h4>Low Trust Balances</h4><ul>"
		for balance in low_balances:
			amount = frappe.utils.fmt_money(balance.trust_balance or 0)
			html += f"<li><a href='/app/legal-crm-lead/{balance.name}'>{balance.lead_name}</a> - {amount}</li>"
		html += "</ul></div>"

		return html

@frappe.whitelist()
def get_dashboard_data(data):
	"""Get dashboard data for API calls"""
	# Get the default dashboard
	dashboard = frappe.get_all("Legal CRM Dashboard", 
		filters={"is_default": 1}, 
		limit=1)
	
	if not dashboard:
		return data
	
	dashboard_doc = frappe.get_doc("Legal CRM Dashboard", dashboard[0].name)
	dashboard_doc.calculate_metrics()
	dashboard_doc.generate_charts()

	# Merge with existing data
	data.update({
		"metrics": {
			"total_leads": dashboard_doc.total_leads,
			"qualified_leads": dashboard_doc.qualified_leads,
			"conversion_rate": dashboard_doc.conversion_rate,
			"total_deals": dashboard_doc.total_deals,
			"won_deals": dashboard_doc.won_deals,
			"pipeline_value": dashboard_doc.pipeline_value
		},
		"charts": {
			"leads_by_practice_area": dashboard_doc.leads_by_practice_area,
			"deals_by_status": dashboard_doc.deals_by_status,
			"monthly_revenue": dashboard_doc.monthly_revenue
		}
	})

	return data