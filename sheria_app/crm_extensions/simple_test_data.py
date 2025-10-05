import frappe
from frappe.utils import nowdate, add_days

def create_court_types():
    """Create court types"""
    court_types = ["Supreme Court", "Court of Appeal", "High Court", "Magistrate Court", "Kadhi Court"]
    for ct in court_types:
        if not frappe.db.exists("Court Type", ct):
            doc = frappe.get_doc({
                "doctype": "Court Type",
                "court_type": ct,
                "description": f"{ct} of Kenya"
            })
            doc.insert()
    print("Court types created")

def create_court_subtypes():
    """Create court subtypes"""
    court_subtypes = ["Commercial", "Criminal", "Civil", "Family", "Constitutional", "Employment"]
    for cst in court_subtypes:
        if not frappe.db.exists("Court Subtype", cst):
            doc = frappe.get_doc({
                "doctype": "Court Subtype",
                "court_subtype": cst,
                "description": f"{cst} matters"
            })
            doc.insert()
    print("Court subtypes created")

def create_courts():
    """Create courts"""
    courts_data = [
        {"court_name": "Supreme Court of Kenya", "court_type": "Supreme Court", "location": "Nairobi"},
        {"court_name": "Nairobi High Court", "court_type": "High Court", "location": "Nairobi"},
        {"court_name": "Mombasa High Court", "court_type": "High Court", "location": "Mombasa"},
        {"court_name": "Kisumu High Court", "court_type": "High Court", "location": "Kisumu"},
        {"court_name": "Eldoret High Court", "court_type": "High Court", "location": "Eldoret"},
        {"court_name": "Nakuru High Court", "court_type": "High Court", "location": "Nakuru"},
        {"court_name": "Nairobi Magistrate Court", "court_type": "Magistrate Court", "location": "Nairobi"},
        {"court_name": "Mombasa Magistrate Court", "court_type": "Magistrate Court", "location": "Mombasa"},
        {"court_name": "Kisumu Magistrate Court", "court_type": "Magistrate Court", "location": "Kisumu"},
        {"court_name": "Nairobi Kadhi Court", "court_type": "Kadhi Court", "location": "Nairobi"}
    ]

    for court_data in courts_data:
        if not frappe.db.exists("Court", court_data["court_name"]):
            doc = frappe.get_doc({
                "doctype": "Court",
                **court_data
            })
            doc.insert()
    print("Courts created")

def create_practice_areas():
    """Create practice areas"""
    practice_areas = [
        "Corporate Law", "Criminal Law", "Family Law", "Property Law", "Employment Law",
        "Intellectual Property", "Tax Law", "Environmental Law", "Constitutional Law",
        "Commercial Law", "Banking & Finance", "Insurance Law", "Maritime Law"
    ]
    for pa in practice_areas:
        if not frappe.db.exists("Practice Area", pa):
            doc = frappe.get_doc({
                "doctype": "Practice Area",
                "practice_area_name": pa,
                "description": f"Legal practice in {pa.lower()}"
            })
            doc.insert()
    print("Practice areas created")

def create_lawyers():
    """Create lawyers"""
    lawyers_data = [
        {"lawyer_name": "Adv. Sarah Wanjiku", "email": "sarah.wanjiku@lawfirm.com", "phone": "+254712345678"},
        {"lawyer_name": "Adv. David Kiprop", "email": "david.kiprop@lawfirm.com", "phone": "+254723456789"},
        {"lawyer_name": "Adv. Grace Achieng", "email": "grace.achieng@lawfirm.com", "phone": "+254734567890"},
        {"lawyer_name": "Adv. Michael Oduya", "email": "michael.oduya@lawfirm.com", "phone": "+254745678901"},
        {"lawyer_name": "Adv. Linda Kiprop", "email": "linda.kiprop@lawfirm.com", "phone": "+254756789012"},
        {"lawyer_name": "Adv. Peter Mwangi", "email": "peter.mwangi@lawfirm.com", "phone": "+254767890123"},
        {"lawyer_name": "Adv. Mary Wairimu", "email": "mary.wairimu@lawfirm.com", "phone": "+254778901234"},
        {"lawyer_name": "Adv. James Kiprotich", "email": "james.kiprotich@lawfirm.com", "phone": "+254789012345"}
    ]

    for lawyer_data in lawyers_data:
        if not frappe.db.exists("Lawyer", lawyer_data["lawyer_name"]):
            doc = frappe.get_doc({
                "doctype": "Lawyer",
                **lawyer_data
            })
            doc.insert()
    print("Lawyers created")

