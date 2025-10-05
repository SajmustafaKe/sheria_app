# Copyright (c) 2025, Coale Tech and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document

class LegalCRMFormScript(Document):
	def validate(self):
		"""Validate the form script"""
		if self.javascript_code:
			# Basic JavaScript validation
			if "frappe" not in self.javascript_code:
				frappe.msgprint(_("JavaScript code should use Frappe framework functions"),
					alert=True)

		if self.python_code:
			# Basic Python validation
			if "frappe" not in self.python_code:
				frappe.msgprint(_("Python code should use Frappe framework functions"),
					alert=True)

	def on_update(self):
		"""Clear cache when form script is updated"""
		frappe.clear_cache()

@frappe.whitelist()
def get_form_script(doctype_name):
	"""Get active form script for a doctype"""
	scripts = frappe.get_all("Legal CRM Form Script",
		filters={
			"doctype_name": doctype_name,
			"is_active": 1
		},
		fields=["javascript_code", "python_code"]
	)

	if scripts:
		return scripts[0]
	return {}

# Default Legal CRM Lead Form Script
DEFAULT_LEAD_SCRIPT = """
// Legal CRM Lead Form Script
frappe.ui.form.on('Legal CRM Lead', {
    refresh: function(frm) {
        // Add custom buttons
        if (!frm.doc.__islocal) {
            frm.add_custom_button(__('Create Legal Case'), function() {
                frappe.new_doc('Legal Case', {
                    client: frm.doc.name,
                    client_name: frm.doc.lead_name,
                    practice_area: frm.doc.practice_area,
                    court: frm.doc.court
                });
            });
        }

        // Trust balance indicator
        if (frm.doc.trust_balance !== undefined) {
            let color = frm.doc.trust_balance > 0 ? 'green' : 'red';
            frm.dashboard.add_indicator(__('Trust Balance: {0}',
                [format_currency(frm.doc.trust_balance)]), color);
        }
    },

    client_type: function(frm) {
        // Show/hide fields based on client type
        frm.toggle_reqd('first_name', frm.doc.client_type === 'Individual');
        frm.toggle_reqd('organization', frm.doc.client_type === 'Company');
        frm.toggle_reqd('company_registration_number', frm.doc.client_type === 'Company');
        frm.toggle_reqd('id_passport_number', frm.doc.client_type === 'Individual');

        // Refresh form to show changes
        frm.refresh_fields();
    },

    kra_pin: function(frm) {
        // Auto-format KRA PIN
        if (frm.doc.kra_pin) {
            frm.doc.kra_pin = frm.doc.kra_pin.toUpperCase();
            frm.refresh_field('kra_pin');
        }
    },

    practice_area: function(frm) {
        // Filter courts based on practice area
        frm.set_query('court', function() {
            return {
                filters: {
                    practice_area: frm.doc.practice_area
                }
            };
        });
    }
});
"""

# Default Legal CRM Deal Form Script
DEFAULT_DEAL_SCRIPT = """
// Legal CRM Deal Form Script
frappe.ui.form.on('Legal CRM Deal', {
    refresh: function(frm) {
        // Add custom buttons
        if (frm.doc.status === 'Won' && !frm.doc.legal_case) {
            frm.add_custom_button(__('Create Legal Case'), function() {
                frappe.call({
                    method: 'sheria_app.crm_extensions.doctype.legal_crm_deal.legal_crm_deal.create_legal_case_from_deal',
                    args: {
                        deal_name: frm.doc.name
                    },
                    callback: function(r) {
                        if (r.message) {
                            frappe.msgprint(__('Legal Case {0} created', [r.message]));
                            frm.reload_doc();
                        }
                    }
                });
            });
        }

        // Deal value indicator
        if (frm.doc.expected_deal_value) {
            frm.dashboard.add_indicator(__('Expected Value: {0}',
                [format_currency(frm.doc.expected_deal_value)]), 'blue');
        }
    },

    status: function(frm) {
        // Auto-set closed date for won deals
        if (frm.doc.status === 'Won' && !frm.doc.closed_date) {
            frm.set_value('closed_date', frappe.datetime.now_date());
        }
    },

    client_type: function(frm) {
        // Similar to lead script
        frm.toggle_reqd('first_name', frm.doc.client_type === 'Individual');
        frm.toggle_reqd('organization', frm.doc.client_type === 'Company');
    },

    expected_deal_value: function(frm) {
        // Auto-set deal_value if not set
        if (frm.doc.expected_deal_value && !frm.doc.deal_value) {
            frm.set_value('deal_value', frm.doc.expected_deal_value);
        }
    }
});
"""

def create_default_scripts():
	"""Create default form scripts if they don't exist"""
	if not frappe.db.exists("Legal CRM Form Script", "Legal CRM Lead - Default"):
		doc = frappe.new_doc("Legal CRM Form Script")
		doc.script_name = "Legal CRM Lead - Default"
		doc.doctype_name = "Legal CRM Lead"
		doc.javascript_code = DEFAULT_LEAD_SCRIPT
		doc.is_active = 1
		doc.insert(ignore_permissions=True)

	if not frappe.db.exists("Legal CRM Form Script", "Legal CRM Deal - Default"):
		doc = frappe.new_doc("Legal CRM Form Script")
		doc.script_name = "Legal CRM Deal - Default"
		doc.doctype_name = "Legal CRM Deal"
		doc.javascript_code = DEFAULT_DEAL_SCRIPT
		doc.is_active = 1
		doc.insert(ignore_permissions=True)

	frappe.db.commit()