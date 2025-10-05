// Sheria App Main JavaScript
// Copyright (c) 2024, Sheria Legal Technologies
// For license information, please see license.txt

frappe.provide('sheria');

// Initialize Sheria App
$(document).ready(function() {
	// Add custom styles and functionality
	sheria.init();
});

sheria.init = function() {
	// Initialize legal dashboard
	if (frappe.get_route()[0] === 'legal-dashboard') {
		sheria.init_legal_dashboard();
	}

	// Initialize client portal
	if (frappe.get_route()[0] === 'client-portal') {
		sheria.init_client_portal();
	}

	// Add custom keyboard shortcuts
	sheria.init_keyboard_shortcuts();

	// Initialize real-time notifications
	sheria.init_notifications();
};

sheria.init_legal_dashboard = function() {
	// Initialize dashboard widgets
	sheria.load_case_statistics();
	sheria.load_upcoming_hearings();
	sheria.load_recent_activities();
};

sheria.init_client_portal = function() {
	// Initialize client portal features
	sheria.load_client_services();
	sheria.load_service_requests();
};

sheria.init_keyboard_shortcuts = function() {
	// Add keyboard shortcuts for legal operations
	$(document).on('keydown', function(e) {
		// Ctrl+Shift+N: New Case
		if (e.ctrlKey && e.shiftKey && e.keyCode === 78) {
			e.preventDefault();
			sheria.new_case();
		}
		// Ctrl+Shift+S: New Service Request
		if (e.ctrlKey && e.shiftKey && e.keyCode === 83) {
			e.preventDefault();
			sheria.new_service_request();
		}
	});
};

sheria.init_notifications = function() {
	// Initialize real-time notifications for legal updates
	if (frappe.socketio && frappe.socketio.socket) {
		frappe.socketio.socket.on('legal_update', function(data) {
			sheria.show_notification(data);
		});
	}
};

sheria.new_case = function() {
	frappe.new_doc('Legal Case');
};

sheria.new_service_request = function() {
	frappe.new_doc('Service Request');
};

sheria.load_case_statistics = function() {
	// Load case statistics for dashboard
	frappe.call({
		method: 'sheria.api.get_case_statistics',
		callback: function(r) {
			if (r.message) {
				sheria.render_case_stats(r.message);
			}
		}
	});
};

sheria.load_upcoming_hearings = function() {
	// Load upcoming hearings
	frappe.call({
		method: 'sheria.api.get_upcoming_hearings',
		callback: function(r) {
			if (r.message) {
				sheria.render_upcoming_hearings(r.message);
			}
		}
	});
};

sheria.load_recent_activities = function() {
	// Load recent case activities
	frappe.call({
		method: 'sheria.api.get_recent_activities',
		callback: function(r) {
			if (r.message) {
				sheria.render_recent_activities(r.message);
			}
		}
	});
};

sheria.load_client_services = function() {
	// Load client services
	frappe.call({
		method: 'sheria.api.get_client_services',
		callback: function(r) {
			if (r.message) {
				sheria.render_client_services(r.message);
			}
		}
	});
};

sheria.load_service_requests = function() {
	// Load service requests
	frappe.call({
		method: 'sheria.api.get_service_requests',
		callback: function(r) {
			if (r.message) {
				sheria.render_service_requests(r.message);
			}
		}
	});
};

sheria.show_notification = function(data) {
	// Show notification for legal updates
	frappe.show_alert({
		message: data.message,
		indicator: data.indicator || 'blue'
	}, 5);
};

sheria.render_case_stats = function(data) {
	// Render case statistics on dashboard
	let html = `
		<div class="row">
			<div class="col-md-3">
				<div class="card">
					<div class="card-body text-center">
						<h3 class="text-primary">${data.total_cases || 0}</h3>
						<p>Total Cases</p>
					</div>
				</div>
			</div>
			<div class="col-md-3">
				<div class="card">
					<div class="card-body text-center">
						<h3 class="text-success">${data.active_cases || 0}</h3>
						<p>Active Cases</p>
					</div>
				</div>
			</div>
			<div class="col-md-3">
				<div class="card">
					<div class="card-body text-center">
						<h3 class="text-warning">${data.pending_cases || 0}</h3>
						<p>Pending Cases</p>
					</div>
				</div>
			</div>
			<div class="col-md-3">
				<div class="card">
					<div class="card-body text-center">
						<h3 class="text-info">${data.closed_cases || 0}</h3>
						<p>Closed Cases</p>
					</div>
				</div>
			</div>
		</div>
	`;

	$('#case-statistics').html(html);
};

sheria.render_upcoming_hearings = function(data) {
	// Render upcoming hearings
	let html = '<div class="list-group">';
	data.forEach(function(hearing) {
		html += `
			<div class="list-group-item">
				<h6 class="mb-1">${hearing.case_title}</h6>
				<p class="mb-1">${hearing.court} - ${hearing.hearing_date}</p>
				<small class="text-muted">${hearing.judge}</small>
			</div>
		`;
	});
	html += '</div>';

	$('#upcoming-hearings').html(html);
};

sheria.render_recent_activities = function(data) {
	// Render recent activities
	let html = '<div class="timeline">';
	data.forEach(function(activity) {
		html += `
			<div class="timeline-item">
				<div class="timeline-marker"></div>
				<div class="timeline-content">
					<h6>${activity.activity}</h6>
					<p>${activity.description}</p>
					<small class="text-muted">${activity.timestamp}</small>
				</div>
			</div>
		`;
	});
	html += '</div>';

	$('#recent-activities').html(html);
};

sheria.render_client_services = function(data) {
	// Render client services
	let html = '<div class="row">';
	data.forEach(function(service) {
		html += `
			<div class="col-md-4 mb-3">
				<div class="card h-100">
					<div class="card-body">
						<h5 class="card-title">${service.service_name}</h5>
						<p class="card-text">${service.description}</p>
						<p class="text-primary font-weight-bold">KES ${service.price}</p>
						<button class="btn btn-primary btn-sm" onclick="sheria.request_service('${service.name}')">
							Request Service
						</button>
					</div>
				</div>
			</div>
		`;
	});
	html += '</div>';

	$('#client-services').html(html);
};

sheria.render_service_requests = function(data) {
	// Render service requests
	let html = '<div class="list-group">';
	data.forEach(function(request) {
		html += `
			<div class="list-group-item">
				<div class="d-flex w-100 justify-content-between">
					<h6 class="mb-1">${request.service_name}</h6>
					<small class="text-muted">${request.status}</small>
				</div>
				<p class="mb-1">${request.description}</p>
				<small class="text-muted">Requested on ${request.request_date}</small>
			</div>
		`;
	});
	html += '</div>';

	$('#service-requests').html(html);
};

sheria.request_service = function(service_name) {
	// Request a legal service
	frappe.call({
		method: 'sheria.api.request_service',
		args: {
			service: service_name
		},
		callback: function(r) {
			if (r.message) {
				frappe.show_alert({
					message: 'Service request submitted successfully',
					indicator: 'green'
				});
				sheria.load_service_requests();
			}
		}
	});
};