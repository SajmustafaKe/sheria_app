# Sheria Print Formats Module
# Copyright (c) 2024, Sheria Legal Technologies
# For license information, please see license.txt

import frappe
from frappe import _

def get_print_formats():
	"""Get print format configurations for Sheria app"""
	return {
		"Legal Case": {
			"standard": {
				"name": "Legal Case - Standard",
				"doc_type": "Legal Case",
				"html": get_case_print_format(),
				"standard": "Yes"
			},
			"detailed": {
				"name": "Legal Case - Detailed",
				"doc_type": "Legal Case",
				"html": get_case_detailed_print_format(),
				"standard": "No"
			}
		},
		"Service Request": {
			"standard": {
				"name": "Service Request - Standard",
				"doc_type": "Service Request",
				"html": get_service_request_print_format(),
				"standard": "Yes"
			}
		},
		"Legal Service": {
			"invoice": {
				"name": "Legal Service Invoice",
				"doc_type": "Legal Service",
				"html": get_service_invoice_print_format(),
				"standard": "Yes"
			},
			"receipt": {
				"name": "Legal Service Receipt",
				"doc_type": "Legal Service",
				"html": get_service_receipt_print_format(),
				"standard": "No"
			}
		},
		"Client": {
			"profile": {
				"name": "Client Profile",
				"doc_type": "Client",
				"html": get_client_profile_print_format(),
				"standard": "Yes"
			}
		},
		"Lawyer": {
			"profile": {
				"name": "Lawyer Profile",
				"doc_type": "Lawyer",
				"html": get_lawyer_profile_print_format(),
				"standard": "Yes"
			}
		}
	}

def create_default_print_formats():
	"""Create default print formats for Sheria app"""
	try:
		formats = get_print_formats()

		for doctype, format_configs in formats.items():
			for format_key, format_data in format_configs.items():
				if not frappe.db.exists("Print Format", format_data["name"]):
					print_format = frappe.get_doc({
						"doctype": "Print Format",
						"name": format_data["name"],
						"doc_type": format_data["doc_type"],
						"html": format_data["html"],
						"standard": format_data["standard"]
					})
					print_format.insert(ignore_permissions=True)
					frappe.db.commit()

	except Exception as e:
		frappe.log_error(f"Error creating print formats: {str(e)}")

def get_case_print_format():
	"""Get HTML template for legal case print format"""
	return """
	<div class="print-format">
		<div class="header">
			<h1>SHERIA LEGAL MANAGEMENT SYSTEM</h1>
			<h2>LEGAL CASE REPORT</h2>
		</div>

		<div class="case-details">
			<table class="table table-bordered">
				<tr>
					<td><strong>Case Number:</strong></td>
					<td>{{ doc.name }}</td>
					<td><strong>Case Type:</strong></td>
					<td>{{ doc.case_type }}</td>
				</tr>
				<tr>
					<td><strong>Client:</strong></td>
					<td>{{ doc.client_name }}</td>
					<td><strong>Priority:</strong></td>
					<td>{{ doc.priority }}</td>
				</tr>
				<tr>
					<td><strong>Assigned Lawyer:</strong></td>
					<td>{{ doc.assigned_lawyer_name }}</td>
					<td><strong>Status:</strong></td>
					<td>{{ doc.status }}</td>
				</tr>
				<tr>
					<td><strong>Filing Date:</strong></td>
					<td>{{ frappe.utils.format_date(doc.filing_date) }}</td>
					<td><strong>Deadline:</strong></td>
					<td>{{ frappe.utils.format_date(doc.deadline_date) }}</td>
				</tr>
				<tr>
					<td><strong>Court:</strong></td>
					<td>{{ doc.court_name }}</td>
					<td><strong>Practice Area:</strong></td>
					<td>{{ doc.practice_area }}</td>
				</tr>
			</table>
		</div>

		<div class="case-description">
			<h3>Case Description</h3>
			<p>{{ doc.description or "No description provided." }}</p>
		</div>

		{% if doc.hearings %}
		<div class="hearings">
			<h3>Hearing Schedule</h3>
			<table class="table table-bordered">
				<thead>
					<tr>
						<th>Date</th>
						<th>Time</th>
						<th>Type</th>
						<th>Court</th>
						<th>Status</th>
					</tr>
				</thead>
				<tbody>
					{% for hearing in doc.hearings %}
					<tr>
						<td>{{ frappe.utils.format_date(hearing.hearing_date) }}</td>
						<td>{{ hearing.hearing_time }}</td>
						<td>{{ hearing.hearing_type }}</td>
						<td>{{ hearing.court_name }}</td>
						<td>{{ hearing.status }}</td>
					</tr>
					{% endfor %}
				</tbody>
			</table>
		</div>
		{% endif %}

		<div class="footer">
			<p><small>Generated on {{ frappe.utils.format_datetime(frappe.utils.now()) }} by Sheria Legal Management System</small></p>
		</div>
	</div>

	<style>
		.print-format { font-family: Arial, sans-serif; margin: 20px; }
		.header { text-align: center; border-bottom: 2px solid #333; padding-bottom: 10px; margin-bottom: 20px; }
		.header h1 { color: #2c3e50; margin: 0; font-size: 24px; }
		.header h2 { color: #34495e; margin: 5px 0; font-size: 18px; }
		.case-details { margin-bottom: 20px; }
		.case-description { margin-bottom: 20px; }
		.hearings { margin-bottom: 20px; }
		.table { width: 100%; border-collapse: collapse; margin-bottom: 20px; }
		.table th, .table td { border: 1px solid #ddd; padding: 8px; text-align: left; }
		.table th { background-color: #f5f5f5; font-weight: bold; }
		.footer { text-align: center; border-top: 1px solid #ddd; padding-top: 10px; margin-top: 20px; color: #666; }
		h3 { color: #2c3e50; border-bottom: 1px solid #ddd; padding-bottom: 5px; }
	</style>
	"""