def create_crm_leads():
    """Create CRM leads"""
    leads_data = [
        {
            "lead_name": "John Smith",
            "first_name": "John",
            "last_name": "Smith",
            "email": "john.smith@email.com",
            "phone": "+254787654321",
            "client_type": "Individual",
            "id_passport_number": "12345678"
        },
        {
            "lead_name": "ABC Manufacturing Ltd",
            "company_name": "ABC Manufacturing Ltd",
            "email": "info@abc-manufacturing.co.ke",
            "phone": "+254700000001",
            "client_type": "Company",
            "industry": "Manufacturing"
        },
        {
            "lead_name": "Mary Johnson",
            "first_name": "Mary",
            "last_name": "Johnson",
            "email": "mary.johnson@email.com",
            "phone": "+254787654322",
            "client_type": "Individual",
            "id_passport_number": "87654321"
        },
        {
            "lead_name": "XYZ Properties Ltd",
            "company_name": "XYZ Properties Ltd",
            "email": "contact@xyzproperties.co.ke",
            "phone": "+254700000002",
            "client_type": "Company",
            "industry": "Real Estate"
        },
        {
            "lead_name": "David Brown",
            "first_name": "David",
            "last_name": "Brown",
            "email": "david.brown@email.com",
            "phone": "+254787654323",
            "client_type": "Individual",
            "id_passport_number": "11223344"
        }
    ]

    for lead_data in leads_data:
        if not frappe.db.exists("Legal CRM Lead", lead_data["lead_name"]):
            doc = frappe.get_doc({
                "doctype": "Legal CRM Lead",
                **lead_data
            })
            doc.insert()
    print("CRM leads created")

def create_legal_services():
    """Create legal services"""
    legal_services_data = [
        {
            "service_name": "Contract Drafting Service",
            "service_code": "CDS001",
            "description": "Professional contract drafting and review services",
            "service_category": "Corporate Services",
            "billing_type": "Hourly Rate",
            "standard_rate": 5000,
            "currency": "KES",
            "is_active": 1
        },
        {
            "service_name": "Legal Consultation",
            "service_code": "LC001",
            "description": "General legal consultation and advice services",
            "service_category": "General Legal Services",
            "billing_type": "Hourly Rate",
            "standard_rate": 3000,
            "currency": "KES",
            "is_active": 1
        },
        {
            "service_name": "Property Conveyancing",
            "service_code": "PC001",
            "description": "Property transfer and registration services",
            "service_category": "Property Law",
            "billing_type": "Fixed Fee",
            "standard_rate": 25000,
            "currency": "KES",
            "is_active": 1
        },
        {
            "service_name": "Employment Contract Review",
            "service_code": "ECR001",
            "description": "Review and drafting of employment contracts",
            "service_category": "Employment Law",
            "billing_type": "Hourly Rate",
            "standard_rate": 4000,
            "currency": "KES",
            "is_active": 1
        },
        {
            "service_name": "Family Law Consultation",
            "service_code": "FLC001",
            "description": "Family law matters including divorce and custody",
            "service_category": "Family Law",
            "billing_type": "Hourly Rate",
            "standard_rate": 3500,
            "currency": "KES",
            "is_active": 1
        },
        {
            "service_name": "Criminal Defense",
            "service_code": "CD001",
            "description": "Criminal defense and representation services",
            "service_category": "Criminal Law",
            "billing_type": "Hourly Rate",
            "standard_rate": 6000,
            "currency": "KES",
            "is_active": 1
        },
        {
            "service_name": "Company Registration",
            "service_code": "CR001",
            "description": "Business registration and incorporation services",
            "service_category": "Corporate Services",
            "billing_type": "Fixed Fee",
            "standard_rate": 15000,
            "currency": "KES",
            "is_active": 1
        },
        {
            "service_name": "Trademark Registration",
            "service_code": "TR001",
            "description": "Intellectual property registration services",
            "service_category": "Intellectual Property",
            "billing_type": "Fixed Fee",
            "standard_rate": 20000,
            "currency": "KES",
            "is_active": 1
        }
    ]

    for ls_data in legal_services_data:
        if not frappe.db.exists("Legal Service", ls_data["service_name"]):
            doc = frappe.get_doc({
                "doctype": "Legal Service",
                **ls_data
            })
            doc.insert()
    print("Legal services created")

