# Sheria App Permissions Module
# Copyright (c) 2024, Coale Tech
# For license information, please see license.txt

import frappe
from frappe import _

def get_permission_config():
	"""Get permission configuration for Sheria app"""
	return {
		"roles": {
			"Legal Admin": {
				"name": "Legal Admin",
				"role_name": _("Legal Admin"),
				"desk_access": 1,
				"permissions": get_legal_admin_permissions()
			},
			"Lawyer": {
				"name": "Lawyer",
				"role_name": _("Lawyer"),
				"desk_access": 1,
				"permissions": get_lawyer_permissions()
			},
			"Legal Assistant": {
				"name": "Legal Assistant",
				"role_name": _("Legal Assistant"),
				"desk_access": 1,
				"permissions": get_legal_assistant_permissions()
			},
			"Client": {
				"name": "Client",
				"role_name": _("Client"),
				"desk_access": 0,
				"permissions": get_client_permissions()
			},
			"Paralegal": {
				"name": "Paralegal",
				"role_name": _("Paralegal"),
				"desk_access": 1,
				"permissions": get_paralegal_permissions()
			}
		},
		"user_types": {
			"Legal Staff": {
				"name": "Legal Staff",
				"user_type": _("Legal Staff"),
				"roles": ["Lawyer", "Legal Assistant", "Paralegal"]
			},
			"Client User": {
				"name": "Client User",
				"user_type": _("Client User"),
				"roles": ["Client"]
			}
		}
	}

def get_legal_admin_permissions():
	"""Get permissions for Legal Admin role"""
	return [
		# Legal Practice Module
		{
			"doctype": "Legal Case",
			"read": 1,
			"write": 1,
			"create": 1,
			"delete": 1,
			"submit": 1,
			"cancel": 1,
			"amend": 1,
			"print": 1,
			"email": 1,
			"report": 1,
			"export": 1,
			"share": 1
		},
		{
			"doctype": "Case Hearing",
			"read": 1,
			"write": 1,
			"create": 1,
			"delete": 1,
			"submit": 1,
			"cancel": 1,
			"amend": 1,
			"print": 1,
			"email": 1,
			"report": 1,
			"export": 1,
			"share": 1
		},
		{
			"doctype": "Court",
			"read": 1,
			"write": 1,
			"create": 1,
			"delete": 1,
			"submit": 1,
			"cancel": 1,
			"amend": 1,
			"print": 1,
			"email": 1,
			"report": 1,
			"export": 1,
			"share": 1
		},
		{
			"doctype": "Lawyer",
			"read": 1,
			"write": 1,
			"create": 1,
			"delete": 1,
			"submit": 1,
			"cancel": 1,
			"amend": 1,
			"print": 1,
			"email": 1,
			"report": 1,
			"export": 1,
			"share": 1
		},
		{
			"doctype": "Practice Area",
			"read": 1,
			"write": 1,
			"create": 1,
			"delete": 1,
			"submit": 1,
			"cancel": 1,
			"amend": 1,
			"print": 1,
			"email": 1,
			"report": 1,
			"export": 1,
			"share": 1
		},
		{
			"doctype": "Legal Document",
			"read": 1,
			"write": 1,
			"create": 1,
			"delete": 1,
			"submit": 1,
			"cancel": 1,
			"amend": 1,
			"print": 1,
			"email": 1,
			"report": 1,
			"export": 1,
			"share": 1
		},
		{
			"doctype": "Legal Research",
			"read": 1,
			"write": 1,
			"create": 1,
			"delete": 1,
			"submit": 1,
			"cancel": 1,
			"amend": 1,
			"print": 1,
			"email": 1,
			"report": 1,
			"export": 1,
			"share": 1
		},

		# Client Services Module
		{
			"doctype": "Service Request",
			"read": 1,
			"write": 1,
			"create": 1,
			"delete": 1,
			"submit": 1,
			"cancel": 1,
			"amend": 1,
			"print": 1,
			"email": 1,
			"report": 1,
			"export": 1,
			"share": 1
		},
		{
			"doctype": "Legal Service",
			"read": 1,
			"write": 1,
			"create": 1,
			"delete": 1,
			"submit": 1,
			"cancel": 1,
			"amend": 1,
			"print": 1,
			"email": 1,
			"report": 1,
			"export": 1,
			"share": 1
		},
		{
			"doctype": "Client",
			"read": 1,
			"write": 1,
			"create": 1,
			"delete": 1,
			"submit": 1,
			"cancel": 1,
			"amend": 1,
			"print": 1,
			"email": 1,
			"report": 1,
			"export": 1,
			"share": 1
		},
		{
			"doctype": "Consultation",
			"read": 1,
			"write": 1,
			"create": 1,
			"delete": 1,
			"submit": 1,
			"cancel": 1,
			"amend": 1,
			"print": 1,
			"email": 1,
			"report": 1,
			"export": 1,
			"share": 1
		},
		{
			"doctype": "Client Feedback",
			"read": 1,
			"write": 1,
			"create": 1,
			"delete": 1,
			"submit": 1,
			"cancel": 1,
			"amend": 1,
			"print": 1,
			"email": 1,
			"report": 1,
			"export": 1,
			"share": 1
		},
		{
			"doctype": "Service Category",
			"read": 1,
			"write": 1,
			"create": 1,
			"delete": 1,
			"submit": 1,
			"cancel": 1,
			"amend": 1,
			"print": 1,
			"email": 1,
			"report": 1,
			"export": 1,
			"share": 1
		},

		# Reports and Analytics
		{
			"doctype": "Case Summary Report",
			"read": 1,
			"write": 0,
			"create": 0,
			"delete": 0,
			"submit": 0,
			"cancel": 0,
			"amend": 0,
			"print": 1,
			"email": 1,
			"report": 1,
			"export": 1,
			"share": 1
		},
		{
			"doctype": "Client Portfolio Report",
			"read": 1,
			"write": 0,
			"create": 0,
			"delete": 0,
			"submit": 0,
			"cancel": 0,
			"amend": 0,
			"print": 1,
			"email": 1,
			"report": 1,
			"export": 1,
			"share": 1
		},
		{
			"doctype": "Financial Summary Report",
			"read": 1,
			"write": 0,
			"create": 0,
			"delete": 0,
			"submit": 0,
			"cancel": 0,
			"amend": 0,
			"print": 1,
			"email": 1,
			"report": 1,
			"export": 1,
			"share": 1
		}
	]

