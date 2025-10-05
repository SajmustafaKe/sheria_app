# Sheria App Web Pages Module
# Copyright (c) 2024, Coale Tech
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.website.utils import get_home_page

def get_web_page_config():
	"""Get web page configuration for Sheria app"""
	return {
		"legal-services": {
			"name": "legal-services",
			"title": _("Legal Services"),
			"route": "/legal-services",
			"published": 1,
			"content_type": "Page Builder",
			"page_name": "Legal Services",
			"meta_title": _("Professional Legal Services - Sheria"),
			"meta_description": _("Comprehensive legal services for individuals and businesses in Kenya. Expert lawyers, consultations, and legal solutions."),
			"meta_keywords": "legal services, lawyers Kenya, legal consultation, law firm",
			"content": get_legal_services_content(),
			"javascript": get_legal_services_js(),
			"css": get_legal_services_css()
		},
		"service-request": {
			"name": "service-request",
			"title": _("Request Legal Service"),
			"route": "/service-request",
			"published": 1,
			"content_type": "Page Builder",
			"page_name": "Service Request",
			"meta_title": _("Request Legal Service - Sheria"),
			"meta_description": _("Submit your legal service request online. Get professional legal assistance for your needs."),
			"meta_keywords": "legal service request, legal consultation, law firm services",
			"content": get_service_request_content(),
			"javascript": get_service_request_js(),
			"css": get_service_request_css()
		},
		"client-portal": {
			"name": "client-portal",
			"title": _("Client Portal"),
			"route": "/client-portal",
			"published": 1,
			"content_type": "Page Builder",
			"page_name": "Client Portal",
			"meta_title": _("Client Portal - Sheria"),
			"meta_description": _("Access your legal case information, documents, and communicate with your lawyer."),
			"meta_keywords": "client portal, legal case tracking, lawyer communication",
			"content": get_client_portal_content(),
			"javascript": get_client_portal_js(),
			"css": get_client_portal_css()
		},
		"legal-resources": {
			"name": "legal-resources",
			"title": _("Legal Resources"),
			"route": "/legal-resources",
			"published": 1,
			"content_type": "Page Builder",
			"page_name": "Legal Resources",
			"meta_title": _("Legal Resources - Sheria"),
			"meta_description": _("Access legal resources, articles, and information to help you understand your rights."),
			"meta_keywords": "legal resources, legal articles, legal information, Kenya law",
			"content": get_legal_resources_content(),
			"javascript": get_legal_resources_js(),
			"css": get_legal_resources_css()
		}
	}

def get_legal_services_content():
	"""Get content for legal services page"""
	return """
<div class="legal-services-page">
	<section class="hero-section">
		<div class="container">
			<h1>Professional Legal Services</h1>
			<p>Comprehensive legal solutions for individuals and businesses in Kenya</p>
			<a href="/service-request" class="btn btn-primary">Request Service</a>
		</div>
	</section>

	<section class="services-section">
		<div class="container">
			<h2>Our Legal Services</h2>
			<div class="services-grid" id="services-grid">
				<!-- Services will be loaded dynamically -->
			</div>
		</div>
	</section>

	<section class="why-choose-us">
		<div class="container">
			<h2>Why Choose Sheria?</h2>
			<div class="features-grid">
				<div class="feature-item">
					<h3>Expert Lawyers</h3>
					<p>Qualified and experienced legal professionals</p>
				</div>
				<div class="feature-item">
					<h3>Modern Technology</h3>
					<p>Advanced case management and client portal</p>
				</div>
				<div class="feature-item">
					<h3>Client Focused</h3>
					<p>Dedicated to providing exceptional service</p>
				</div>
				<div class="feature-item">
					<h3>Affordable Rates</h3>
					<p>Competitive pricing with transparent billing</p>
				</div>
			</div>
		</div>
	</section>

	<section class="contact-section">
		<div class="container">
			<h2>Get Started Today</h2>
			<p>Ready to get the legal help you need?</p>
			<a href="/service-request" class="btn btn-secondary">Contact Us</a>
		</div>
	</section>
</div>
"""

def get_legal_services_js():
	"""Get JavaScript for legal services page"""
	return """
// Legal Services Page JavaScript
frappe.ready(function() {
	load_services();
});

function load_services() {
	frappe.call({
		method: 'sheria_app.api.get_published_services',
		callback: function(r) {
			if (r.message) {
				render_services(r.message);
			}
		}
	});
}

function render_services(services) {
	const grid = document.getElementById('services-grid');
	grid.innerHTML = '';

	services.forEach(service => {
		const serviceCard = `
			<div class="service-card">
				<h3>${service.service_name}</h3>
				<p>${service.description}</p>
				<div class="service-meta">
					<span class="category">${service.category_name}</span>
					<span class="price">From KES ${service.base_price}</span>
				</div>
				<a href="/service-request?service=${service.name}" class="btn btn-outline">Request Service</a>
			</div>
		`;
		grid.innerHTML += serviceCard;
	});
}
"""

