# Sheria App Install Module
# Copyright (c) 2024, Coale Tech
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.desk.page.setup_wizard.setup_wizard import make_records
from . import dashboard
from . import workspace
from . import web_pages
from . import permissions

def before_install():
	"""Before app installation"""
	pass

def after_install():
	"""After app installation"""
	try:
		# Create default records
		create_default_records()

		# Set up roles and permissions
		setup_roles_and_permissions()

		# Create default workspaces
		create_default_workspaces()

		# Create default settings
		create_default_settings()

		# Create default email templates
		create_default_email_templates()

		# Create default print formats
		create_default_print_formats()

		# Create default dashboards
		dashboard.create_default_dashboards()

		# Create default web pages
		web_pages.create_default_web_pages()

		# Create default roles and permissions
		permissions.create_default_roles()
		permissions.create_default_user_types()
		permissions.setup_permissions()

		frappe.db.commit()

	except Exception as e:
		frappe.log_error(f"Error in after_install: {str(e)}")
		frappe.throw(_("Installation failed. Please check error logs."))

def create_default_records():
	"""Create default records for the app"""
	try:
		# Create default practice areas
		practice_areas = [
			{"practice_area": "Corporate Law", "description": "Business formation, contracts, mergers & acquisitions"},
			{"practice_area": "Criminal Law", "description": "Criminal defense and prosecution"},
			{"practice_area": "Family Law", "description": "Divorce, custody, adoption, domestic partnerships"},
			{"practice_area": "Property Law", "description": "Real estate, land disputes, property transactions"},
			{"practice_area": "Employment Law", "description": "Labor relations, workplace disputes, employment contracts"},
			{"practice_area": "Intellectual Property", "description": "Patents, trademarks, copyrights, trade secrets"},
			{"practice_area": "Tax Law", "description": "Tax planning, compliance, disputes"},
			{"practice_area": "Constitutional Law", "description": "Human rights, constitutional challenges"},
			{"practice_area": "Environmental Law", "description": "Environmental protection, compliance"},
			{"practice_area": "International Law", "description": "Cross-border transactions, treaties"}
		]

		for area in practice_areas:
			if not frappe.db.exists("Practice Area", area["practice_area"]):
				doc = frappe.get_doc({
					"doctype": "Practice Area",
					"practice_area": area["practice_area"],
					"description": area["description"]
				})
				doc.insert()

		# Create default case types
		case_types = [
			{"case_type": "Civil Suit", "description": "Civil litigation matters"},
			{"case_type": "Criminal Case", "description": "Criminal prosecution or defense"},
			{"case_type": "Constitutional Petition", "description": "Constitutional law matters"},
			{"case_type": "Commercial Dispute", "description": "Business and commercial disputes"},
			{"case_type": "Employment Dispute", "description": "Labor and employment matters"},
			{"case_type": "Family Dispute", "description": "Family law matters"},
			{"case_type": "Property Dispute", "description": "Property and land matters"},
			{"case_type": "Tax Dispute", "description": "Tax-related disputes"},
			{"case_type": "Intellectual Property", "description": "IP infringement cases"}
		]

		for case_type in case_types:
			if not frappe.db.exists("Case Type", case_type["case_type"]):
				doc = frappe.get_doc({
					"doctype": "Case Type",
					"case_type": case_type["case_type"],
					"description": case_type["case_type"]
				})
				doc.insert()

		# Create default courts
		courts = [
			{"court_name": "High Court of Kenya", "court_type": "High Court", "jurisdiction": "National"},
			{"court_name": "Court of Appeal", "court_type": "Appellate Court", "jurisdiction": "National"},
			{"court_name": "Supreme Court of Kenya", "court_type": "Supreme Court", "jurisdiction": "National"},
			{"court_name": "Nairobi Chief Magistrate Court", "court_type": "Magistrate Court", "jurisdiction": "Nairobi"},
			{"court_name": "Mombasa High Court", "court_type": "High Court", "jurisdiction": "Coast"},
			{"court_name": "Kisumu High Court", "court_type": "High Court", "jurisdiction": "Nyanza"},
			{"court_name": "Eldoret High Court", "court_type": "High Court", "jurisdiction": "Rift Valley"}
		]

		for court in courts:
			if not frappe.db.exists("Court", court["court_name"]):
				doc = frappe.get_doc({
					"doctype": "Court",
					"court_name": court["court_name"],
					"court_type": court["court_type"],
					"jurisdiction": court["jurisdiction"]
				})
				doc.insert()

	except Exception as e:
		frappe.log_error(f"Error creating default records: {str(e)}")