def get_lawyer_permissions():
	"""Get permissions for Lawyer role"""
	return [
		# Legal Practice Module - Full access to assigned cases
		{
			"doctype": "Legal Case",
			"read": 1,
			"write": 1,
			"create": 1,
			"delete": 0,
			"submit": 1,
			"cancel": 0,
			"amend": 1,
			"print": 1,
			"email": 1,
			"report": 1,
			"export": 1,
			"share": 1,
			"if_owner": 1
		},
		{
			"doctype": "Case Hearing",
			"read": 1,
			"write": 1,
			"create": 1,
			"delete": 0,
			"submit": 1,
			"cancel": 0,
			"amend": 1,
			"print": 1,
			"email": 1,
			"report": 1,
			"export": 1,
			"share": 1,
			"if_owner": 1
		},
		{
			"doctype": "Legal Document",
			"read": 1,
			"write": 1,
			"create": 1,
			"delete": 0,
			"submit": 1,
			"cancel": 0,
			"amend": 1,
			"print": 1,
			"email": 1,
			"report": 1,
			"export": 1,
			"share": 1,
			"if_owner": 1
		},
		{
			"doctype": "Legal Research",
			"read": 1,
			"write": 1,
			"create": 1,
			"delete": 0,
			"submit": 1,
			"cancel": 0,
			"amend": 1,
			"print": 1,
			"email": 1,
			"report": 1,
			"export": 1,
			"share": 1
		},

		# Client Services Module - Limited access
		{
			"doctype": "Service Request",
			"read": 1,
			"write": 1,
			"create": 0,
			"delete": 0,
			"submit": 1,
			"cancel": 0,
			"amend": 1,
			"print": 1,
			"email": 1,
			"report": 0,
			"export": 0,
			"share": 1,
			"if_owner": 1
		},
		{
			"doctype": "Consultation",
			"read": 1,
			"write": 1,
			"create": 1,
			"delete": 0,
			"submit": 1,
			"cancel": 0,
			"amend": 1,
			"print": 1,
			"email": 1,
			"report": 0,
			"export": 0,
			"share": 1,
			"if_owner": 1
		},
		{
			"doctype": "Client",
			"read": 1,
			"write": 0,
			"create": 0,
			"delete": 0,
			"submit": 0,
			"cancel": 0,
			"amend": 0,
			"print": 1,
			"email": 1,
			"report": 0,
			"export": 0,
			"share": 0,
			"if_owner": 1
		},

		# Reports - Read only
		{
			"doctype": "Case Summary Report",
			"read": 1,
			"write": 0,
			"create": 0,
			"delete": 0,
			"submit": 0,
			"cancel": 0,
			"amend": 0,
			"print": 1,
			"email": 1,
			"report": 1,
			"export": 1,
			"share": 0
		}
	]

