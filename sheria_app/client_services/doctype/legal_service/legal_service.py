# Legal Service DocType
# Copyright (c) 2024, Sheria Legal Technologies
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import nowdate, now


class WebsiteConfig:
	def __init__(self):
		self.condition_field = "is_active"
		self.page_name_field = "service_name"
		self.template = "legal_service_profile"


class LegalService(Document):
	website = WebsiteConfig()
	def validate(self):
		self.set_creation_details()
		self.validate_service_code()
		self.update_last_modified()

	def set_creation_details(self):
		"""Set creation details on first save"""
		if self.is_new():
			self.created_by = frappe.session.user
			self.creation_date = nowdate()

	def validate_service_code(self):
		"""Validate service code format"""
		if self.service_code:
			# Service code should be uppercase and contain only letters, numbers, and hyphens
			import re
			if not re.match(r'^[A-Z0-9-]+$', self.service_code):
				frappe.throw(_("Service Code should contain only uppercase letters, numbers, and hyphens"))

	def update_last_modified(self):
		"""Update last modified timestamp"""
		self.last_updated = now()

	def on_update(self):
		"""Actions on update"""
		if self.has_value_changed("is_active"):
			self.handle_activation_change()

		self.update_service_status()

	def handle_activation_change(self):
		"""Handle service activation/deactivation"""
		if not self.is_active:
			# Check if there are pending service requests
			pending_requests = frappe.db.count("Service Request", {
				"service": self.name,
				"status": ["in", ["Draft", "Submitted", "In Progress"]]
			})

			if pending_requests > 0:
				frappe.msgprint(
					_("Warning: There are {0} pending service requests for this service. "
					  "Deactivating it may affect client expectations.").format(pending_requests),
					alert=True
				)

	def update_service_status(self):
		"""Update service status based on current state"""
		# This method is called during on_update hook
		# Add any status update logic here if needed
		pass


@frappe.whitelist()
def get_active_services(category=None):
	"""Get all active legal services, optionally filtered by category"""
	filters = {"is_active": 1, "docstatus": 1}

	if category:
		filters["category"] = category

	services = frappe.get_all("Legal Service",
		filters=filters,
		fields=["name", "service_code", "service_name", "category", "description",
				"price", "billing_type", "estimated_duration", "featured"],
		order_by="category asc, service_name asc"
	)

	return services


@frappe.whitelist()
def get_featured_services():
	"""Get featured legal services"""
	services = frappe.get_all("Legal Service",
		filters={"is_active": 1, "featured": 1, "docstatus": 1},
		fields=["name", "service_code", "service_name", "category", "description",
				"price", "billing_type", "estimated_duration"],
		order_by="service_name asc"
	)

	return services


@frappe.whitelist()
def get_services_by_category():
	"""Get services grouped by category"""
	services = frappe.db.sql("""
		SELECT
			category,
			COUNT(*) as service_count,
			GROUP_CONCAT(service_name SEPARATOR ', ') as services
		FROM `tabLegal Service`
		WHERE is_active = 1 AND docstatus = 1
		GROUP BY category
		ORDER BY category
	""", as_dict=True)

	return services


@frappe.whitelist()
def get_service_details(service_code):
	"""Get detailed information about a specific service"""
	service = frappe.get_doc("Legal Service", service_code)

	return {
		"service_code": service.service_code,
		"service_name": service.service_name,
		"category": service.category,
		"description": service.description,
		"requirements": service.requirements,
		"timeline": service.timeline,
		"deliverables": service.deliverables,
		"price": service.price,
		"billing_type": service.billing_type,
		"estimated_duration": service.estimated_duration,
		"complexity_level": service.complexity_level,
		"eligibility_criteria": service.eligibility_criteria,
		"exclusions": service.exclusions,
		"terms_and_conditions": service.terms_and_conditions
	}


@frappe.whitelist()
def search_services(search_term=None, category=None, max_price=None):
	"""Search services based on various criteria"""
	filters = {"is_active": 1, "docstatus": 1}

	if category:
		filters["category"] = category

	if max_price:
		filters["price"] = ["<=", max_price]

	services = frappe.get_all("Legal Service",
		filters=filters,
		fields=["name", "service_code", "service_name", "category", "description", "price", "billing_type"]
	)

	if search_term:
		# Filter services that match search term in name or description
		filtered_services = []
		search_lower = search_term.lower()

		for service in services:
			if (search_lower in service.service_name.lower() or
				search_lower in (service.description or "").lower()):
				filtered_services.append(service)

		services = filtered_services

	return services


@frappe.whitelist()
def get_permission_query_conditions(user):
	"""Return permission query conditions for Legal Service"""
	# Only show active and approved services to users
	return "is_active = 1 AND docstatus = 1"