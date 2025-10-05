# Copyright (c) 2024, Sheria Law Management System and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Judge(Document):
	def validate(self):
		# Validate judge name is provided
		if not self.judge_name:
			frappe.throw("Judge Name is required")

		# Validate email format if provided
		if self.email_address and not frappe.utils.validate_email_address(self.email_address):
			frappe.throw("Please enter a valid email address")