def setup_roles_and_permissions():
	"""Set up roles and permissions"""
	try:
		# Create custom roles
		roles = [
			{"role_name": "Legal Admin", "desk_access": 1, "is_custom": 1},
			{"role_name": "Lawyer", "desk_access": 1, "is_custom": 1},
			{"role_name": "Legal Assistant", "desk_access": 1, "is_custom": 1},
			{"role_name": "Client", "desk_access": 0, "is_custom": 1}
		]

		for role_data in roles:
			if not frappe.db.exists("Role", role_data["role_name"]):
				role = frappe.get_doc({
					"doctype": "Role",
					"role_name": role_data["role_name"],
					"desk_access": role_data["desk_access"],
					"is_custom": role_data["is_custom"]
				})
				role.insert()

	except Exception as e:
		frappe.log_error(f"Error setting up roles: {str(e)}")

def create_default_workspaces():
	"""Create default workspaces"""
	try:
		# Legal Practice Workspace
		if not frappe.db.exists("Workspace", "Legal Practice"):
			workspace = frappe.get_doc({
				"doctype": "Workspace",
				"name": "Legal Practice",
				"label": "Legal Practice",
				"category": "Modules",
				"is_standard": 1,
				"developer_mode_only": 0,
				"restrict_to_domain": "",
				"icon": "octicon octicon-law",
				"color": "blue",
				"content": """
# Legal Practice

Welcome to the Legal Practice workspace. This is where you manage all legal cases, hearings, and practice-related activities.

## Quick Actions
- [New Case](/app/legal-case/new)
- [Case Calendar](/app/query-report/Case Calendar)
- [Legal Reports](/app/query-report/Legal Practice Reports)

## Recent Cases
<!-- Recent Cases will be displayed here -->

## Upcoming Hearings
<!-- Upcoming hearings will be displayed here -->
				""",
				"extends_another_page": 0,
				"is_hidden": 0
			})
			workspace.insert()

		# Client Services Workspace
		if not frappe.db.exists("Workspace", "Client Services"):
			workspace = frappe.get_doc({
				"doctype": "Workspace",
				"name": "Client Services",
				"label": "Client Services",
				"category": "Modules",
				"is_standard": 1,
				"developer_mode_only": 0,
				"restrict_to_domain": "",
				"icon": "octicon octicon-person",
				"color": "green",
				"content": """
# Client Services

Manage client relationships, service requests, and client communications.

## Quick Actions
- [New Service Request](/app/service-request/new)
- [Client Portal](/app/client-portal)
- [Service Reports](/app/query-report/Client Service Reports)

## Active Service Requests
<!-- Active service requests will be displayed here -->

## Client Feedback
<!-- Client feedback will be displayed here -->
				""",
				"extends_another_page": 0,
				"is_hidden": 0
			})
			workspace.insert()

	except Exception as e:
		frappe.log_error(f"Error creating workspaces: {str(e)}")

def create_default_settings():
	"""Create default settings"""
	try:
		if not frappe.db.exists("Sheria Settings"):
			settings = frappe.get_doc({
				"doctype": "Sheria Settings",
				"company_name": "Sheria Legal Technologies",
				"admin_email": "admin@sheria_app.co.ke",
				"default_currency": "KES",
				"case_number_prefix": "CASE",
				"hearing_reminder_days": 7,
				"auto_create_case_timeline": 1,
				"enable_client_portal": 1,
				"enable_online_booking": 1
			})
			settings.insert()

	except Exception as e:
		frappe.log_error(f"Error creating settings: {str(e)}")

