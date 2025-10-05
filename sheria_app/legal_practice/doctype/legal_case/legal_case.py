# Copyright (c) 2024, Sheria Law Management System and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import getdate, today

class WebsiteConfig:
	def __init__(self):
		self.condition_field = "published"
		self.page_name_field = "name"
		self.template = "legal_case_profile"

class LegalCase(Document):
	website = WebsiteConfig()

	def validate(self):
		# Set default date opened if not set
		if not self.case_details_date_opened:
			self.case_details_date_opened = today()

		# Validate case year format
		if self.header_case_year and len(str(self.header_case_year)) != 4:
			frappe.throw("Case Year must be a 4-digit year")

		# Ensure case number is provided
		if not self.header_case_number:
			frappe.throw("Case Number is required")

	def on_update(self):
		# Update case status based on proceedings
		self.update_case_status()

	def update_case_status(self):
		# Logic to update case status based on current state
		# This method is called during on_update
		# Add any status update logic here if needed
		pass


def get_permission_query_conditions(user):
	"""
	Return permission query conditions for Legal Case
	"""
	if not user:
		user = frappe.session.user

	# Admin users can see all cases
	if "System Manager" in frappe.get_roles(user):
		return None

	# Lawyers can see cases they are assigned to
	if "Lawyer" in frappe.get_roles(user):
		return f"`tabLegal Case`.`case_details_assigned_to` = {frappe.db.escape(user)}"

	# Clients can see their own cases
	if "Client" in frappe.get_roles(user):
		# Get client name from user
		client_name = frappe.db.get_value("Client", {"email_address": user}, "client_name")
		if client_name:
			return f"`tabLegal Case`.`case_details_client_name` = {frappe.db.escape(client_name)}"

	# Default: no access
	return "1=0"


def has_permission(doc, ptype="read", user=None):
	"""
	Check if user has permission for a specific Legal Case document
	"""
	user = user or frappe.session.user

	# System Managers have full access
	if "System Manager" in frappe.get_roles(user):
		return True

	# Lawyers can access cases assigned to them
	if "Lawyer" in frappe.get_roles(user):
		return doc.case_details_assigned_to == user

	# Clients can access their own cases
	if "Client" in frappe.get_roles(user):
		client_name = frappe.db.get_value("Client", {"email_address": user}, "client_name")
		return doc.case_details_client_name == client_name

	# Default: no access
	return False