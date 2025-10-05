# Copyright (c) 2025, Coale Tech and contributors
# For license information, please see license.txt

import frappe
from frappe import _
import re

from crm.fcrm.doctype.crm_deal.crm_deal import CRMDeal
from crm.fcrm.doctype.crm_service_level_agreement.utils import get_sla
from crm.fcrm.doctype.crm_status_change_log.crm_status_change_log import add_status_change_log
from crm.fcrm.doctype.fcrm_settings.fcrm_settings import get_exchange_rate


class LegalCRMDeal(CRMDeal):
	def validate(self):
		# Call parent validation first
		super().validate()

		# Add legal-specific validations
		self.validate_kra_pin()
		self.validate_company_registration()
		self.validate_client_type_requirements()
		self.validate_case_assignment()
		self.update_trust_balance()
		self.validate_billing_information()

	def validate_kra_pin(self):
		"""Validate KRA PIN format for Kenyan tax identification"""
		if self.kra_pin:
			# KRA PIN format: A123456789X or P123456789X (Individual/Company)
			kra_pattern = r'^[AP]\d{9}[A-Z]$'
			if not re.match(kra_pattern, self.kra_pin.upper()):
				frappe.throw(_("Invalid KRA PIN format. Should be A/P followed by 9 digits and a letter."))

			# Check for duplicates across deals
			existing = frappe.db.exists("Legal CRM Deal",
				{"kra_pin": self.kra_pin, "name": ["!=", self.name]})
			if existing:
				frappe.throw(_("KRA PIN {0} already exists for another deal.").format(self.kra_pin))

	def validate_company_registration(self):
		"""Validate company registration number if client type is Company"""
		if self.client_type == "Company" and self.company_registration_number:
			# Basic validation - should be numeric or have specific format
			if not re.match(r'^[A-Z0-9\-]+$', self.company_registration_number.upper()):
				frappe.throw(_("Invalid company registration number format."))

	def validate_client_type_requirements(self):
		"""Validate required fields based on client type"""
		if self.client_type == "Individual":
			if not self.first_name:
				frappe.throw(_("First name is required for individual clients."))
			if not self.id_passport_number:
				frappe.throw(_("ID/Passport number is required for individual clients."))
		elif self.client_type == "Company":
			if not self.organization:
				frappe.throw(_("Organization name is required for company clients."))
			if not self.company_registration_number:
				frappe.throw(_("Company registration number is required for company clients."))

	def validate_case_assignment(self):
		"""Validate that legal matters have required assignments"""
		if self.practice_area and not self.assigned_lawyer:
			frappe.msgprint(_("Consider assigning a lawyer for this legal matter."),
				alert=True)

		if self.case_type and not self.case_status:
			frappe.throw(_("Case status is required when case type is specified."))

	def update_trust_balance(self):
		"""Update trust balance from trust account transactions"""
		if self.kra_pin:
			# Get trust balance from trust account ledger
			balance = frappe.db.sql("""
				SELECT SUM(credit - debit) as balance
				FROM `tabTrust Account Ledger`
				WHERE kra_pin = %s AND docstatus = 1
			""", self.kra_pin)

			if balance and balance[0][0]:
				self.trust_balance = balance[0][0]
			else:
				self.trust_balance = 0

			# Update trust account transactions table
			self.update_trust_transactions()

	def update_trust_transactions(self):
		"""Update the trust account transactions child table"""
		if self.kra_pin:
			# Clear existing transactions
			self.set("trust_account_transactions", [])

			# Get transactions from trust account ledger
			transactions = frappe.db.sql("""
				SELECT name, transaction_date, transaction_type, debit, credit,
					   balance, description, reference_document
				FROM `tabTrust Account Transaction`
				WHERE kra_pin = %s AND docstatus = 1
				ORDER BY transaction_date DESC, creation DESC
				LIMIT 50
			""", self.kra_pin, as_dict=True)

			for transaction in transactions:
				self.append("trust_account_transactions", {
					"transaction_date": transaction.transaction_date,
					"transaction_type": transaction.transaction_type,
					"debit": transaction.debit,
					"credit": transaction.credit,
					"balance": transaction.balance,
					"description": transaction.description,
					"reference_document": transaction.reference_document,
				})

	def validate_billing_information(self):
		"""Validate billing information for legal matters"""
		if self.expected_deal_value and self.expected_deal_value > 0:
			if not self.payment_terms:
				frappe.msgprint(_("Consider setting payment terms for this matter."),
					alert=True)

			if self.client_type == "Company" and not self.billing_address:
				frappe.msgprint(_("Billing address is recommended for company clients."),
					alert=True)

	def before_save(self):
		# Call parent before_save
		super().before_save()

		# Set deal value from expected deal value if not set
		if self.expected_deal_value and not self.deal_value:
			self.deal_value = self.expected_deal_value

	def on_update(self):
		"""Additional actions on update"""
		super().on_update()

		# Create legal case if this is a won deal with case details
		if self.status == "Won" and self.case_type and not self.get("legal_case"):
			self.create_legal_case()

	def create_legal_case(self):
		"""Create a legal case from this deal"""
		if frappe.db.exists("Legal Case", {"deal": self.name}):
			return

		legal_case = frappe.new_doc("Legal Case")
		legal_case.update({
			"deal": self.name,
			"case_details_client_name": self.organization or f"{self.first_name} {self.last_name}".strip(),
			"practice_area": self.practice_area,
			"court": self.court,
			"case_type": self.case_type,
			"assigned_lawyer": self.assigned_lawyer,
			"case_priority": self.case_priority,
			"description": f"Legal matter created from deal {self.name}",
			"expected_fee": self.expected_deal_value,
		})

		legal_case.insert(ignore_permissions=True)
		frappe.msgprint(_("Legal case {0} created from deal.").format(legal_case.name))

	@staticmethod
	def default_list_data():
		columns = [
			{
				"label": "Organization",
				"type": "Link",
				"key": "organization",
				"options": "CRM Organization",
				"width": "12rem",
			},
			{
				"label": "Deal Owner",
				"type": "Link",
				"key": "deal_owner",
				"options": "User",
				"width": "10rem",
			},
			{
				"label": "Status",
				"type": "Link",
				"key": "status",
				"options": "CRM Deal Status",
				"width": "8rem",
			},
			{
				"label": "Expected Value",
				"type": "Currency",
				"key": "expected_deal_value",
				"width": "10rem",
			},
			{
				"label": "Practice Area",
				"type": "Link",
				"key": "practice_area",
				"options": "Practice Area",
				"width": "10rem",
			},
			{
				"label": "Assigned Lawyer",
				"type": "Link",
				"key": "assigned_lawyer",
				"options": "Lawyer",
				"width": "10rem",
			},
			{
				"label": "Last Modified",
				"type": "Datetime",
				"key": "modified",
				"width": "8rem",
			},
		]
		rows = [
			"name",
			"organization",
			"deal_owner",
			"status",
			"expected_deal_value",
			"practice_area",
			"assigned_lawyer",
			"client_type",
			"kra_pin",
			"case_type",
			"modified",
		]
		return {"columns": columns, "rows": rows}


# Standalone validation functions for testing
def validate_company_registration(reg_number):
	"""Standalone company registration validation function for testing"""
	if not reg_number:
		return False

	# Basic validation - should be numeric or have specific format
	return bool(re.match(r'^[A-Z0-9\-]+$', reg_number.upper()))