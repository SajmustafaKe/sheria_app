frappe.ui.form.on('Task', {
    refresh: function(frm) {
        // Set progress bar
        if (frm.doc.progress !== undefined) {
            frm.dashboard.add_progress(__('Progress'), frm.doc.progress + '%', frm.doc.progress);
        }

        // Add custom buttons
        if (frm.doc.status === 'Open' || frm.doc.status === 'In Progress') {
            frm.add_custom_button(__('Mark Complete'), function() {
                frm.set_value('status', 'Completed');
                frm.set_value('progress', 100);
                frm.save();
            });
        }

        if (frm.doc.status === 'Completed') {
            frm.add_custom_button(__('Reopen'), function() {
                frm.set_value('status', 'Open');
                frm.set_value('progress', 0);
                frm.save();
            });
        }
    },

    progress: function(frm) {
        // Update status based on progress
        if (frm.doc.progress === 100 && frm.doc.status !== 'Completed') {
            frm.set_value('status', 'Completed');
        } else if (frm.doc.progress > 0 && frm.doc.progress < 100 && frm.doc.status === 'Open') {
            frm.set_value('status', 'In Progress');
        }
    },

    status: function(frm) {
        // Update progress based on status
        if (frm.doc.status === 'Completed' && frm.doc.progress !== 100) {
            frm.set_value('progress', 100);
        } else if (frm.doc.status === 'Open' && frm.doc.progress > 0) {
            frm.set_value('progress', 0);
        }
    }
});