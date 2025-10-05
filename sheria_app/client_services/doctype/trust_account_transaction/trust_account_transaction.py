# Trust Account Transaction
# Copyright (c) 2024, Sheria Legal Technologies
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import getdate, now
from frappe.model.document import Document

class TrustAccountTransaction(Document):
	def autoname(self):
		"""Generate transaction ID"""
		if not self.transaction_id:
			# Generate unique transaction ID
			prefix = "TAT"
			current_year = getdate().year
			# Get the last transaction number for this year
			last_transaction = frappe.db.sql("""
				SELECT transaction_id
				FROM `tabTrust Account Transaction`
				WHERE transaction_id LIKE %s
				ORDER BY creation DESC
				LIMIT 1
			""", (f"{prefix}{current_year}%",))

			if last_transaction:
				last_num = int(last_transaction[0][0].replace(f"{prefix}{current_year}", ""))
				next_num = last_num + 1
			else:
				next_num = 1

			self.transaction_id = f"{prefix}{current_year}{next_num:06d}"

	def validate(self):
		"""Validate trust account transaction"""
		self.validate_amount()
		self.validate_client()
		self.set_balance_before()

	def before_submit(self):
		"""Set approval details before submission"""
		self.approved_by = frappe.session.user
		self.approval_date = getdate()

	def on_submit(self):
		"""Update client trust balance on submission"""
		self.update_client_balance()

	def on_cancel(self):
		"""Update client trust balance on cancellation"""
		self.update_client_balance(reverse=True)

	def validate_amount(self):
		"""Validate transaction amount"""
		if self.amount <= 0:
			frappe.throw(_("Transaction amount must be greater than zero"))

		# For withdrawals and payments, check available balance
		if self.transaction_type in ["Withdrawal", "Payment"]:
			current_balance = self.get_client_balance()
			if current_balance < self.amount:
				frappe.throw(_("Insufficient trust account balance. Available: {0}").format(
					frappe.utils.fmt_money(current_balance, currency=frappe.defaults.get_global_default("currency"))
				))

	def validate_client(self):
		"""Validate client exists and is active"""
		if not frappe.db.exists("Client", self.client):
			frappe.throw(_("Client not found"))

		client_status = frappe.db.get_value("Client", self.client, "status")
		if client_status != "Active":
			frappe.throw(_("Cannot create transaction for inactive client"))

	def set_balance_before(self):
		"""Set balance before transaction"""
		self.balance_before = self.get_client_balance()

	def update_client_balance(self, reverse=False):
		"""Update client's trust account balance"""
		try:
			# Calculate balance change
			multiplier = -1 if reverse else 1

			if self.transaction_type == "Deposit":
				balance_change = self.amount * multiplier
			elif self.transaction_type in ["Withdrawal", "Payment"]:
				balance_change = -self.amount * multiplier
			elif self.transaction_type == "Adjustment":
				# For adjustments, amount can be positive or negative
				balance_change = self.amount * multiplier
			else:
				return

			# Update balance after
			self.balance_after = self.balance_before + balance_change

			# Update client's trust balance
			current_balance = frappe.db.get_value("Client", self.client, "trust_balance") or 0
			new_balance = current_balance + balance_change

			frappe.db.set_value("Client", self.client, "trust_balance", new_balance)

			# Create ledger entry for audit trail
			self.create_ledger_entry(balance_change, new_balance)

		except Exception as e:
			frappe.log_error(f"Error updating client balance: {str(e)}")
			frappe.throw(_("Failed to update client trust balance"))

	def get_client_balance(self):
		"""Get current client trust balance"""
		try:
			balance = frappe.db.sql("""
				SELECT
					COALESCE(SUM(
						CASE
							WHEN transaction_type = 'Deposit' THEN amount
							WHEN transaction_type IN ('Withdrawal', 'Payment') THEN -amount
							WHEN transaction_type = 'Adjustment' THEN amount
							ELSE 0
						END
					), 0) as balance
				FROM `tabTrust Account Transaction`
				WHERE client = %s
					AND docstatus = 1
					AND name != %s
			""", (self.client, self.name), as_dict=True)

			return balance[0].balance if balance else 0

		except Exception as e:
			frappe.log_error(f"Error getting client balance: {str(e)}")
			return 0

	def create_ledger_entry(self, balance_change, new_balance):
		"""Create trust account ledger entry for audit trail"""
		try:
			ledger_entry = frappe.get_doc({
				"doctype": "Trust Account Ledger",
				"transaction": self.name,
				"client": self.client,
				"transaction_date": self.transaction_date,
				"transaction_type": self.transaction_type,
				"amount": self.amount,
				"balance_change": balance_change,
				"balance_after": new_balance,
				"description": self.description,
				"reference": self.reference
			})
			ledger_entry.insert(ignore_permissions=True)

		except Exception as e:
			frappe.log_error(f"Error creating ledger entry: {str(e)}")

@frappe.whitelist()
def get_client_trust_statement(client, from_date=None, to_date=None):
	"""Get client's trust account statement"""
	try:
		filters = {"client": client, "docstatus": 1}
		date_condition = ""

		if from_date and to_date:
			date_condition = f" AND transaction_date BETWEEN '{from_date}' AND '{to_date}'"
		elif from_date:
			date_condition = f" AND transaction_date >= '{from_date}'"
		elif to_date:
			date_condition = f" AND transaction_date <= '{to_date}'"

		transactions = frappe.db.sql(f"""
			SELECT
				transaction_date,
				transaction_type,
				amount,
				description,
				reference,
				balance_after,
				creation
			FROM `tabTrust Account Transaction`
			WHERE client = %s
				AND docstatus = 1
			{date_condition}
			ORDER BY transaction_date ASC, creation ASC
		""", (client,), as_dict=True)

		# Calculate running balance
		running_balance = 0
		for transaction in transactions:
			if transaction.transaction_type == "Deposit":
				running_balance += transaction.amount
			elif transaction.transaction_type in ["Withdrawal", "Payment"]:
				running_balance -= transaction.amount
			elif transaction.transaction_type == "Adjustment":
				running_balance += transaction.amount

			transaction.running_balance = running_balance

		return transactions

	except Exception as e:
		frappe.log_error(f"Error getting trust statement: {str(e)}")
		return {"error": "Failed to get trust statement"}