def get_case_detailed_print_format():
	"""Get HTML template for detailed legal case print format"""
	return """
	<div class="print-format">
		<div class="header">
			<h1>SHERIA LEGAL MANAGEMENT SYSTEM</h1>
			<h2>DETAILED LEGAL CASE REPORT</h2>
		</div>

		<div class="case-details">
			<table class="table table-bordered">
				<tr>
					<td colspan="4" style="background-color: #f8f9fa;"><strong>CASE INFORMATION</strong></td>
				</tr>
				<tr>
					<td><strong>Case Number:</strong></td>
					<td>{{ doc.name }}</td>
					<td><strong>Case Type:</strong></td>
					<td>{{ doc.case_type }}</td>
				</tr>
				<tr>
					<td><strong>Client:</strong></td>
					<td>{{ doc.client_name }}</td>
					<td><strong>Client ID:</strong></td>
					<td>{{ doc.client }}</td>
				</tr>
				<tr>
					<td><strong>Assigned Lawyer:</strong></td>
					<td>{{ doc.assigned_lawyer_name }}</td>
					<td><strong>Lawyer ID:</strong></td>
					<td>{{ doc.assigned_lawyer }}</td>
				</tr>
				<tr>
					<td><strong>Status:</strong></td>
					<td>{{ doc.status }}</td>
					<td><strong>Priority:</strong></td>
					<td>{{ doc.priority }}</td>
				</tr>
				<tr>
					<td><strong>Filing Date:</strong></td>
					<td>{{ frappe.utils.format_date(doc.filing_date) }}</td>
					<td><strong>Deadline:</strong></td>
					<td>{{ frappe.utils.format_date(doc.deadline_date) }}</td>
				</tr>
				<tr>
					<td><strong>Court:</strong></td>
					<td>{{ doc.court_name }}</td>
					<td><strong>Practice Area:</strong></td>
					<td>{{ doc.practice_area }}</td>
				</tr>
				<tr>
					<td><strong>Estimated Value:</strong></td>
					<td>{{ doc.currency }} {{ doc.estimated_value }}</td>
					<td><strong>Actual Cost:</strong></td>
					<td>{{ doc.currency }} {{ doc.actual_cost }}</td>
				</tr>
			</table>
		</div>

		<div class="case-description">
			<h3>Case Description</h3>
			<p>{{ doc.description or "No description provided." }}</p>
		</div>

		{% if doc.case_documents %}
		<div class="documents">
			<h3>Case Documents</h3>
			<table class="table table-bordered">
				<thead>
					<tr>
						<th>Document Type</th>
						<th>Document Name</th>
						<th>Date</th>
						<th>Status</th>
					</tr>
				</thead>
				<tbody>
					{% for doc_item in doc.case_documents %}
					<tr>
						<td>{{ doc_item.document_type }}</td>
						<td>{{ doc_item.document_name }}</td>
						<td>{{ frappe.utils.format_date(doc_item.date) }}</td>
						<td>{{ doc_item.status }}</td>
					</tr>
					{% endfor %}
				</tbody>
			</table>
		</div>
		{% endif %}

		{% if doc.hearings %}
		<div class="hearings">
			<h3>Hearing Schedule & History</h3>
			<table class="table table-bordered">
				<thead>
					<tr>
						<th>Date</th>
						<th>Time</th>
						<th>Type</th>
						<th>Court</th>
						<th>Judge</th>
						<th>Status</th>
						<th>Outcome</th>
					</tr>
				</thead>
				<tbody>
					{% for hearing in doc.hearings %}
					<tr>
						<td>{{ frappe.utils.format_date(hearing.hearing_date) }}</td>
						<td>{{ hearing.hearing_time }}</td>
						<td>{{ hearing.hearing_type }}</td>
						<td>{{ hearing.court_name }}</td>
						<td>{{ hearing.judge_name or '-' }}</td>
						<td>{{ hearing.status }}</td>
						<td>{{ hearing.outcome or '-' }}</td>
					</tr>
					{% endfor %}
				</tbody>
			</table>
		</div>
		{% endif %}

		{% if doc.case_notes %}
		<div class="notes">
			<h3>Case Notes & Updates</h3>
			{% for note in doc.case_notes %}
			<div class="note-item">
				<strong>{{ frappe.utils.format_datetime(note.date) }} - {{ note.added_by }}</strong>
				<p>{{ note.note }}</p>
			</div>
			{% endfor %}
		</div>
		{% endif %}

		<div class="footer">
			<p><small>Generated on {{ frappe.utils.format_datetime(frappe.utils.now()) }} by Sheria Legal Management System</small></p>
			<p><small>Confidential - For Internal Use Only</small></p>
		</div>
	</div>

	<style>
		.print-format { font-family: Arial, sans-serif; margin: 20px; }
		.header { text-align: center; border-bottom: 2px solid #333; padding-bottom: 10px; margin-bottom: 20px; }
		.header h1 { color: #2c3e50; margin: 0; font-size: 24px; }
		.header h2 { color: #34495e; margin: 5px 0; font-size: 18px; }
		.case-details { margin-bottom: 20px; }
		.case-description, .documents, .hearings, .notes { margin-bottom: 20px; }
		.table { width: 100%; border-collapse: collapse; margin-bottom: 20px; }
		.table th, .table td { border: 1px solid #ddd; padding: 8px; text-align: left; }
		.table th { background-color: #f5f5f5; font-weight: bold; }
		.note-item { border: 1px solid #eee; padding: 10px; margin-bottom: 10px; background-color: #fafafa; }
		.footer { text-align: center; border-top: 1px solid #ddd; padding-top: 10px; margin-top: 20px; color: #666; }
		h3 { color: #2c3e50; border-bottom: 1px solid #ddd; padding-bottom: 5px; }
	</style>
	"""

