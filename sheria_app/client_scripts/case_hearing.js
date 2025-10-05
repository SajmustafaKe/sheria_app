frappe.ui.form.on('Case Hearing', {
    refresh: function(frm) {
        // Set default status
        if (!frm.doc.status) {
            frm.set_value('status', 'Scheduled');
        }

        // Add reminder button for upcoming hearings
        if (frm.doc.status === 'Scheduled' && frm.doc.hearing_date) {
            let hearing_date = moment(frm.doc.hearing_date);
            let today = moment();

            if (hearing_date.diff(today, 'days') <= 7 && hearing_date.isAfter(today)) {
                frm.add_custom_button(__('Send Reminder'), function() {
                    send_hearing_reminder(frm);
                });
            }
        }

        // Add outcome button for completed hearings
        if (frm.doc.status === 'Scheduled') {
            frm.add_custom_button(__('Mark Completed'), function() {
                frm.set_value('status', 'Completed');
                frm.save();
            });
        }
    },

    hearing_date: function(frm) {
        // Validate hearing date is not in the past
        if (frm.doc.hearing_date) {
            let hearing_date = moment(frm.doc.hearing_date);
            let today = moment().startOf('day');

            if (hearing_date.isBefore(today)) {
                frappe.msgprint(__('Hearing date cannot be in the past'));
                frm.set_value('hearing_date', '');
            }
        }
    },

    status: function(frm) {
        // Set outcome when status changes to completed
        if (frm.doc.status === 'Completed' && !frm.doc.outcome) {
            frappe.prompt([
                {
                    label: 'Outcome',
                    fieldname: 'outcome',
                    fieldtype: 'Select',
                    options: 'Adjourned\nDismissed\nSettled\nVerdict\nPending',
                    reqd: 1
                },
                {
                    label: 'Next Hearing Date',
                    fieldname: 'next_hearing_date',
                    fieldtype: 'Date'
                },
                {
                    label: 'Notes',
                    fieldname: 'notes',
                    fieldtype: 'Text'
                }
            ], function(values) {
                frm.set_value('outcome', values.outcome);
                if (values.next_hearing_date) {
                    frm.set_value('next_hearing_date', values.next_hearing_date);
                }
                if (values.notes) {
                    frm.set_value('notes', values.notes);
                }
                frm.save();
            }, __('Enter Hearing Outcome'), __('Submit'));
        }
    }
});

function send_hearing_reminder(frm) {
    frappe.call({
        method: 'sheria.api.send_hearing_reminder',
        args: {
            hearing_id: frm.doc.name
        },
        callback: function(r) {
            if (r.message && r.message.success) {
                frappe.msgprint(__('Reminder sent successfully'));
            }
        }
    });
}