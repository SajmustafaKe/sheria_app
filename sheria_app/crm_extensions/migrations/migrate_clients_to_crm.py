# Migration script to migrate existing Client records to Legal CRM Leads
# Run this after installing the CRM extensions
# Note: Client doctype has been deprecated and removed. This script is kept for backward compatibility.

import frappe
from frappe import _

def migrate_clients_to_crm_leads():
	"""Migrate existing Client records to Legal CRM Lead records"""

	# Check if Client doctype exists
	if not frappe.db.exists("DocType", "Client"):
		frappe.msgprint(_("Client doctype not found. Migration not needed."))
		return

	# Get all existing clients
	clients = frappe.get_all("Client",
		fields=["name", "client_name", "client_type", "status", "email_address",
				"phone_number", "kra_pin", "id_passport_number", "company_registration_number",
				"practice_area", "court", "assigned_lawyer", "case_priority",
				"billing_address", "payment_terms", "credit_limit", "trust_balance",
				"confidentiality_agreement_signed", "marketing_consent"],
		filters={"migrated_to_crm": ["!=", 1]}  # Only migrate unmigrated clients
	)

	if not clients:
		frappe.msgprint(_("No Client records found to migrate."))
		return

	migrated_count = 0
	skipped_count = 0

	for client in clients:
		try:
			# Check if lead already exists for this client
			existing_lead = frappe.db.exists("Legal CRM Lead",
				{"kra_pin": client.kra_pin}) if client.kra_pin else None

			if existing_lead:
				frappe.db.set_value("Client", client.name, "migrated_to_crm", 1)
				skipped_count += 1
				continue

			# Create new Legal CRM Lead
			lead = frappe.new_doc("Legal CRM Lead")

			# Map client fields to lead fields
			lead.update({
				"lead_name": client.client_name,
				"client_type": client.client_type,
				"status": "Qualified" if client.status == "Active" else "New",
				"email": client.email_address,
				"phone": client.phone_number,
				"kra_pin": client.kra_pin,
				"id_passport_number": client.id_passport_number,
				"company_registration_number": client.company_registration_number,
				"practice_area": client.practice_area,
				"court": client.court,
				"case_priority": client.case_priority,
				"confidentiality_agreement_signed": client.confidentiality_agreement_signed,
				"marketing_consent": client.marketing_consent,
				"billing_address": client.billing_address,
				"payment_terms": client.payment_terms,
				"credit_limit": client.credit_limit,
				"trust_balance": client.trust_balance,
			})

			# Set organization for company clients
			if client.client_type == "Company":
				lead.organization = client.client_name
				lead.lead_name = client.client_name

			# Set first/last name for individual clients
			elif client.client_type == "Individual":
				name_parts = client.client_name.split(" ", 1)
				lead.first_name = name_parts[0]
				if len(name_parts) > 1:
					lead.last_name = name_parts[1]

			# Set default lead owner (could be assigned_lawyer or a default user)
			if client.assigned_lawyer:
				lead.lead_owner = client.assigned_lawyer

			lead.flags.ignore_mandatory = True
			lead.insert(ignore_permissions=True)

			# Mark client as migrated
			frappe.db.set_value("Client", client.name, "migrated_to_crm", 1)

			migrated_count += 1
			frappe.db.commit()

		except Exception as e:
			frappe.log_error(f"Failed to migrate client {client.name}: {str(e)}",
				"Client Migration Error")
			continue

	# Log migration results
	frappe.msgprint(_(f"Migration completed: {migrated_count} clients migrated, {skipped_count} skipped"))

	return {"migrated": migrated_count, "skipped": skipped_count}

def add_migration_field():
	"""Add migration tracking field to Client doctype"""
	if not frappe.db.has_column("Client", "migrated_to_crm"):
		frappe.db.add_column("Client", "migrated_to_crm", "Check", default=0)
		frappe.db.commit()

# Execute migration
if __name__ == "__main__":
	add_migration_field()
	migrate_clients_to_crm_leads()