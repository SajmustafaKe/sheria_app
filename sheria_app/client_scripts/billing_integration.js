// Billing Integration Client Scripts

frappe.ui.form.on('Time Entry', {
    refresh: function(frm) {
        // Add billing actions for approved time entries
        if (frm.doc.status === 'Approved' && frm.doc.is_billable && !frm.doc.billed) {
            frm.add_custom_button(__('Generate Invoice'), function() {
                generate_invoice_from_time_entry(frm);
            }, __('Billing'));
        }

        // Show invoice link if billed
        if (frm.doc.billed && frm.doc.invoice_reference) {
            frm.add_custom_button(__('View Invoice'), function() {
                frappe.set_route('Form', 'Sales Invoice', frm.doc.invoice_reference);
            }, __('Billing'));
        }
    }
});

function generate_invoice_from_time_entry(frm) {
    frappe.call({
        method: 'sheria.api.generate_invoice_from_time_entries',
        args: {
            time_entries: [frm.doc.name]
        },
        callback: function(r) {
            if (r.message && r.message.success) {
                frappe.msgprint(__('Invoice generated successfully: {0}', [r.message.invoice_id]));
                frm.reload_doc();
            }
        }
    });
}

// Bulk invoice generation from list view
frappe.listview_settings['Time Entry'] = {
    button: {
        show: function(doc) {
            return doc.status === 'Approved' && doc.is_billable && !doc.billed;
        },
        get_label: function(doc) {
            return __('Generate Invoice');
        },
        get_description: function(doc) {
            return __('Generate invoice for selected time entries');
        },
        action: function(doc) {
            // Get selected items
            let selected = cur_list.get_checked_items();
            if (selected.length === 0) {
                frappe.msgprint(__('Please select time entries to invoice'));
                return;
            }

            let time_entries = selected.map(item => item.name);

            frappe.call({
                method: 'sheria.api.generate_invoice_from_time_entries',
                args: {
                    time_entries: time_entries
                },
                callback: function(r) {
                    if (r.message && r.message.success) {
                        frappe.msgprint(__('Invoice generated successfully: {0}', [r.message.invoice_id]));
                        cur_list.refresh();
                    }
                }
            });
        }
    }
};

// Trust Account Management
frappe.ui.form.on('Trust Account Transaction', {
    refresh: function(frm) {
        // Show current balance
        if (frm.doc.client && !frm.doc.__islocal) {
            frappe.call({
                method: 'sheria.api.get_client_trust_balance',
                args: {
                    client: frm.doc.client
                },
                callback: function(r) {
                    if (r.message) {
                        frm.dashboard.add_indicator(__('Trust Balance: {0}', [frappe.format(r.message.balance, {fieldtype: 'Currency'})]), 'blue');
                    }
                }
            });
        }
    },

    transaction_type: function(frm) {
        // Set balance before for validation
        if (frm.doc.client && frm.doc.transaction_type) {
            frappe.call({
                method: 'sheria.api.get_client_trust_balance',
                args: {
                    client: frm.doc.client
                },
                callback: function(r) {
                    if (r.message) {
                        frm.set_value('balance_before', r.message.balance);
                    }
                }
            });
        }
    }
});

// Client Trust Account Dashboard
frappe.ui.form.on('Client', {
    refresh: function(frm) {
        // Add trust account section
        if (frm.doc.trust_balance !== undefined) {
            frm.dashboard.add_indicator(__('Trust Account Balance: {0}', [frappe.format(frm.doc.trust_balance, {fieldtype: 'Currency'})]), 'green');

            // Add trust account actions
            frm.page.add_menu_item(__('View Trust Statement'), function() {
                view_trust_statement(frm.doc.name);
            });

            frm.page.add_menu_item(__('Add Trust Deposit'), function() {
                add_trust_transaction(frm.doc.name, 'Deposit');
            });

            frm.page.add_menu_item(__('Trust Withdrawal'), function() {
                add_trust_transaction(frm.doc.name, 'Withdrawal');
            });
        }
    }
});

function view_trust_statement(client) {
    frappe.call({
        method: 'sheria.api.get_client_trust_statement',
        args: {
            client: client
        },
        callback: function(r) {
            if (r.message) {
                // Show trust statement in a dialog
                let dialog = new frappe.ui.Dialog({
                    title: __('Trust Account Statement'),
                    fields: [
                        {
                            fieldtype: 'HTML',
                            options: generate_statement_html(r.message)
                        }
                    ]
                });
                dialog.show();
            }
        }
    });
}

function add_trust_transaction(client, type) {
    let dialog = new frappe.ui.Dialog({
        title: __('Add Trust {0}', [type]),
        fields: [
            {
                label: __('Amount'),
                fieldname: 'amount',
                fieldtype: 'Currency',
                reqd: 1
            },
            {
                label: __('Description'),
                fieldname: 'description',
                fieldtype: 'Text',
                reqd: 1
            },
            {
                label: __('Reference'),
                fieldname: 'reference',
                fieldtype: 'Data'
            }
        ],
        primary_action_label: __('Submit'),
        primary_action(values) {
            frappe.call({
                method: 'sheria.api.create_trust_account_transaction',
                args: {
                    client: client,
                    amount: values.amount,
                    transaction_type: type,
                    description: values.description,
                    reference: values.reference
                },
                callback: function(r) {
                    if (r.message && r.message.success) {
                        frappe.msgprint(__('Trust {0} added successfully', [type]));
                        dialog.hide();
                        cur_frm.reload_doc();
                    }
                }
            });
        }
    });
    dialog.show();
}

function generate_statement_html(transactions) {
    let html = `
        <div class="trust-statement">
            <table class="table table-bordered">
                <thead>
                    <tr>
                        <th>Date</th>
                        <th>Type</th>
                        <th>Description</th>
                        <th>Amount</th>
                        <th>Balance</th>
                    </tr>
                </thead>
                <tbody>
    `;

    transactions.forEach(function(transaction) {
        html += `
            <tr>
                <td>${frappe.format(transaction.transaction_date, {fieldtype: 'Date'})}</td>
                <td>${transaction.transaction_type}</td>
                <td>${transaction.description}</td>
                <td>${frappe.format(transaction.amount, {fieldtype: 'Currency'})}</td>
                <td>${frappe.format(transaction.running_balance || transaction.balance_after, {fieldtype: 'Currency'})}</td>
            </tr>
        `;
    });

    html += `
                </tbody>
            </table>
        </div>
    `;

    return html;
}