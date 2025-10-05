# Copyright (c) 2024, Sheria Law Management System and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Court(Document):
	def validate(self):
		# Validate court name is provided
		if not self.court_name:
			frappe.throw("Court Name is required")

		# Validate email format if provided
		if self.court_email and not frappe.utils.validate_email_address(self.court_email):
			frappe.throw("Please enter a valid email address")