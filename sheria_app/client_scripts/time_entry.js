frappe.ui.form.on('Time Entry', {
    refresh: function(frm) {
        // Set employee if not set
        if (!frm.doc.employee && frappe.session.user) {
            frm.set_value('employee', frappe.session.user);
        }

        // Calculate total amount on refresh
        calculate_total(frm);
    },

    start_time: function(frm) {
        calculate_hours(frm);
    },

    end_time: function(frm) {
        calculate_hours(frm);
    },

    hours: function(frm) {
        calculate_total(frm);
    },

    billing_rate: function(frm) {
        calculate_total(frm);
    },

    billable: function(frm) {
        calculate_total(frm);
    }
});

function calculate_hours(frm) {
    if (frm.doc.start_time && frm.doc.end_time) {
        let start = moment(frm.doc.start_time, 'HH:mm:ss');
        let end = moment(frm.doc.end_time, 'HH:mm:ss');

        if (end.isBefore(start)) {
            end.add(1, 'day'); // Handle overnight work
        }

        let duration = moment.duration(end.diff(start));
        let hours = duration.asHours();

        frm.set_value('hours', hours);
    }
}

function calculate_total(frm) {
    if (frm.doc.hours && frm.doc.billing_rate && frm.doc.billable) {
        let total = frm.doc.hours * frm.doc.billing_rate;
        frm.set_value('total_amount', total);
    } else {
        frm.set_value('total_amount', 0);
    }
}