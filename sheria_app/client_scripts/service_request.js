frappe.ui.form.on('Service Request', {
    refresh: function(frm) {
        // Set default values
        if (!frm.doc.request_date) {
            frm.set_value('request_date', frappe.datetime.get_today());
        }

        if (!frm.doc.status) {
            frm.set_value('status', 'Draft');
        }

        // Add custom buttons based on status
        if (frm.doc.status === 'Draft') {
            frm.add_custom_button(__('Submit Request'), function() {
                frm.set_value('status', 'Submitted');
                frm.save();
            });
        }

        if (frm.doc.status === 'Under Review' && frappe.user.has_role('Legal Admin')) {
            frm.add_custom_button(__('Approve'), function() {
                approve_request(frm);
            }, __('Actions'));

            frm.add_custom_button(__('Reject'), function() {
                reject_request(frm);
            }, __('Actions'));
        }

        // Show service details
        if (frm.doc.service) {
            show_service_details(frm);
        }
    },

    service: function(frm) {
        // Load service details when service is selected
        if (frm.doc.service) {
            show_service_details(frm);
        }
    },

    preferred_date: function(frm) {
        // Validate preferred date is not in the past
        if (frm.doc.preferred_date) {
            let preferred_date = moment(frm.doc.preferred_date);
            let today = moment().startOf('day');

            if (preferred_date.isBefore(today)) {
                frappe.msgprint(__('Preferred date cannot be in the past'));
                frm.set_value('preferred_date', '');
            }
        }
    }
});

function show_service_details(frm) {
    frappe.call({
        method: 'frappe.client.get',
        args: {
            doctype: 'Legal Service',
            name: frm.doc.service
        },
        callback: function(r) {
            if (r.message) {
                let service = r.message;
                frm.dashboard.add_section([
                    {
                        label: __('Service Details'),
                        fieldtype: 'HTML',
                        options: `
                            <div class="service-details">
                                <p><strong>Category:</strong> ${service.category || ''}</p>
                                <p><strong>Price:</strong> ${service.currency || 'KES'} ${service.price || 0}</p>
                                <p><strong>Duration:</strong> ${service.duration || 0} ${service.duration_unit || 'Days'}</p>
                                <p><strong>Description:</strong> ${service.description || ''}</p>
                            </div>
                        `
                    }
                ]);
            }
        }
    });
}

function approve_request(frm) {
    frappe.prompt([
        {
            label: 'Approval Date',
            fieldname: 'approved_date',
            fieldtype: 'Date',
            default: frappe.datetime.get_today(),
            reqd: 1
        }
    ], function(values) {
        frm.set_value('status', 'Approved');
        frm.set_value('approved_date', values.approved_date);
        frm.save();
    }, __('Approve Service Request'), __('Approve'));
}

function reject_request(frm) {
    frappe.prompt([
        {
            label: 'Rejection Reason',
            fieldname: 'rejection_reason',
            fieldtype: 'Text',
            reqd: 1
        }
    ], function(values) {
        frm.set_value('status', 'Rejected');
        frm.set_value('rejection_reason', values.rejection_reason);
        frm.save();
    }, __('Reject Service Request'), __('Reject'));
}