def get_service_request_print_format():
	"""Get HTML template for service request print format"""
	return """
	<div class="print-format">
		<div class="header">
			<h1>SHERIA LEGAL MANAGEMENT SYSTEM</h1>
			<h2>SERVICE REQUEST</h2>
		</div>

		<div class="request-details">
			<table class="table table-bordered">
				<tr>
					<td><strong>Request Number:</strong></td>
					<td>{{ doc.name }}</td>
					<td><strong>Status:</strong></td>
					<td>{{ doc.status }}</td>
				</tr>
				<tr>
					<td><strong>Client:</strong></td>
					<td>{{ doc.client_name }}</td>
					<td><strong>Service Type:</strong></td>
					<td>{{ doc.service_type }}</td>
				</tr>
				<tr>
					<td><strong>Priority:</strong></td>
					<td>{{ doc.priority }}</td>
					<td><strong>Request Date:</strong></td>
					<td>{{ frappe.utils.format_date(doc.request_date) }}</td>
				</tr>
				{% if doc.assigned_to %}
				<tr>
					<td><strong>Assigned To:</strong></td>
					<td>{{ doc.assigned_to_name }}</td>
					<td><strong>Due Date:</strong></td>
					<td>{{ frappe.utils.format_date(doc.due_date) }}</td>
				</tr>
				{% endif %}
			</table>
		</div>

		<div class="request-description">
			<h3>Request Description</h3>
			<p>{{ doc.description or "No description provided." }}</p>
		</div>

		{% if doc.attachments %}
		<div class="attachments">
			<h3>Attachments</h3>
			<ul>
				{% for attachment in doc.attachments %}
				<li>{{ attachment.file_name }}</li>
				{% endfor %}
			</ul>
		</div>
		{% endif %}

		<div class="footer">
			<p><small>Generated on {{ frappe.utils.format_datetime(frappe.utils.now()) }} by Sheria Legal Management System</small></p>
		</div>
	</div>

	<style>
		.print-format { font-family: Arial, sans-serif; margin: 20px; }
		.header { text-align: center; border-bottom: 2px solid #333; padding-bottom: 10px; margin-bottom: 20px; }
		.header h1 { color: #2c3e50; margin: 0; font-size: 24px; }
		.header h2 { color: #34495e; margin: 5px 0; font-size: 18px; }
		.request-details { margin-bottom: 20px; }
		.request-description { margin-bottom: 20px; }
		.attachments { margin-bottom: 20px; }
		.table { width: 100%; border-collapse: collapse; margin-bottom: 20px; }
		.table th, .table td { border: 1px solid #ddd; padding: 8px; text-align: left; }
		.table th { background-color: #f5f5f5; font-weight: bold; }
		.footer { text-align: center; border-top: 1px solid #ddd; padding-top: 10px; margin-top: 20px; color: #666; }
		h3 { color: #2c3e50; border-bottom: 1px solid #ddd; padding-bottom: 5px; }
		ul { padding-left: 20px; }
	</style>
	"""

