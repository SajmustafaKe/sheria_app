// Client Script for Legal CRM Lead
frappe.ui.form.on('Legal CRM Lead', {
    refresh: function(frm) {
        // Add button to open Legal CRM Dashboard
        if (frm.doc.name) {
            frm.add_custom_button(__('Open CRM Dashboard'), function() {
                frappe.msgprint(__('CRM Dashboard feature is available. Please access it from the Sheria workspace.'));
            }, __('View'));
        }
    }
});