def get_legal_services_css():
	"""Get CSS for legal services page"""
	return """
/* Legal Services Page Styles */
.legal-services-page .hero-section {
	background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
	color: white;
	padding: 80px 0;
	text-align: center;
}

.legal-services-page .hero-section h1 {
	font-size: 3rem;
	margin-bottom: 1rem;
}

.legal-services-page .hero-section p {
	font-size: 1.2rem;
	margin-bottom: 2rem;
}

.services-section {
	padding: 80px 0;
	background: #f8f9fa;
}

.services-section h2 {
	text-align: center;
	margin-bottom: 3rem;
	color: #333;
}

.services-grid {
	display: grid;
	grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
	gap: 2rem;
}

.service-card {
	background: white;
	padding: 2rem;
	border-radius: 8px;
	box-shadow: 0 2px 10px rgba(0,0,0,0.1);
	transition: transform 0.3s ease;
}

.service-card:hover {
	transform: translateY(-5px);
}

.service-card h3 {
	color: #333;
	margin-bottom: 1rem;
}

.service-card p {
	color: #666;
	margin-bottom: 1.5rem;
	line-height: 1.6;
}

.service-meta {
	display: flex;
	justify-content: space-between;
	align-items: center;
	margin-bottom: 1.5rem;
}

.category {
	background: #e3f2fd;
	color: #1976d2;
	padding: 0.25rem 0.75rem;
	border-radius: 20px;
	font-size: 0.875rem;
}

.price {
	font-weight: bold;
	color: #4caf50;
}

.why-choose-us {
	padding: 80px 0;
}

.why-choose-us h2 {
	text-align: center;
	margin-bottom: 3rem;
	color: #333;
}

.features-grid {
	display: grid;
	grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
	gap: 2rem;
}

.feature-item {
	text-align: center;
	padding: 2rem;
	background: white;
	border-radius: 8px;
	box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.feature-item h3 {
	color: #333;
	margin-bottom: 1rem;
}

.feature-item p {
	color: #666;
	line-height: 1.6;
}

.contact-section {
	padding: 80px 0;
	background: #667eea;
	color: white;
	text-align: center;
}

.contact-section h2 {
	margin-bottom: 1rem;
}

.contact-section p {
	margin-bottom: 2rem;
	font-size: 1.1rem;
}

.btn {
	display: inline-block;
	padding: 12px 30px;
	border-radius: 5px;
	text-decoration: none;
	font-weight: 500;
	transition: all 0.3s ease;
	cursor: pointer;
	border: none;
}

.btn-primary {
	background: #4caf50;
	color: white;
}

.btn-primary:hover {
	background: #45a049;
}

.btn-secondary {
	background: white;
	color: #667eea;
}

.btn-secondary:hover {
	background: #f8f9fa;
}

.btn-outline {
	border: 2px solid #667eea;
	color: #667eea;
	background: transparent;
}

.btn-outline:hover {
	background: #667eea;
	color: white;
}
"""

def get_service_request_content():
	"""Get content for service request page"""
	return """
<div class="service-request-page">
	<section class="request-section">
		<div class="container">
			<h1>Request Legal Service</h1>
			<p>Fill out the form below to submit your legal service request</p>

			<div class="request-form-container">
				<form id="service-request-form" class="request-form">
					<div class="form-group">
						<label for="service_type">Service Type *</label>
						<select id="service_type" name="service_type" required>
							<option value="">Select Service Type</option>
						</select>
					</div>

					<div class="form-group">
						<label for="subject">Subject *</label>
						<input type="text" id="subject" name="subject" required
							   placeholder="Brief description of your legal matter">
					</div>

					<div class="form-group">
						<label for="description">Description *</label>
						<textarea id="description" name="description" rows="5" required
								  placeholder="Please provide detailed information about your legal matter"></textarea>
					</div>

					<div class="form-row">
						<div class="form-group">
							<label for="client_name">Full Name *</label>
							<input type="text" id="client_name" name="client_name" required>
						</div>
						<div class="form-group">
							<label for="email">Email Address *</label>
							<input type="email" id="email" name="email" required>
						</div>
					</div>

					<div class="form-row">
						<div class="form-group">
							<label for="phone">Phone Number *</label>
							<input type="tel" id="phone" name="phone" required>
						</div>
						<div class="form-group">
							<label for="priority">Priority</label>
							<select id="priority" name="priority">
								<option value="Low">Low</option>
								<option value="Medium" selected>Medium</option>
								<option value="High">High</option>
								<option value="Urgent">Urgent</option>
							</select>
						</div>
					</div>

					<div class="form-group">
						<label for="attachments">Attachments</label>
						<input type="file" id="attachments" name="attachments" multiple
							   accept=".pdf,.doc,.docx,.jpg,.jpeg,.png">
						<small>Upload relevant documents (PDF, DOC, Images)</small>
					</div>

					<div class="form-group checkbox-group">
						<label class="checkbox-label">
							<input type="checkbox" id="terms" name="terms" required>
							<span class="checkmark"></span>
							I agree to the <a href="/terms" target="_blank">Terms of Service</a> and <a href="/privacy" target="_blank">Privacy Policy</a>
						</label>
					</div>

					<button type="submit" class="btn btn-primary btn-block">Submit Request</button>
				</form>
			</div>
		</div>
	</section>
</div>
"""