def get_legal_assistant_permissions():
	"""Get permissions for Legal Assistant role"""
	return [
		# Legal Practice Module - Limited access
		{
			"doctype": "Legal Case",
			"read": 1,
			"write": 1,
			"create": 0,
			"delete": 0,
			"submit": 0,
			"cancel": 0,
			"amend": 0,
			"print": 1,
			"email": 1,
			"report": 0,
			"export": 0,
			"share": 0,
			"if_owner": 1
		},
		{
			"doctype": "Case Hearing",
			"read": 1,
			"write": 1,
			"create": 0,
			"delete": 0,
			"submit": 0,
			"cancel": 0,
			"amend": 0,
			"print": 1,
			"email": 1,
			"report": 0,
			"export": 0,
			"share": 0,
			"if_owner": 1
		},
		{
			"doctype": "Legal Document",
			"read": 1,
			"write": 1,
			"create": 1,
			"delete": 0,
			"submit": 1,
			"cancel": 0,
			"amend": 0,
			"print": 1,
			"email": 1,
			"report": 0,
			"export": 0,
			"share": 0,
			"if_owner": 1
		},

		# Client Services Module - Full access for service requests
		{
			"doctype": "Service Request",
			"read": 1,
			"write": 1,
			"create": 1,
			"delete": 0,
			"submit": 1,
			"cancel": 0,
			"amend": 1,
			"print": 1,
			"email": 1,
			"report": 1,
			"export": 1,
			"share": 1
		},
		{
			"doctype": "Consultation",
			"read": 1,
			"write": 1,
			"create": 1,
			"delete": 0,
			"submit": 1,
			"cancel": 0,
			"amend": 1,
			"print": 1,
			"email": 1,
			"report": 0,
			"export": 0,
			"share": 1
		},
		{
			"doctype": "Client",
			"read": 1,
			"write": 1,
			"create": 1,
			"delete": 0,
			"submit": 1,
			"cancel": 0,
			"amend": 0,
			"print": 1,
			"email": 1,
			"report": 0,
			"export": 0,
			"share": 0
		},
		{
			"doctype": "Client Feedback",
			"read": 1,
			"write": 1,
			"create": 1,
			"delete": 0,
			"submit": 1,
			"cancel": 0,
			"amend": 0,
			"print": 1,
			"email": 1,
			"report": 1,
			"export": 1,
			"share": 1
		}
	]

def get_client_permissions():
	"""Get permissions for Client role"""
	return [
		# Limited access to own data only
		{
			"doctype": "Service Request",
			"read": 1,
			"write": 0,
			"create": 1,
			"delete": 0,
			"submit": 0,
			"cancel": 0,
			"amend": 0,
			"print": 1,
			"email": 1,
			"report": 0,
			"export": 0,
			"share": 0,
			"if_owner": 1
		},
		{
			"doctype": "Client Feedback",
			"read": 1,
			"write": 0,
			"create": 1,
			"delete": 0,
			"submit": 0,
			"cancel": 0,
			"amend": 0,
			"print": 1,
			"email": 1,
			"report": 0,
			"export": 0,
			"share": 0,
			"if_owner": 1
		},
		{
			"doctype": "Consultation",
			"read": 1,
			"write": 0,
			"create": 0,
			"delete": 0,
			"submit": 0,
			"cancel": 0,
			"amend": 0,
			"print": 1,
			"email": 1,
			"report": 0,
			"export": 0,
			"share": 0,
			"if_owner": 1
		}
	]