def get_service_invoice_print_format():
	"""Get HTML template for legal service invoice print format"""
	return """
	<div class="print-format">
		<div class="header">
			<h1>SHERIA LEGAL MANAGEMENT SYSTEM</h1>
			<h2>LEGAL SERVICE INVOICE</h2>
		</div>

		<div class="invoice-details">
			<table class="table table-bordered">
				<tr>
					<td><strong>Invoice Number:</strong></td>
					<td>{{ doc.name }}</td>
					<td><strong>Invoice Date:</strong></td>
					<td>{{ frappe.utils.format_date(doc.invoice_date) }}</td>
				</tr>
				<tr>
					<td><strong>Client:</strong></td>
					<td>{{ doc.client_name }}</td>
					<td><strong>Due Date:</strong></td>
					<td>{{ frappe.utils.format_date(doc.due_date) }}</td>
				</tr>
				<tr>
					<td><strong>Service Type:</strong></td>
					<td>{{ doc.service_type }}</td>
					<td><strong>Status:</strong></td>
					<td>{{ doc.status }}</td>
				</tr>
			</table>
		</div>

		<div class="service-details">
			<h3>Service Details</h3>
			<p>{{ doc.description or "No description provided." }}</p>
		</div>

		<div class="billing-details">
			<table class="table table-bordered">
				<thead>
					<tr>
						<th>Description</th>
						<th>Quantity</th>
						<th>Rate</th>
						<th>Amount</th>
					</tr>
				</thead>
				<tbody>
					{% for item in doc.service_items %}
					<tr>
						<td>{{ item.description }}</td>
						<td>{{ item.quantity }}</td>
						<td>{{ doc.currency }} {{ item.rate }}</td>
						<td>{{ doc.currency }} {{ item.amount }}</td>
					</tr>
					{% endfor %}
				</tbody>
				<tfoot>
					<tr>
						<td colspan="3"><strong>Subtotal</strong></td>
						<td><strong>{{ doc.currency }} {{ doc.total_amount }}</strong></td>
					</tr>
					{% if doc.tax_amount %}
					<tr>
						<td colspan="3"><strong>Tax ({{ doc.tax_rate }}%)</strong></td>
						<td><strong>{{ doc.currency }} {{ doc.tax_amount }}</strong></td>
					</tr>
					{% endif %}
					<tr>
						<td colspan="3"><strong>Total Amount</strong></td>
						<td><strong>{{ doc.currency }} {{ doc.grand_total }}</strong></td>
					</tr>
				</tfoot>
			</table>
		</div>

		<div class="payment-info">
			<h3>Payment Information</h3>
			<p><strong>Outstanding Amount:</strong> {{ doc.currency }} {{ doc.outstanding_amount }}</p>
			<p><strong>Payment Terms:</strong> {{ doc.payment_terms or "Due upon receipt" }}</p>
		</div>

		<div class="footer">
			<p><small>Generated on {{ frappe.utils.format_datetime(frappe.utils.now()) }} by Sheria Legal Management System</small></p>
		</div>
	</div>

	<style>
		.print-format { font-family: Arial, sans-serif; margin: 20px; }
		.header { text-align: center; border-bottom: 2px solid #333; padding-bottom: 10px; margin-bottom: 20px; }
		.header h1 { color: #2c3e50; margin: 0; font-size: 24px; }
		.header h2 { color: #34495e; margin: 5px 0; font-size: 18px; }
		.invoice-details, .service-details, .billing-details, .payment-info { margin-bottom: 20px; }
		.table { width: 100%; border-collapse: collapse; margin-bottom: 20px; }
		.table th, .table td { border: 1px solid #ddd; padding: 8px; text-align: left; }
		.table th { background-color: #f5f5f5; font-weight: bold; }
		.table tfoot td { border-top: 2px solid #333; }
		.footer { text-align: center; border-top: 1px solid #ddd; padding-top: 10px; margin-top: 20px; color: #666; }
		h3 { color: #2c3e50; border-bottom: 1px solid #ddd; padding-bottom: 5px; }
	</style>
	"""