def get_service_request_js():
	"""Get JavaScript for service request page"""
	return """
// Service Request Page JavaScript
frappe.ready(function() {
	load_service_types();
	setup_form_submission();
});

function load_service_types() {
	frappe.call({
		method: 'sheria_app.api.get_service_types',
		callback: function(r) {
			if (r.message) {
				const select = document.getElementById('service_type');
				r.message.forEach(service => {
					const option = document.createElement('option');
					option.value = service.name;
					option.textContent = service.service_name;
					select.appendChild(option);
				});
			}
		}
	});
}

function setup_form_submission() {
	const form = document.getElementById('service-request-form');

	form.addEventListener('submit', function(e) {
		e.preventDefault();

		if (!validate_form()) {
			return;
		}

		const formData = new FormData(form);

		// Show loading state
		const submitBtn = form.querySelector('button[type="submit"]');
		const originalText = submitBtn.textContent;
		submitBtn.textContent = 'Submitting...';
		submitBtn.disabled = true;

		frappe.call({
			method: 'sheria_app.api.submit_service_request',
			args: {
				service_type: formData.get('service_type'),
				subject: formData.get('subject'),
				description: formData.get('description'),
				client_name: formData.get('client_name'),
				email: formData.get('email'),
				phone: formData.get('phone'),
				priority: formData.get('priority')
			},
			callback: function(r) {
				submitBtn.textContent = originalText;
				submitBtn.disabled = false;

				if (r.message && r.message.success) {
					show_success_message('Service request submitted successfully! We will contact you soon.');
					form.reset();
				} else {
					show_error_message(r.message ? r.message.message : 'Error submitting request');
				}
			}
		});
	});
}

function validate_form() {
	const required_fields = ['service_type', 'subject', 'description', 'client_name', 'email', 'phone'];
	let is_valid = true;

	required_fields.forEach(field => {
		const element = document.getElementById(field);
		if (!element.value.trim()) {
			element.classList.add('error');
			is_valid = false;
		} else {
			element.classList.remove('error');
		}
	});

	const email = document.getElementById('email');
	const email_regex = /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/;
	if (email.value && !email_regex.test(email.value)) {
		email.classList.add('error');
		is_valid = false;
	}

	const terms = document.getElementById('terms');
	if (!terms.checked) {
		terms.closest('.checkbox-label').classList.add('error');
		is_valid = false;
	} else {
		terms.closest('.checkbox-label').classList.remove('error');
	}

	return is_valid;
}

function show_success_message(message) {
	show_message(message, 'success');
}

function show_error_message(message) {
	show_message(message, 'error');
}

function show_message(message, type) {
	// Remove existing messages
	const existing = document.querySelector('.message');
	if (existing) existing.remove();

	const messageDiv = document.createElement('div');
	messageDiv.className = `message ${type}`;
	messageDiv.textContent = message;

	const container = document.querySelector('.request-form-container');
	container.insertBefore(messageDiv, container.firstChild);

	setTimeout(() => messageDiv.remove(), 5000);
}
"""