def create_service_requests():
    """Create service requests"""
    # Ensure customers and legal services exist first
    create_customers()
    create_legal_services()
    
    service_requests_data = [
        {
            "subject": "Contract Review Request",
            "description": "Need review of employment contract",
            "service": "CDS001",
            "client": "John Smith",
            "status": "Draft",
            "priority": "High"
        },
        {
            "subject": "Company Registration Assistance",
            "description": "Help with registering a new manufacturing company",
            "service": "CR001",
            "client": "ABC Manufacturing Ltd",
            "status": "In Progress",
            "priority": "Medium"
        },
        {
            "subject": "Divorce Proceedings",
            "description": "Legal assistance for divorce and child custody",
            "service": "FLC001",
            "client": "Mary Johnson",
            "status": "Open",
            "priority": "High"
        },
        {
            "subject": "Property Purchase Agreement",
            "description": "Review property purchase contract and title",
            "service": "PC001",
            "client": "XYZ Properties Ltd",
            "status": "Completed",
            "priority": "Medium"
        },
        {
            "subject": "Criminal Defense Case",
            "description": "Legal representation for criminal charges",
            "service": "CD001",
            "client": "David Brown",
            "status": "In Progress",
            "priority": "High"
        },
        {
            "subject": "Trademark Registration",
            "description": "Register company trademark and brand protection",
            "service": "TR001",
            "client": "Kenya Tech Solutions Ltd",
            "status": "Open",
            "priority": "Medium"
        },
        {
            "subject": "Tax Compliance Review",
            "description": "Review tax obligations and compliance",
            "service": "LC001",
            "client": "Sarah Wilson",
            "status": "Draft",
            "priority": "Low"
        },
        {
            "subject": "Commercial Contract Drafting",
            "description": "Draft commercial supply agreement",
            "service": "CDS001",
            "client": "ABC Manufacturing Ltd",
            "status": "In Progress",
            "priority": "Medium"
        },
        {
            "subject": "Employment Contract Review",
            "description": "Review employment contract terms",
            "service": "ECR001",
            "client": "XYZ Properties Ltd",
            "status": "Open",
            "priority": "High"
        },
        {
            "subject": "Estate Planning Services",
            "description": "Will preparation and estate planning",
            "service": "LC001",
            "client": "John Smith",
            "status": "Completed",
            "priority": "Medium"
        }
    ]

    for sr_data in service_requests_data:
        if not frappe.db.exists("Service Request", {"subject": sr_data["subject"]}):
            doc = frappe.get_doc({
                "doctype": "Service Request",
                **sr_data
            })
            doc.insert()
    print("Service requests created")

