# Copyright (c) 2024, Sheria Law Management System and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Lawyer(Document):
	def validate(self):
		# Validate lawyer name is provided
		if not self.lawyer_name:
			frappe.throw("Lawyer Name is required")

		# Validate email format if provided
		if self.email_address and not frappe.utils.validate_email_address(self.email_address):
			frappe.throw("Please enter a valid email address")

		# Validate admission number format if provided
		if self.admission_number and not self.admission_number.isalnum():
			frappe.throw("Admission Number should contain only letters and numbers")

	def before_save(self):
		# Set default status if not set
		if not self.status:
			self.status = "Active"