def get_service_request_css():
	"""Get CSS for service request page"""
	return """
/* Service Request Page Styles */
.service-request-page {
	padding: 40px 0;
	background: #f8f9fa;
}

.request-section {
	max-width: 800px;
	margin: 0 auto;
	padding: 0 20px;
}

.request-section h1 {
	text-align: center;
	color: #333;
	margin-bottom: 1rem;
}

.request-section > p {
	text-align: center;
	color: #666;
	margin-bottom: 3rem;
}

.request-form-container {
	background: white;
	padding: 3rem;
	border-radius: 8px;
	box-shadow: 0 2px 20px rgba(0,0,0,0.1);
}

.request-form .form-group {
	margin-bottom: 1.5rem;
}

.request-form label {
	display: block;
	margin-bottom: 0.5rem;
	color: #333;
	font-weight: 500;
}

.request-form input,
.request-form select,
.request-form textarea {
	width: 100%;
	padding: 12px;
	border: 2px solid #e1e5e9;
	border-radius: 5px;
	font-size: 1rem;
	transition: border-color 0.3s ease;
}

.request-form input:focus,
.request-form select:focus,
.request-form textarea:focus {
	outline: none;
	border-color: #667eea;
}

.request-form .form-row {
	display: grid;
	grid-template-columns: 1fr 1fr;
	gap: 1rem;
}

.request-form textarea {
	resize: vertical;
	min-height: 120px;
}

.request-form .checkbox-group {
	margin-bottom: 2rem;
}

.checkbox-label {
	display: flex;
	align-items: center;
	cursor: pointer;
	font-weight: normal;
}

.checkbox-label input[type="checkbox"] {
	margin-right: 10px;
}

.checkbox-label a {
	color: #667eea;
	text-decoration: none;
}

.checkbox-label a:hover {
	text-decoration: underline;
}

.btn-block {
	width: 100%;
	padding: 15px;
	font-size: 1.1rem;
}

.message {
	padding: 1rem;
	border-radius: 5px;
	margin-bottom: 1rem;
	font-weight: 500;
}

.message.success {
	background: #d4edda;
	color: #155724;
	border: 1px solid #c3e6cb;
}

.message.error {
	background: #f8d7da;
	color: #721c24;
	border: 1px solid #f5c6cb;
}

.error {
	border-color: #dc3545 !important;
}

small {
	display: block;
	margin-top: 0.25rem;
	color: #666;
	font-size: 0.875rem;
}
"""

def get_client_portal_content():
	"""Get content for client portal page"""
	return """
<div class="client-portal-page">
	<section class="portal-header">
		<div class="container">
			<h1>Client Portal</h1>
			<p>Access your legal case information and communicate with your lawyer</p>
		</div>
	</section>

	<section class="portal-content">
		<div class="container">
			<div class="portal-login" id="portal-login">
				<h2>Client Login</h2>
				<form id="login-form" class="login-form">
					<div class="form-group">
						<label for="login_email">Email Address</label>
						<input type="email" id="login_email" name="email" required>
					</div>
					<div class="form-group">
						<label for="login_password">Access Code</label>
						<input type="password" id="login_password" name="password" required>
					</div>
					<button type="submit" class="btn btn-primary">Login</button>
				</form>
				<p class="login-help">
					Don't have access? Contact your lawyer for login credentials.
				</p>
			</div>

			<div class="portal-dashboard" id="portal-dashboard" style="display: none;">
				<div class="dashboard-header">
					<h2>Welcome, <span id="client-name"></span></h2>
					<button id="logout-btn" class="btn btn-outline">Logout</button>
				</div>

				<div class="dashboard-grid">
					<div class="dashboard-card">
						<h3>My Cases</h3>
						<div id="cases-list" class="cases-list">
							<!-- Cases will be loaded here -->
						</div>
					</div>

					<div class="dashboard-card">
						<h3>Recent Documents</h3>
						<div id="documents-list" class="documents-list">
							<!-- Documents will be loaded here -->
						</div>
					</div>

					<div class="dashboard-card">
						<h3>Upcoming Hearings</h3>
						<div id="hearings-list" class="hearings-list">
							<!-- Hearings will be loaded here -->
						</div>
					</div>

					<div class="dashboard-card">
						<h3>Messages</h3>
						<div id="messages-list" class="messages-list">
							<!-- Messages will be loaded here -->
						</div>
						<button id="new-message-btn" class="btn btn-secondary">Send Message</button>
					</div>
				</div>
			</div>
		</div>
	</section>
</div>
"""

