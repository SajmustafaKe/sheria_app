from . import __version__ as app_version

app_name = "sheria_app"
app_title = "Sheria App"
app_publisher = "Coale Tech"
app_description = "Law Management System"
app_icon = "octicon octicon-law"
app_color = "blue"
app_email = "info@coale.tech"
app_license = "mit"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
app_include_css = "/assets/sheria_app/css/sheria_app.css"
app_include_js = "/assets/sheria_app/js/sheria_app.js"

# include js, css files in header of web template
web_include_css = "/assets/sheria_app/css/sheria-web.css"
web_include_js = "/assets/sheria_app/js/sheria-web.js"

# include custom scss in every website theme (without file extension ".scss")
website_theme_scss = "sheria_app/public/scss/website"

# include js, css files in header of web form
webform_include_js = {"Legal Service Request": "public/js/legal_service_request.js"}
webform_include_css = {"Legal Service Request": "public/css/legal_service_request.css"}

# Home Pages
# ----------

# application home page (will override Website Settings)
home_page = "legal-dashboard"

# website user home page (by Role)
role_home_page = {
	"Legal Admin": "legal-dashboard",
	"Lawyer": "legal-dashboard"
}

# Generators
# ----------

# automatically create page for each record of this doctype
website_generators = ["Legal Case", "Legal Service"]

# Installation
# ------------

before_install = "sheria_app.install.before_install"
after_install = "sheria_app.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

notification_config = "sheria_app.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

permission_query_conditions = {
	"Legal Case": "sheria_app.legal_practice.doctype.legal_case.legal_case.get_permission_query_conditions",
	"Legal Service": "sheria_app.client_services.doctype.legal_service.legal_service.get_permission_query_conditions",
}

has_permission = {
	"Legal Case": "sheria_app.legal_practice.doctype.legal_case.legal_case.has_permission",
	"Legal Service": "sheria_app.client_services.doctype.legal_service.legal_service.has_permission",
}

# DocType Class
# ---------------
# Override standard doctype classes

override_doctype_class = {
	# "Customer": "sheria_app.overrides.CustomCustomer",
	"CRM Lead": "sheria_app.crm_extensions.doctype.legal_crm_lead.legal_crm_lead.LegalCRMLead",
	"CRM Deal": "sheria_app.crm_extensions.doctype.legal_crm_deal.legal_crm_deal.LegalCRMDeal"
}

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Legal Case": {
		"on_submit": "sheria_app.legal_practice.doctype.legal_case.legal_case.on_case_submit",
		"on_cancel": "sheria_app.legal_practice.doctype.legal_case.legal_case.on_case_cancel",
	},
	"Legal Service": {
		"on_submit": "sheria_app.client_services.doctype.legal_service.legal_service.on_service_submit",
	},
	# "Customer": {
	# 	"validate": "sheria_app.overrides.customer.validate_kenya_customer",
	# }
}

# Scheduled Tasks
# ---------------

scheduler_events = {
	"all": [
		"sheria_app.tasks.all"
	],
	"daily": [
		"sheria_app.tasks.daily"
	],
	"hourly": [
		"sheria_app.tasks.hourly",
		"sheria_app.crm_extensions.doctype.legal_document_template.legal_document_template.auto_generate_documents"
	],
	"weekly": [
		"sheria_app.tasks.weekly"
	],
	"monthly": [
		"sheria_app.tasks.monthly"
	]
}

# Workspace
# ---------

workspaces = [
	"Legal Practice",
	"Client Services",
	"sheria-legal-management"
]

# Testing
# -------

# before_tests = "sheria_app.install.before_tests"

# Overriding Methods
# ------------------------------
#
override_whitelisted_methods = {
	# "frappe.desk.form.save.savedocs": "sheria_app.overrides.form.save_savedocs"
}

# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
override_doctype_dashboards = {
	"Legal CRM Lead": "sheria_app.crm_extensions.doctype.legal_crm_dashboard.legal_crm_dashboard.get_dashboard_data",
	"Legal CRM Deal": "sheria_app.crm_extensions.doctype.legal_crm_dashboard.legal_crm_dashboard.get_dashboard_data"
}

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Add all simple doctypes related to this app
all_doctypes = {
	"Legal Practice": [
		"Legal Case",
		"Case Hearing",
		"Case Document",
		"Court",
		"Judge",
		"Lawyer",
		"Legal Team",
		"Practice Area",
		"Case Type",
		"Case Status",
		"Legal Research",
		"Legal Precedent",
		"Case Timeline",
		"Legal Fee",
		"Legal Expense"
	],
	"Client Services": [
		"Legal Service",
		"Service Request",
		"Client Portal",
		"Service Package",
		"Legal Consultation",
		"Document Preparation",
		"Legal Agreement",
		"Client Feedback",
		"Service Rating"
	],
	"CRM Extensions": [
		"Legal CRM Lead",
		"Legal CRM Deal",
		"Legal CRM Dashboard",
		"Legal CRM Form Script",
		"Legal Document Template",
		"Legal Document Merge Field"
	]
}

# User Data Protection
# --------------------

user_data_fields = [
	{
		"doctype": "Legal Case",
		"filter_by": "client",
		"redact_fields": ["client_name", "client_email", "client_phone"],
		"partial": 1,
	},
	{
		"doctype": "Legal Service",
		"filter_by": "client",
		"redact_fields": ["client_name", "client_email", "client_phone"],
		"partial": 1,
	},
	{
		"doctype": "Client",
		"filter_by": "email",
		"redact_fields": ["phone", "address"],
		"partial": 1,
	},
]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"sheria_app.auth.validate"
# ]

fixtures = [
	"sheria_app.email_templates",
	"sheria_app.print_formats",
	"sheria_app.web_forms",
	"sheria_app.report_builder",
	"sheria_app.dashboard",
	"sheria_app.web_pages",
	"sheria_app.permissions",
]