def create_default_email_templates():
	"""Create default email templates"""
	try:
		# Booking confirmation template
		if not frappe.db.exists("Email Template", "Booking Confirmation"):
			template = frappe.get_doc({
				"doctype": "Email Template",
				"name": "Booking Confirmation",
				"subject": "Legal Service Booking Confirmation - {{ service_request.name }}",
				"response": """
Dear {{ data.client_name }},

Thank you for booking our legal services. Your booking has been confirmed.

**Booking Details:**
- Service: {{ data.service_name }}
- Reference: {{ service_request.name }}
- Preferred Date: {{ data.preferred_date }}
- Status: Submitted

We will contact you within 24 hours to discuss next steps and schedule your consultation.

**Contact Information:**
- Email: {{ data.client_email }}
- Phone: {{ data.client_phone }}

If you have any questions, please don't hesitate to contact us.

Best regards,
Sheria Legal Team
				""",
				"owner": "Administrator"
			})
			template.insert()

		# Contact form template
		if not frappe.db.exists("Email Template", "Contact Form Submission"):
			template = frappe.get_doc({
				"doctype": "Email Template",
				"name": "Contact Form Submission",
				"subject": "New Contact Form Submission from {{ data.name }}",
				"response": """
A new contact form has been submitted:

**Contact Details:**
- Name: {{ data.name }}
- Email: {{ data.email }}
- Phone: {{ data.phone }}
- Address: {{ data.address }}

**Message:**
{{ data.message }}

Please respond to this inquiry as soon as possible.
				""",
				"owner": "Administrator"
			})
			template.insert()

	except Exception as e:
		frappe.log_error(f"Error creating email templates: {str(e)}")

def create_default_print_formats():
	"""Create default print formats"""
	try:
		# Legal Case print format
		if not frappe.db.exists("Print Format", "Legal Case Standard"):
			print_format = frappe.get_doc({
				"doctype": "Print Format",
				"name": "Legal Case Standard",
				"doc_type": "Legal Case",
				"standard": "Yes",
				"print_format_type": "Jinja",
				"raw_printing": 0,
				"raw_commands": "",
				"html": """
<div class="print-format">
	<div class="header">
		<h2>LEGAL CASE DETAILS</h2>
		<h3>{{ doc.case_title }}</h3>
	</div>

	<div class="case-info">
		<table class="table table-bordered">
			<tr>
				<td><strong>Case Number:</strong></td>
				<td>{{ doc.name }}</td>
				<td><strong>Case Type:</strong></td>
				<td>{{ doc.case_type }}</td>
			</tr>
			<tr>
				<td><strong>Client:</strong></td>
				<td>{{ doc.client_name }}</td>
				<td><strong>Status:</strong></td>
				<td>{{ doc.status }}</td>
			</tr>
			<tr>
				<td><strong>Court:</strong></td>
				<td>{{ doc.court }}</td>
				<td><strong>Judge:</strong></td>
				<td>{{ doc.judge }}</td>
			</tr>
			<tr>
				<td><strong>Practice Area:</strong></td>
				<td>{{ doc.practice_area }}</td>
				<td><strong>Priority:</strong></td>
				<td>{{ doc.priority }}</td>
			</tr>
		</table>
	</div>

	<div class="case-description">
		<h4>Case Description</h4>
		<p>{{ doc.description }}</p>
	</div>

	{% if doc.case_documents %}
	<div class="case-documents">
		<h4>Case Documents</h4>
		<ul>
		{% for doc in doc.case_documents %}
			<li>{{ doc.document_name }} - {{ doc.document_type }}</li>
		{% endfor %}
		</ul>
	</div>
	{% endif %}
</div>

<style>
.print-format { font-family: Arial, sans-serif; }
.header { text-align: center; margin-bottom: 30px; }
.case-info { margin-bottom: 30px; }
.table { width: 100%; border-collapse: collapse; }
.table td { padding: 8px; border: 1px solid #ddd; }
.case-description, .case-documents { margin-top: 30px; }
</style>
				""",
				"align_labels_right": 0,
				"show_section_headings": 1,
				"line_breaks": 0,
				"margin_top": 15,
				"margin_bottom": 15,
				"margin_left": 15,
				"margin_right": 15,
				"page_number": "Hide",
				"owner": "Administrator"
			})
			print_format.insert()

	except Exception as e:
		frappe.log_error(f"Error creating print formats: {str(e)}")