def get_client_portal_js():
	"""Get JavaScript for client portal page"""
	return """
// Client Portal Page JavaScript
frappe.ready(function() {
	setup_portal_login();
	setup_portal_logout();
	setup_new_message();
});

function setup_portal_login() {
	const loginForm = document.getElementById('login-form');

	loginForm.addEventListener('submit', function(e) {
		e.preventDefault();

		const email = document.getElementById('login_email').value;
		const password = document.getElementById('login_password').value;

		frappe.call({
			method: 'sheria_app.api.client_portal_login',
			args: { email: email, password: password },
			callback: function(r) {
				if (r.message && r.message.success) {
					show_portal_dashboard(r.message.client_data);
				} else {
					show_error_message(r.message ? r.message.message : 'Login failed');
				}
			}
		});
	});
}

function setup_portal_logout() {
	document.getElementById('logout-btn').addEventListener('click', function() {
		document.getElementById('portal-login').style.display = 'block';
		document.getElementById('portal-dashboard').style.display = 'none';
		document.getElementById('login-form').reset();
	});
}

function setup_new_message() {
	document.getElementById('new-message-btn').addEventListener('click', function() {
		const subject = prompt('Message Subject:');
		if (subject) {
			const message = prompt('Message:');
			if (message) {
				send_message(subject, message);
			}
		}
	});
}

function show_portal_dashboard(client_data) {
	document.getElementById('portal-login').style.display = 'none';
	document.getElementById('portal-dashboard').style.display = 'block';
	document.getElementById('client-name').textContent = client_data.client_name;

	load_client_cases(client_data.client_id);
	load_client_documents(client_data.client_id);
	load_client_hearings(client_data.client_id);
	load_client_messages(client_data.client_id);
}

function load_client_cases(client_id) {
	frappe.call({
		method: 'sheria_app.api.get_client_cases',
		args: { client_id: client_id },
		callback: function(r) {
			if (r.message) {
				render_cases(r.message);
			}
		}
	});
}

function load_client_documents(client_id) {
	frappe.call({
		method: 'sheria_app.api.get_client_documents',
		args: { client_id: client_id },
		callback: function(r) {
			if (r.message) {
				render_documents(r.message);
			}
		}
	});
}

function load_client_hearings(client_id) {
	frappe.call({
		method: 'sheria_app.api.get_client_hearings',
		args: { client_id: client_id },
		callback: function(r) {
			if (r.message) {
				render_hearings(r.message);
			}
		}
	});
}

function load_client_messages(client_id) {
	frappe.call({
		method: 'sheria_app.api.get_client_messages',
		args: { client_id: client_id },
		callback: function(r) {
			if (r.message) {
				render_messages(r.message);
			}
		}
	});
}

function render_cases(cases) {
	const container = document.getElementById('cases-list');
	container.innerHTML = '';

	if (cases.length === 0) {
		container.innerHTML = '<p>No active cases found.</p>';
		return;
	}

	cases.forEach(case_item => {
		const caseDiv = document.createElement('div');
		caseDiv.className = 'case-item';
		caseDiv.innerHTML = `
			<h4>${case_item.case_title}</h4>
			<p>Status: ${case_item.status}</p>
			<p>Lawyer: ${case_item.lawyer_name}</p>
			<small>Filed: ${case_item.filing_date}</small>
		`;
		container.appendChild(caseDiv);
	});
}

function render_documents(documents) {
	const container = document.getElementById('documents-list');
	container.innerHTML = '';

	if (documents.length === 0) {
		container.innerHTML = '<p>No recent documents.</p>';
		return;
	}

	documents.forEach(doc => {
		const docDiv = document.createElement('div');
		docDiv.className = 'document-item';
		docDiv.innerHTML = `
			<h4>${doc.document_name}</h4>
			<p>Type: ${doc.document_type}</p>
			<small>Uploaded: ${doc.upload_date}</small>
			<a href="${doc.file_url}" target="_blank" class="btn btn-sm">Download</a>
		`;
		container.appendChild(docDiv);
	});
}

function render_hearings(hearings) {
	const container = document.getElementById('hearings-list');
	container.innerHTML = '';

	if (hearings.length === 0) {
		container.innerHTML = '<p>No upcoming hearings.</p>';
		return;
	}

	hearings.forEach(hearing => {
		const hearingDiv = document.createElement('div');
		hearingDiv.className = 'hearing-item';
		hearingDiv.innerHTML = `
			<h4>${hearing.case_title}</h4>
			<p>Date: ${hearing.hearing_date} at ${hearing.hearing_time}</p>
			<p>Court: ${hearing.court_name}</p>
		`;
		container.appendChild(hearingDiv);
	});
}

function render_messages(messages) {
	const container = document.getElementById('messages-list');
	container.innerHTML = '';

	if (messages.length === 0) {
		container.innerHTML = '<p>No messages.</p>';
		return;
	}

	messages.forEach(msg => {
		const msgDiv = document.createElement('div');
		msgDiv.className = 'message-item';
		msgDiv.innerHTML = `
			<h4>${msg.subject}</h4>
			<p>${msg.message}</p>
			<small>From: ${msg.from_user} on ${msg.sent_date}</small>
		`;
		container.appendChild(msgDiv);
	});
}

function send_message(subject, message) {
	const client_email = document.getElementById('login_email').value;

	frappe.call({
		method: 'sheria_app.api.send_client_message',
		args: {
			client_email: client_email,
			subject: subject,
			message: message
		},
		callback: function(r) {
			if (r.message && r.message.success) {
				alert('Message sent successfully!');
				// Reload messages
				const client_id = r.message.client_id;
				load_client_messages(client_id);
			} else {
				show_error_message('Failed to send message');
			}
		}
	});
}

function show_error_message(message) {
	alert(message);
}
"""