def get_paralegal_permissions():
	"""Get permissions for Paralegal role"""
	return [
		# Legal Practice Module - Research and document support
		{
			"doctype": "Legal Case",
			"read": 1,
			"write": 0,
			"create": 0,
			"delete": 0,
			"submit": 0,
			"cancel": 0,
			"amend": 0,
			"print": 1,
			"email": 1,
			"report": 0,
			"export": 0,
			"share": 0,
			"if_owner": 1
		},
		{
			"doctype": "Legal Document",
			"read": 1,
			"write": 1,
			"create": 1,
			"delete": 0,
			"submit": 1,
			"cancel": 0,
			"amend": 0,
			"print": 1,
			"email": 1,
			"report": 0,
			"export": 0,
			"share": 0,
			"if_owner": 1
		},
		{
			"doctype": "Legal Research",
			"read": 1,
			"write": 1,
			"create": 1,
			"delete": 0,
			"submit": 1,
			"cancel": 0,
			"amend": 0,
			"print": 1,
			"email": 1,
			"report": 1,
			"export": 1,
			"share": 1
		},
		{
			"doctype": "Case Hearing",
			"read": 1,
			"write": 0,
			"create": 0,
			"delete": 0,
			"submit": 0,
			"cancel": 0,
			"amend": 0,
			"print": 1,
			"email": 1,
			"report": 0,
			"export": 0,
			"share": 0,
			"if_owner": 1
		},

		# Client Services Module - Support role
		{
			"doctype": "Service Request",
			"read": 1,
			"write": 1,
			"create": 0,
			"delete": 0,
			"submit": 1,
			"cancel": 0,
			"amend": 1,
			"print": 1,
			"email": 1,
			"report": 0,
			"export": 0,
			"share": 0
		},
		{
			"doctype": "Client",
			"read": 1,
			"write": 0,
			"create": 0,
			"delete": 0,
			"submit": 0,
			"cancel": 0,
			"amend": 0,
			"print": 1,
			"email": 1,
			"report": 0,
			"export": 0,
			"share": 0
		}
	]

def create_default_roles():
	"""Create default roles for Sheria app"""
	try:
		roles_config = get_permission_config()["roles"]

		for role_key, role_data in roles_config.items():
			if not frappe.db.exists("Role", role_data["name"]):
				role = frappe.get_doc({
					"doctype": "Role",
					"name": role_data["name"],
					"role_name": role_data["role_name"],
					"desk_access": role_data["desk_access"]
				})

				role.insert(ignore_permissions=True)

		frappe.db.commit()

	except Exception as e:
		frappe.log_error(f"Error creating roles: {str(e)}")

def create_default_user_types():
	"""Create default user types for Sheria app"""
	try:
		user_types_config = get_permission_config()["user_types"]

		for user_type_key, user_type_data in user_types_config.items():
			if not frappe.db.exists("User Type", user_type_data["name"]):
				user_type = frappe.get_doc({
					"doctype": "User Type",
					"name": user_type_data["name"],
					"user_type": user_type_data["user_type"]
				})

				# Add roles to user type
				for role_name in user_type_data["roles"]:
					user_type.append("roles", {"role": role_name})

				user_type.insert(ignore_permissions=True)

		frappe.db.commit()

	except Exception as e:
		frappe.log_error(f"Error creating user types: {str(e)}")

def setup_permissions():
	"""Setup permissions for all doctypes"""
	try:
		roles_config = get_permission_config()["roles"]

		for role_key, role_data in roles_config.items():
			for permission in role_data["permissions"]:
				# Check if permission already exists
				existing = frappe.db.exists("Custom DocPerm", {
					"role": role_data["name"],
					"parent": permission["doctype"]
				})

				if not existing:
					docperm = frappe.get_doc({
						"doctype": "Custom DocPerm",
						"role": role_data["name"],
						"parent": permission["doctype"],
						"parenttype": "DocType",
						"parentfield": "permissions",
						"read": permission.get("read", 0),
						"write": permission.get("write", 0),
						"create": permission.get("create", 0),
						"delete": permission.get("delete", 0),
						"submit": permission.get("submit", 0),
						"cancel": permission.get("cancel", 0),
						"amend": permission.get("amend", 0),
						"print": permission.get("print", 0),
						"email": permission.get("email", 0),
						"report": permission.get("report", 0),
						"export": permission.get("export", 0),
						"share": permission.get("share", 0),
						"if_owner": permission.get("if_owner", 0)
					})

					docperm.insert(ignore_permissions=True)

		frappe.db.commit()

	except Exception as e:
		frappe.log_error(f"Error setting up permissions: {str(e)}")