def create_legal_cases():
    """Create legal cases"""
    # Ensure required doctypes have data first
    create_case_types()
    
    cases_data = [
        {
            "case_title": "ABC Manufacturing - Contract Dispute",
            "header_court": "Nairobi High Court",
            "header_case_type": "Civil Case",
            "header_case_number": "HC/NRB/2025/001",
            "header_case_year": 2025,
            "header_practice_area": "Corporate Law",
            "case_details_client_name": "John Smith",
            "case_details_date_opened": add_days(nowdate(), -30)
        },
        {
            "case_title": "XYZ Properties - Property Dispute",
            "header_court": "Nairobi Magistrates Court",
            "header_case_type": "Civil Case",
            "header_case_number": "MC/NRB/2025/002",
            "header_case_year": 2025,
            "header_practice_area": "Property Law",
            "case_details_client_name": "XYZ Properties Ltd",
            "case_details_date_opened": add_days(nowdate(), -20)
        },
        {
            "case_title": "Mary Johnson - Divorce Case",
            "header_court": "Nairobi Family Court",
            "header_case_type": "Family Case",
            "header_case_number": "FC/NRB/2025/003",
            "header_case_year": 2025,
            "header_practice_area": "Family Law",
            "case_details_client_name": "Mary Johnson",
            "case_details_date_opened": add_days(nowdate(), -15)
        },
        {
            "case_title": "David Brown - Criminal Defense",
            "header_court": "Nairobi Chief Magistrates Court",
            "header_case_type": "Criminal Case",
            "header_case_number": "CMC/NRB/2025/004",
            "header_case_year": 2025,
            "header_practice_area": "Criminal Law",
            "case_details_client_name": "David Brown",
            "case_details_date_opened": add_days(nowdate(), -10)
        },
        {
            "case_title": "Kenya Tech Solutions - IP Dispute",
            "header_court": "Nairobi High Court",
            "header_case_type": "Civil Case",
            "header_case_number": "HC/NRB/2025/005",
            "header_case_year": 2025,
            "header_practice_area": "Intellectual Property",
            "case_details_client_name": "Kenya Tech Solutions Ltd",
            "case_details_date_opened": add_days(nowdate(), -25)
        },
        {
            "case_title": "ABC Manufacturing - Employment Dispute",
            "header_court": "Nairobi Employment Court",
            "header_case_type": "Employment Case",
            "header_case_number": "EC/NRB/2025/006",
            "header_case_year": 2025,
            "header_practice_area": "Employment Law",
            "case_details_client_name": "ABC Manufacturing Ltd",
            "case_details_date_opened": add_days(nowdate(), -35)
        },
        {
            "case_title": "Sarah Wilson - Tax Appeal",
            "header_court": "Nairobi High Court",
            "header_case_type": "Civil Case",
            "header_case_number": "HC/NRB/2025/007",
            "header_case_year": 2025,
            "header_practice_area": "Tax Law",
            "case_details_client_name": "Sarah Wilson",
            "case_details_date_opened": add_days(nowdate(), -5)
        },
        {
            "case_title": "John Smith - Estate Matter",
            "header_court": "Nairobi High Court",
            "header_case_type": "Civil Case",
            "header_case_number": "HC/NRB/2025/008",
            "header_case_year": 2025,
            "header_practice_area": "Estate Planning",
            "case_details_client_name": "John Smith",
            "case_details_date_opened": add_days(nowdate(), -40)
        }
    ]

    for case_data in cases_data:
        if not frappe.db.exists("Legal Case", case_data["case_title"]):
            doc = frappe.get_doc({
                "doctype": "Legal Case",
                **case_data
            })
            doc.insert()
    print("Legal cases created")

def create_customers():
    """Create customers"""
    customers_data = [
        {
            "customer_name": "John Smith",
            "customer_type": "Individual",
            "customer_group": "Individual",
            "territory": "Kenya"
        },
        {
            "customer_name": "ABC Manufacturing Ltd",
            "customer_type": "Company",
            "customer_group": "Commercial",
            "territory": "Kenya"
        },
        {
            "customer_name": "Mary Johnson",
            "customer_type": "Individual",
            "customer_group": "Individual",
            "territory": "Kenya"
        },
        {
            "customer_name": "XYZ Properties Ltd",
            "customer_type": "Company",
            "customer_group": "Commercial",
            "territory": "Kenya"
        },
        {
            "customer_name": "David Brown",
            "customer_type": "Individual",
            "customer_group": "Individual",
            "territory": "Kenya"
        },
        {
            "customer_name": "Kenya Tech Solutions Ltd",
            "customer_type": "Company",
            "customer_group": "Commercial",
            "territory": "Kenya"
        },
        {
            "customer_name": "Sarah Wilson",
            "customer_type": "Individual",
            "customer_group": "Individual",
            "territory": "Kenya"
        }
    ]

    for cust_data in customers_data:
        if not frappe.db.exists("Customer", cust_data["customer_name"]):
            doc = frappe.get_doc({
                "doctype": "Customer",
                **cust_data
            })
            doc.insert()
    print("Customers created")

def create_case_types():
    """Create case types"""
    case_types = ["Civil Case", "Criminal Case", "Family Case", "Commercial Case", "Constitutional Case"]
    for ct in case_types:
        if not frappe.db.exists("Case Type", ct):
            doc = frappe.get_doc({
                "doctype": "Case Type",
                "case_type": ct,
                "description": f"{ct} proceedings"
            })
            doc.insert()
    print("Case types created")

def create_default_crm_dashboard():
    """Create a default CRM dashboard"""
    # Check if a default dashboard already exists
    existing_default = frappe.db.exists("Legal CRM Dashboard", {"is_default": 1})
    if not existing_default:
        doc = frappe.get_doc({
            "doctype": "Legal CRM Dashboard",
            "dashboard_name": "Default CRM Dashboard",
            "is_default": 1,
            "date_range": "This Month"
        })
        doc.insert()
    print("Default CRM dashboard created")