def get_client_portal_css():
	"""Get CSS for client portal page"""
	return """
/* Client Portal Page Styles */
.client-portal-page {
	min-height: 100vh;
	background: #f8f9fa;
}

.portal-header {
	background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
	color: white;
	padding: 60px 0;
	text-align: center;
}

.portal-header h1 {
	font-size: 2.5rem;
	margin-bottom: 1rem;
}

.portal-header p {
	font-size: 1.1rem;
}

.portal-content {
	padding: 40px 0;
}

.portal-login {
	max-width: 400px;
	margin: 0 auto;
	background: white;
	padding: 3rem;
	border-radius: 8px;
	box-shadow: 0 2px 20px rgba(0,0,0,0.1);
}

.portal-login h2 {
	text-align: center;
	margin-bottom: 2rem;
	color: #333;
}

.login-form .form-group {
	margin-bottom: 1.5rem;
}

.login-form label {
	display: block;
	margin-bottom: 0.5rem;
	color: #333;
	font-weight: 500;
}

.login-form input {
	width: 100%;
	padding: 12px;
	border: 2px solid #e1e5e9;
	border-radius: 5px;
	font-size: 1rem;
}

.login-form input:focus {
	outline: none;
	border-color: #667eea;
}

.login-help {
	text-align: center;
	margin-top: 2rem;
	color: #666;
	font-size: 0.9rem;
}

.portal-dashboard {
	max-width: 1200px;
	margin: 0 auto;
}

.dashboard-header {
	display: flex;
	justify-content: space-between;
	align-items: center;
	margin-bottom: 2rem;
	padding-bottom: 1rem;
	border-bottom: 2px solid #e1e5e9;
}

.dashboard-header h2 {
	color: #333;
	margin: 0;
}

.dashboard-grid {
	display: grid;
	grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
	gap: 2rem;
}

.dashboard-card {
	background: white;
	padding: 2rem;
	border-radius: 8px;
	box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.dashboard-card h3 {
	color: #333;
	margin-bottom: 1.5rem;
	border-bottom: 2px solid #f0f0f0;
	padding-bottom: 0.5rem;
}

.case-item,
.document-item,
.hearing-item,
.message-item {
	padding: 1rem;
	border: 1px solid #e1e5e9;
	border-radius: 5px;
	margin-bottom: 1rem;
	background: #fafafa;
}

.case-item h4,
.document-item h4,
.hearing-item h4,
.message-item h4 {
	margin: 0 0 0.5rem 0;
	color: #333;
	font-size: 1rem;
}

.case-item p,
.document-item p,
.hearing-item p,
.message-item p {
	margin: 0.25rem 0;
	color: #666;
	font-size: 0.9rem;
}

.case-item small,
.document-item small,
.hearing-item small,
.message-item small {
	color: #999;
	font-size: 0.8rem;
}

.btn-sm {
	padding: 6px 12px;
	font-size: 0.875rem;
}

.btn-outline {
	border: 2px solid #667eea;
	color: #667eea;
	background: transparent;
}

.btn-outline:hover {
	background: #667eea;
	color: white;
}
"""

def get_legal_resources_content():
	"""Get content for legal resources page"""
	return """
<div class="legal-resources-page">
	<section class="resources-hero">
		<div class="container">
			<h1>Legal Resources</h1>
			<p>Access legal information, articles, and resources to help you understand your rights</p>
		</div>
	</section>

	<section class="resources-content">
		<div class="container">
			<div class="resources-filters">
				<div class="filter-tabs">
					<button class="tab-btn active" data-category="all">All Resources</button>
					<button class="tab-btn" data-category="articles">Articles</button>
					<button class="tab-btn" data-category="guides">Legal Guides</button>
					<button class="tab-btn" data-category="faq">FAQ</button>
				</div>
				<div class="search-box">
					<input type="text" id="resource-search" placeholder="Search resources...">
				</div>
			</div>

			<div class="resources-grid" id="resources-grid">
				<!-- Resources will be loaded dynamically -->
			</div>

			<div class="load-more-container">
				<button id="load-more-btn" class="btn btn-secondary">Load More</button>
			</div>
		</div>
	</section>

	<section class="contact-banner">
		<div class="container">
			<h2>Need Personal Legal Advice?</h2>
			<p>Our experienced lawyers are here to help with your specific legal needs</p>
			<a href="/service-request" class="btn btn-primary">Get Legal Help</a>
		</div>
	</section>
</div>
"""