def get_service_receipt_print_format():
	"""Get HTML template for legal service receipt print format"""
	return """
	<div class="print-format">
		<div class="header">
			<h1>SHERIA LEGAL MANAGEMENT SYSTEM</h1>
			<h2>PAYMENT RECEIPT</h2>
		</div>

		<div class="receipt-details">
			<table class="table table-bordered">
				<tr>
					<td><strong>Receipt Number:</strong></td>
					<td>{{ doc.name }}</td>
					<td><strong>Receipt Date:</strong></td>
					<td>{{ frappe.utils.format_date(doc.receipt_date) }}</td>
				</tr>
				<tr>
					<td><strong>Client:</strong></td>
					<td>{{ doc.client_name }}</td>
					<td><strong>Payment Method:</strong></td>
					<td>{{ doc.payment_method }}</td>
				</tr>
				<tr>
					<td><strong>Service:</strong></td>
					<td>{{ doc.service_name }}</td>
					<td><strong>Reference:</strong></td>
					<td>{{ doc.reference_number }}</td>
				</tr>
			</table>
		</div>

		<div class="payment-details">
			<h3>Payment Details</h3>
			<table class="table table-bordered">
				<tr>
					<td><strong>Amount Paid:</strong></td>
					<td>{{ doc.currency }} {{ doc.amount_paid }}</td>
				</tr>
				<tr>
					<td><strong>Payment Date:</strong></td>
					<td>{{ frappe.utils.format_date(doc.payment_date) }}</td>
				</tr>
				<tr>
					<td><strong>Received By:</strong></td>
					<td>{{ doc.received_by }}</td>
				</tr>
			</table>
		</div>

		<div class="service-info">
			<h3>Service Information</h3>
			<p>{{ doc.service_description or "Legal services rendered." }}</p>
		</div>

		<div class="footer">
			<p><strong>Thank you for your payment!</strong></p>
			<p><small>Generated on {{ frappe.utils.format_datetime(frappe.utils.now()) }} by Sheria Legal Management System</small></p>
		</div>
	</div>

	<style>
		.print-format { font-family: Arial, sans-serif; margin: 20px; }
		.header { text-align: center; border-bottom: 2px solid #333; padding-bottom: 10px; margin-bottom: 20px; }
		.header h1 { color: #2c3e50; margin: 0; font-size: 24px; }
		.header h2 { color: #34495e; margin: 5px 0; font-size: 18px; }
		.receipt-details, .payment-details, .service-info { margin-bottom: 20px; }
		.table { width: 100%; border-collapse: collapse; margin-bottom: 20px; }
		.table th, .table td { border: 1px solid #ddd; padding: 8px; text-align: left; }
		.table th { background-color: #f5f5f5; font-weight: bold; }
		.footer { text-align: center; border-top: 1px solid #ddd; padding-top: 10px; margin-top: 20px; color: #666; }
		h3 { color: #2c3e50; border-bottom: 1px solid #ddd; padding-bottom: 5px; }
	</style>
	"""