# Permission validation functions

def validate_user_permissions(user, doctype, permission_type):
	"""Validate if user has specific permission for doctype"""
	try:
		if not user or user == "Guest":
			return False

		# Get user roles
		user_roles = frappe.get_roles(user)

		# Check if user has permission
		has_permission = frappe.has_permission(
			doctype=doctype,
			ptype=permission_type,
			user=user
		)

		return has_permission

	except Exception as e:
		frappe.log_error(f"Error validating user permissions: {str(e)}")
		return False

def get_user_accessible_doctypes(user, permission_type="read"):
	"""Get list of doctypes user can access"""
	try:
		if not user or user == "Guest":
			return []

		accessible_doctypes = []

		# Get all Sheria doctypes
		sheria_doctypes = [
			"Legal Case", "Case Hearing", "Court", "Lawyer", "Practice Area",
			"Legal Document", "Legal Research", "Service Request", "Legal Service",
			"Client", "Consultation", "Client Feedback", "Service Category"
		]

		for doctype in sheria_doctypes:
			if frappe.has_permission(doctype=doctype, ptype=permission_type, user=user):
				accessible_doctypes.append(doctype)

		return accessible_doctypes

	except Exception as e:
		frappe.log_error(f"Error getting accessible doctypes: {str(e)}")
		return []

def restrict_data_access(user, doctype, filters=None):
	"""Apply data access restrictions based on user role"""
	try:
		if not filters:
			filters = {}

		user_roles = frappe.get_roles(user)

		# Apply ownership restrictions for certain roles
		if "Lawyer" in user_roles or "Legal Assistant" in user_roles or "Paralegal" in user_roles:
			if doctype in ["Legal Case", "Service Request", "Consultation"]:
				filters["owner"] = user

		# Client role restrictions
		if "Client" in user_roles:
			if doctype == "Service Request":
				# Clients can only see their own requests
				client_email = frappe.db.get_value("User", user, "email")
				if client_email:
					client = frappe.db.exists("Client", {"email": client_email})
					if client:
						filters["client"] = client

		return filters

	except Exception as e:
		frappe.log_error(f"Error restricting data access: {str(e)}")
		return filters

# Permission API endpoints

@frappe.whitelist()
def get_user_permissions():
	"""API endpoint to get current user permissions"""
	try:
		user = frappe.session.user

		if user == "Guest":
			return {"permissions": {}}

		permissions = {}

		# Get accessible doctypes for different permission types
		permissions["read"] = get_user_accessible_doctypes(user, "read")
		permissions["write"] = get_user_accessible_doctypes(user, "write")
		permissions["create"] = get_user_accessible_doctypes(user, "create")

		# Get user roles
		permissions["roles"] = frappe.get_roles(user)

		return {"permissions": permissions}

	except Exception as e:
		frappe.log_error(f"Error getting user permissions: {str(e)}")
		return {"permissions": {}}

@frappe.whitelist()
def check_doctype_permission(doctype, permission_type):
	"""API endpoint to check specific doctype permission"""
	try:
		user = frappe.session.user

		has_permission = validate_user_permissions(user, doctype, permission_type)

		return {"has_permission": has_permission}

	except Exception as e:
		frappe.log_error(f"Error checking doctype permission: {str(e)}")
		return {"has_permission": False}

@frappe.whitelist()
def get_role_permissions(role_name):
	"""API endpoint to get permissions for a specific role"""
	try:
		roles_config = get_permission_config()["roles"]

		if role_name in roles_config:
			return {"permissions": roles_config[role_name]["permissions"]}
		else:
			return {"permissions": []}

	except Exception as e:
		frappe.log_error(f"Error getting role permissions: {str(e)}")
		return {"permissions": []}