def get_legal_resources_js():
	"""Get JavaScript for legal resources page"""
	return """
// Legal Resources Page JavaScript
frappe.ready(function() {
	load_resources();
	setup_filters();
	setup_search();
	setup_load_more();
});

let current_page = 1;
let current_category = 'all';
let search_query = '';

function load_resources() {
	frappe.call({
		method: 'sheria_app.api.get_legal_resources',
		args: {
			category: current_category,
			search: search_query,
			page: current_page
		},
		callback: function(r) {
			if (r.message) {
				if (current_page === 1) {
					document.getElementById('resources-grid').innerHTML = '';
				}
				render_resources(r.message.resources);

				const loadMoreBtn = document.getElementById('load-more-btn');
				if (r.message.has_more) {
					loadMoreBtn.style.display = 'block';
				} else {
					loadMoreBtn.style.display = 'none';
				}
			}
		}
	});
}

function render_resources(resources) {
	const grid = document.getElementById('resources-grid');

	resources.forEach(resource => {
		const resourceCard = document.createElement('div');
		resourceCard.className = 'resource-card';
		resourceCard.innerHTML = `
			<div class="resource-header">
				<span class="resource-category">${resource.category}</span>
				<span class="resource-date">${resource.publish_date}</span>
			</div>
			<h3>${resource.title}</h3>
			<p>${resource.summary}</p>
			<a href="/resource/${resource.name}" class="btn btn-outline">Read More</a>
		`;
		grid.appendChild(resourceCard);
	});
}

function setup_filters() {
	const tabBtns = document.querySelectorAll('.tab-btn');

	tabBtns.forEach(btn => {
		btn.addEventListener('click', function() {
			// Remove active class from all buttons
			tabBtns.forEach(b => b.classList.remove('active'));
			// Add active class to clicked button
			this.classList.add('active');

			current_category = this.dataset.category;
			current_page = 1;
			load_resources();
		});
	});
}

function setup_search() {
	const searchInput = document.getElementById('resource-search');
	let searchTimeout;

	searchInput.addEventListener('input', function() {
		clearTimeout(searchTimeout);
		search_query = this.value;

		searchTimeout = setTimeout(() => {
			current_page = 1;
			load_resources();
		}, 500);
	});
}

function setup_load_more() {
	document.getElementById('load-more-btn').addEventListener('click', function() {
		current_page++;
		load_resources();
	});
}
"""

def get_legal_resources_css():
	"""Get CSS for legal resources page"""
	return """
/* Legal Resources Page Styles */
.legal-resources-page {
	min-height: 100vh;
}

.resources-hero {
	background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
	color: white;
	padding: 60px 0;
	text-align: center;
}

.resources-hero h1 {
	font-size: 2.5rem;
	margin-bottom: 1rem;
}

.resources-hero p {
	font-size: 1.1rem;
}

.resources-content {
	padding: 60px 0;
	background: #f8f9fa;
}

.resources-filters {
	display: flex;
	justify-content: space-between;
	align-items: center;
	margin-bottom: 3rem;
	flex-wrap: wrap;
	gap: 1rem;
}

.filter-tabs {
	display: flex;
	gap: 1rem;
	flex-wrap: wrap;
}

.tab-btn {
	padding: 10px 20px;
	border: 2px solid #667eea;
	background: white;
	color: #667eea;
	border-radius: 25px;
	cursor: pointer;
	transition: all 0.3s ease;
	font-weight: 500;
}

.tab-btn.active,
.tab-btn:hover {
	background: #667eea;
	color: white;
}

.search-box {
	flex: 1;
	max-width: 300px;
}

.search-box input {
	width: 100%;
	padding: 12px 20px;
	border: 2px solid #e1e5e9;
	border-radius: 25px;
	font-size: 1rem;
}

.search-box input:focus {
	outline: none;
	border-color: #667eea;
}

.resources-grid {
	display: grid;
	grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
	gap: 2rem;
	margin-bottom: 3rem;
}

.resource-card {
	background: white;
	padding: 2rem;
	border-radius: 8px;
	box-shadow: 0 2px 10px rgba(0,0,0,0.1);
	transition: transform 0.3s ease;
}

.resource-card:hover {
	transform: translateY(-5px);
}

.resource-header {
	display: flex;
	justify-content: space-between;
	align-items: center;
	margin-bottom: 1rem;
}

.resource-category {
	background: #e3f2fd;
	color: #1976d2;
	padding: 0.25rem 0.75rem;
	border-radius: 20px;
	font-size: 0.875rem;
	font-weight: 500;
}

.resource-date {
	color: #666;
	font-size: 0.875rem;
}

.resource-card h3 {
	color: #333;
	margin-bottom: 1rem;
	line-height: 1.4;
}

.resource-card p {
	color: #666;
	line-height: 1.6;
	margin-bottom: 1.5rem;
}

.load-more-container {
	text-align: center;
}

.contact-banner {
	padding: 60px 0;
	background: #667eea;
	color: white;
	text-align: center;
}

.contact-banner h2 {
	margin-bottom: 1rem;
}

.contact-banner p {
	margin-bottom: 2rem;
	font-size: 1.1rem;
}
"""