def get_client_profile_print_format():
	"""Get HTML template for client profile print format"""
	return """
	<div class="print-format">
		<div class="header">
			<h1>SHERIA LEGAL MANAGEMENT SYSTEM</h1>
			<h2>CLIENT PROFILE</h2>
		</div>

		<div class="client-details">
			<table class="table table-bordered">
				<tr>
					<td colspan="4" style="background-color: #f8f9fa;"><strong>CLIENT INFORMATION</strong></td>
				</tr>
				<tr>
					<td><strong>Client ID:</strong></td>
					<td>{{ doc.name }}</td>
					<td><strong>Client Type:</strong></td>
					<td>{{ doc.client_type }}</td>
				</tr>
				<tr>
					<td><strong>Full Name:</strong></td>
					<td>{{ doc.client_name }}</td>
					<td><strong>Status:</strong></td>
					<td>{{ doc.status }}</td>
				</tr>
				<tr>
					<td><strong>Email:</strong></td>
					<td>{{ doc.email }}</td>
					<td><strong>Phone:</strong></td>
					<td>{{ doc.phone }}</td>
				</tr>
				<tr>
					<td><strong>Registration Date:</strong></td>
					<td>{{ frappe.utils.format_date(doc.registration_date) }}</td>
					<td><strong>Last Contact:</strong></td>
					<td>{{ frappe.utils.format_date(doc.last_contact_date) }}</td>
				</tr>
			</table>
		</div>

		{% if doc.address %}
		<div class="address">
			<h3>Address Information</h3>
			<p>{{ doc.address }}</p>
		</div>
		{% endif %}

		{% if doc.client_cases %}
		<div class="cases">
			<h3>Associated Cases</h3>
			<table class="table table-bordered">
				<thead>
					<tr>
						<th>Case Number</th>
						<th>Case Type</th>
						<th>Status</th>
						<th>Filing Date</th>
					</tr>
				</thead>
				<tbody>
					{% for case in doc.client_cases %}
					<tr>
						<td>{{ case.case_number }}</td>
						<td>{{ case.case_type }}</td>
						<td>{{ case.status }}</td>
						<td>{{ frappe.utils.format_date(case.filing_date) }}</td>
					</tr>
					{% endfor %}
				</tbody>
			</table>
		</div>
		{% endif %}

		<div class="footer">
			<p><small>Generated on {{ frappe.utils.format_datetime(frappe.utils.now()) }} by Sheria Legal Management System</small></p>
			<p><small>Confidential - For Internal Use Only</small></p>
		</div>
	</div>

	<style>
		.print-format { font-family: Arial, sans-serif; margin: 20px; }
		.header { text-align: center; border-bottom: 2px solid #333; padding-bottom: 10px; margin-bottom: 20px; }
		.header h1 { color: #2c3e50; margin: 0; font-size: 24px; }
		.header h2 { color: #34495e; margin: 5px 0; font-size: 18px; }
		.client-details, .address, .cases { margin-bottom: 20px; }
		.table { width: 100%; border-collapse: collapse; margin-bottom: 20px; }
		.table th, .table td { border: 1px solid #ddd; padding: 8px; text-align: left; }
		.table th { background-color: #f5f5f5; font-weight: bold; }
		.footer { text-align: center; border-top: 1px solid #ddd; padding-top: 10px; margin-top: 20px; color: #666; }
		h3 { color: #2c3e50; border-bottom: 1px solid #ddd; padding-bottom: 5px; }
	</style>
	"""

