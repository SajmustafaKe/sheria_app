# Trust Account Ledger
# Copyright (c) 2024, Sheria Legal Technologies
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import getdate
from frappe.model.document import Document

class TrustAccountLedger(Document):
	def autoname(self):
		"""Generate entry ID"""
		if not self.entry_id:
			# Generate unique entry ID
			prefix = "TAL"
			current_year = getdate().year
			# Get the last entry number for this year
			last_entry = frappe.db.sql("""
				SELECT entry_id
				FROM `tabTrust Account Ledger`
				WHERE entry_id LIKE %s
				ORDER BY creation DESC
				LIMIT 1
			""", (f"{prefix}{current_year}%",))

			if last_entry:
				last_num = int(last_entry[0][0].replace(f"{prefix}{current_year}", ""))
				next_num = last_num + 1
			else:
				next_num = 1

			self.entry_id = f"{prefix}{current_year}{next_num:06d}"

	def validate(self):
		"""Validate trust account ledger entry"""
		# Ledger entries are created automatically, so minimal validation
		if not self.client:
			frappe.throw(_("Client is required"))

		if not self.transaction:
			frappe.throw(_("Transaction reference is required"))