def create_default_web_pages():
	"""Create default web pages for Sheria app"""
	try:
		web_pages = get_web_page_config()

		for page_key, page_data in web_pages.items():
			if not frappe.db.exists("Web Page", page_data["name"]):
				web_page = frappe.get_doc({
					"doctype": "Web Page",
					"name": page_data["name"],
					"title": page_data["title"],
					"route": page_data["route"],
					"published": page_data["published"],
					"content_type": page_data["content_type"],
					"page_name": page_data["page_name"],
					"meta_title": page_data["meta_title"],
					"meta_description": page_data["meta_description"],
					"meta_keywords": page_data["meta_keywords"],
					"content": page_data["content"],
					"javascript": page_data["javascript"],
					"css": page_data["css"]
				})

				web_page.insert(ignore_permissions=True)
				frappe.db.commit()

	except Exception as e:
		frappe.log_error(f"Error creating web pages: {str(e)}")

# Web page API endpoints

@frappe.whitelist(allow_guest=True)
def get_published_services():
	"""API endpoint to get published legal services"""
	try:
		services = frappe.db.sql("""
			SELECT name, service_name, description, category_name, base_price
			FROM `tabLegal Service`
			WHERE published = 1 AND disabled = 0
			ORDER BY service_name
		""", as_dict=True)

		return services

	except Exception as e:
		frappe.log_error(f"Error getting published services: {str(e)}")
		return []

@frappe.whitelist(allow_guest=True)
def get_service_types():
	"""API endpoint to get service types"""
	try:
		services = frappe.db.sql("""
			SELECT name, service_name
			FROM `tabLegal Service`
			WHERE published = 1 AND disabled = 0
			ORDER BY service_name
		""", as_dict=True)

		return services

	except Exception as e:
		frappe.log_error(f"Error getting service types: {str(e)}")
		return []

@frappe.whitelist(allow_guest=True)
def submit_service_request(service_type, subject, description, client_name, email, phone, priority="Medium"):
	"""API endpoint to submit service request"""
	try:
		# Create service request
		service_request = frappe.get_doc({
			"doctype": "Service Request",
			"service_type": service_type,
			"subject": subject,
			"description": description,
			"client_name": client_name,
			"email": email,
			"phone": phone,
			"priority": priority,
			"status": "Submitted",
			"request_date": frappe.utils.today()
		})

		service_request.insert(ignore_permissions=True)
		frappe.db.commit()

		# Send notification email
		send_service_request_notification(service_request)

		return {"success": True, "message": "Service request submitted successfully"}

	except Exception as e:
		frappe.log_error(f"Error submitting service request: {str(e)}")
		return {"success": False, "message": str(e)}

@frappe.whitelist(allow_guest=True)
def get_legal_resources(category="all", search="", page=1, page_size=12):
	"""API endpoint to get legal resources"""
	try:
		conditions = []
		values = []

		if category != "all":
			conditions.append("category = %s")
			values.append(category)

		if search:
			conditions.append("(title LIKE %s OR content LIKE %s OR summary LIKE %s)")
			search_term = f"%{search}%"
			values.extend([search_term, search_term, search_term])

		where_clause = " AND ".join(conditions) if conditions else "1=1"

		offset = (page - 1) * page_size

		resources = frappe.db.sql(f"""
			SELECT name, title, summary, category, publish_date, content
			FROM `tabLegal Resource`
			WHERE published = 1 AND {where_clause}
			ORDER BY publish_date DESC
			LIMIT %s OFFSET %s
		""", values + [page_size, offset], as_dict=True)

		# Check if there are more resources
		total_count = frappe.db.sql(f"""
			SELECT COUNT(*) as count
			FROM `tabLegal Resource`
			WHERE published = 1 AND {where_clause}
		""", values)[0][0]

		has_more = (page * page_size) < total_count

		return {
			"resources": resources,
			"has_more": has_more
		}

	except Exception as e:
		frappe.log_error(f"Error getting legal resources: {str(e)}")
		return {"resources": [], "has_more": False}

def send_service_request_notification(service_request):
	"""Send notification email for new service request"""
	try:
		subject = f"New Service Request: {service_request.subject}"
		message = f"""
		A new service request has been submitted:

		Service Type: {service_request.service_type}
		Subject: {service_request.subject}
		Client: {service_request.client_name}
		Email: {service_request.email}
		Phone: {service_request.phone}
		Priority: {service_request.priority}

		Description:
		{service_request.description}

		Please review and assign this request to an appropriate lawyer.
		"""

		# Send to admin/support team
		frappe.sendmail(
			recipients=["admin@sheria_app.com"],  # Replace with actual admin email
			subject=subject,
			message=message
		)

	except Exception as e:
		frappe.log_error(f"Error sending service request notification: {str(e)}")