def get_lawyer_profile_print_format():
	"""Get HTML template for lawyer profile print format"""
	return """
	<div class="print-format">
		<div class="header">
			<h1>SHERIA LEGAL MANAGEMENT SYSTEM</h1>
			<h2>LAWYER PROFILE</h2>
		</div>

		<div class="lawyer-details">
			<table class="table table-bordered">
				<tr>
					<td colspan="4" style="background-color: #f8f9fa;"><strong>LAWYER INFORMATION</strong></td>
				</tr>
				<tr>
					<td><strong>Lawyer ID:</strong></td>
					<td>{{ doc.name }}</td>
					<td><strong>Status:</strong></td>
					<td>{{ doc.status }}</td>
				</tr>
				<tr>
					<td><strong>Full Name:</strong></td>
					<td>{{ doc.lawyer_name }}</td>
					<td><strong>License Number:</strong></td>
					<td>{{ doc.license_number }}</td>
				</tr>
				<tr>
					<td><strong>Email:</strong></td>
					<td>{{ doc.email }}</td>
					<td><strong>Phone:</strong></td>
					<td>{{ doc.phone }}</td>
				</tr>
				<tr>
					<td><strong>Practice Areas:</strong></td>
					<td>{{ doc.practice_areas }}</td>
					<td><strong>Experience (Years):</strong></td>
					<td>{{ doc.years_of_experience }}</td>
				</tr>
				<tr>
					<td><strong>Joining Date:</strong></td>
					<td>{{ frappe.utils.format_date(doc.joining_date) }}</td>
					<td><strong>Qualifications:</strong></td>
					<td>{{ doc.qualifications }}</td>
				</tr>
			</table>
		</div>

		{% if doc.specializations %}
		<div class="specializations">
			<h3>Specializations</h3>
			<p>{{ doc.specializations }}</p>
		</div>
		{% endif %}

		{% if doc.lawyer_cases %}
		<div class="cases">
			<h3>Current Cases</h3>
			<table class="table table-bordered">
				<thead>
					<tr>
						<th>Case Number</th>
						<th>Client</th>
						<th>Status</th>
						<th>Priority</th>
					</tr>
				</thead>
				<tbody>
					{% for case in doc.lawyer_cases %}
					<tr>
						<td>{{ case.case_number }}</td>
						<td>{{ case.client_name }}</td>
						<td>{{ case.status }}</td>
						<td>{{ case.priority }}</td>
					</tr>
					{% endfor %}
				</tbody>
			</table>
		</div>
		{% endif %}

		<div class="footer">
			<p><small>Generated on {{ frappe.utils.format_datetime(frappe.utils.now()) }} by Sheria Legal Management System</small></p>
			<p><small>Confidential - For Internal Use Only</small></p>
		</div>
	</div>

	<style>
		.print-format { font-family: Arial, sans-serif; margin: 20px; }
		.header { text-align: center; border-bottom: 2px solid #333; padding-bottom: 10px; margin-bottom: 20px; }
		.header h1 { color: #2c3e50; margin: 0; font-size: 24px; }
		.header h2 { color: #34495e; margin: 5px 0; font-size: 18px; }
		.lawyer-details, .specializations, .cases { margin-bottom: 20px; }
		.table { width: 100%; border-collapse: collapse; margin-bottom: 20px; }
		.table th, .table td { border: 1px solid #ddd; padding: 8px; text-align: left; }
		.table th { background-color: #f5f5f5; font-weight: bold; }
		.footer { text-align: center; border-top: 1px solid #ddd; padding-top: 10px; margin-top: 20px; color: #666; }
		h3 { color: #2c3e50; border-bottom: 1px solid #ddd; padding-bottom: 5px; }
	</style>
	"""