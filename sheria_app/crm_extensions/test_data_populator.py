#!/usr/bin/env python3
"""
Test Data Population Script for Sheria Legal Management System
Creates comprehensive test data for all doctypes in the system.
"""

import frappe
import random
from datetime import datetime
from frappe.utils import nowdate, add_days, add_months, getdate

def create_test_data():
    """Main function to create all test data"""
    print("Starting test data creation...")

    # Create data in dependency order
    create_legal_infrastructure()
    # Skip users/employees creation as it requires company setup
    # create_users_and_employees()
    create_crm_data()
    create_client_services_data()
    create_case_management_data()
    create_document_management_data()

    print("Test data creation completed!")

def create_legal_infrastructure():
    """Create courts, judges, lawyers, practice areas, etc."""
    print("Creating legal infrastructure...")

    # Court Types
    court_types = ["Supreme Court", "Court of Appeal", "High Court", "Magistrate Court", "Kadhi Court"]
    for ct in court_types:
        if not frappe.db.exists("Court Type", ct):
            doc = frappe.get_doc({
                "doctype": "Court Type",
                "court_type": ct,
                "description": f"{ct} of Kenya"
            })
            doc.insert()

    # Court Subtypes
    court_subtypes = ["Commercial", "Criminal", "Civil", "Family", "Constitutional", "Employment"]
    for cst in court_subtypes:
        if not frappe.db.exists("Court Subtype", cst):
            doc = frappe.get_doc({
                "doctype": "Court Subtype",
                "court_subtype": cst,
                "description": f"{cst} matters"
            })
            doc.insert()

    # Courts
    courts_data = [
        {"court_name": "Supreme Court of Kenya", "court_type": "Supreme Court", "location": "Nairobi"},
        {"court_name": "Nairobi High Court", "court_type": "High Court", "location": "Nairobi"},
        {"court_name": "Mombasa High Court", "court_type": "High Court", "location": "Mombasa"},
        {"court_name": "Kisumu High Court", "court_type": "High Court", "location": "Kisumu"},
        {"court_name": "Nakuru Chief Magistrate Court", "court_type": "Magistrate Court", "location": "Nakuru"},
        {"court_name": "Eldoret Chief Magistrate Court", "court_type": "Magistrate Court", "location": "Eldoret"},
        {"court_name": "KIPI Office", "court_type": "High Court", "location": "Nairobi"},
        {"court_name": "Companies Registry", "court_type": "High Court", "location": "Nairobi"},
        {"court_name": "Employment and Labour Relations Court", "court_type": "High Court", "location": "Nairobi"},
        {"court_name": "Nairobi Environment and Land Court", "court_type": "High Court", "location": "Nairobi"}
    ]

    for court_data in courts_data:
        if not frappe.db.exists("Court", court_data["court_name"]):
            doc = frappe.get_doc({
                "doctype": "Court",
                "court_name": court_data["court_name"],
                "court_type": court_data["court_type"],
                "location": court_data["location"],
                "court_subtype": random.choice(court_subtypes)
            })
            doc.insert()

    # Judges
    judges_data = [
        {"judge_name": "Justice Mary Ang'awa", "court": "Supreme Court of Kenya"},
        {"judge_name": "Justice Smokin Wanjala", "court": "Nairobi High Court"},
        {"judge_name": "Justice Jairus Ngaah", "court": "Nairobi High Court"},
        {"judge_name": "Justice Reuben Nyakundi", "court": "Mombasa High Court"},
        {"judge_name": "Justice Christine Meoli", "court": "Kisumu High Court"}
    ]

    for judge_data in judges_data:
        if not frappe.db.exists("Judge", judge_data["judge_name"]):
            doc = frappe.get_doc({
                "doctype": "Judge",
                "judge_name": judge_data["judge_name"],
                "court": judge_data["court"],
                "specialization": random.choice(["Commercial Law", "Criminal Law", "Constitutional Law", "Family Law"])
            })
            doc.insert()

    # Practice Areas
    practice_areas = [
        "Corporate Law", "Criminal Law", "Family Law", "Property Law", "Employment Law",
        "Intellectual Property", "Tax Law", "Environmental Law", "Human Rights", "Immigration Law",
        "Medical Law", "Education Law"
    ]

    for pa in practice_areas:
        if not frappe.db.exists("Practice Area", pa):
            doc = frappe.get_doc({
                "doctype": "Practice Area",
                "practice_area_name": pa,
                "description": f"Legal practice in {pa.lower()}"
            })
            doc.insert()

    # Specializations
    specializations = [
        "Mergers & Acquisitions", "Contract Drafting", "Litigation", "Arbitration",
        "Tax Planning", "Estate Planning", "Intellectual Property Registration", "Employment Disputes"
    ]

    for spec in specializations:
        if not frappe.db.exists("Specialization", spec):
            doc = frappe.get_doc({
                "doctype": "Specialization",
                "specialization_name": spec,
                "description": f"Specialized legal services in {spec.lower()}"
            })
            doc.insert()

    # Case Types
    case_types = [
        "Civil Suit", "Criminal Case", "Constitutional Petition", "Employment Dispute",
        "Family Matter", "Commercial Dispute", "Tax Appeal", "Land Dispute",
        "Divorce Proceedings", "Trademark Registration", "Property Dispute", "Medical Malpractice",
        "Unfair Dismissal", "Company Incorporation", "Contract Breach"
    ]

    for ct in case_types:
        if not frappe.db.exists("Case Type", ct):
            doc = frappe.get_doc({
                "doctype": "Case Type",
                "case_type": ct,
                "description": f"{ct} legal proceedings",
                "practice_area": random.choice(practice_areas)
            })
            doc.insert()

    # Lawyers
    lawyers_data = [
        {"lawyer_name": "Adv. Sarah Wanjiku", "email": "sarah.wanjiku@lawfirm.com", "phone": "+254712345678"},
        {"lawyer_name": "Adv. David Kiprop", "email": "david.kiprop@lawfirm.com", "phone": "+254723456789"},
        {"lawyer_name": "Adv. Grace Achieng", "email": "grace.achieng@lawfirm.com", "phone": "+254734567890"},
        {"lawyer_name": "Adv. Michael Oduya", "email": "michael.oduya@lawfirm.com", "phone": "+254745678901"},
        {"lawyer_name": "Adv. Linda Cherono", "email": "linda.cherono@lawfirm.com", "phone": "+254756789012"},
        {"lawyer_name": "Adv. Peter Kipkoech", "email": "peter.kipkoech@lawfirm.com", "phone": "+254767890123"}
    ]

    for lawyer_data in lawyers_data:
        if not frappe.db.exists("Lawyer", lawyer_data["lawyer_name"]):
            doc = frappe.get_doc({
                "doctype": "Lawyer",
                "lawyer_name": lawyer_data["lawyer_name"],
                "email": lawyer_data["email"],
                "phone": lawyer_data["phone"],
                "practice_area": random.choice(practice_areas),
                "specialization": random.choice(specializations),
                "bar_registration_number": f"ADV{random.randint(1000, 9999)}",
                "years_of_experience": random.randint(3, 25)
            })
            doc.insert()

def create_users_and_employees():
    """Create test users and employees"""
    print("Creating users and employees...")

    # Create some test employees
    employees_data = [
        {"first_name": "John", "last_name": "Doe", "email": "john.doe@lawfirm.com", "designation": "Senior Partner"},
        {"first_name": "Jane", "last_name": "Smith", "email": "jane.smith@lawfirm.com", "designation": "Associate Lawyer"},
        {"first_name": "Bob", "last_name": "Johnson", "email": "bob.johnson@lawfirm.com", "designation": "Legal Assistant"},
        {"first_name": "Alice", "last_name": "Brown", "email": "alice.brown@lawfirm.com", "designation": "Paralegal"}
    ]

    for emp_data in employees_data:
        if not frappe.db.exists("Employee", {"employee_name": f"{emp_data['first_name']} {emp_data['last_name']}"}):
            emp = frappe.get_doc({
                "doctype": "Employee",
                "first_name": emp_data["first_name"],
                "last_name": emp_data["last_name"],
                "employee_name": f"{emp_data['first_name']} {emp_data['last_name']}",
                "company": "Sheria Law Firm",
                "designation": emp_data["designation"],
                "department": "Legal",
                "date_of_joining": add_days(nowdate(), -random.randint(30, 1000))
            })
            emp.insert()

def create_crm_data():
    """Create CRM leads and deals"""
    print("Creating CRM data...")

    # Create basic CRM Lead Status if it doesn't exist
    try:
        if not frappe.db.exists("CRM Lead Status", "Open"):
            doc = frappe.get_doc({
                "doctype": "CRM Lead Status",
                "status_name": "Open",
                "color": "#28a745"
            })
            doc.insert()
    except Exception as e:
        print(f"Skipping CRM Lead Status creation: {e}")

    try:
        if not frappe.db.exists("CRM Lead Status", "Qualified"):
            doc = frappe.get_doc({
                "doctype": "CRM Lead Status",
                "status_name": "Qualified",
                "color": "#007bff"
            })
            doc.insert()
    except Exception as e:
        print(f"Skipping CRM Lead Status creation: {e}")

    # Create CRM Deal Status records
    deal_statuses = [
        {"status_name": "Qualification", "color": "#007bff"},
        {"status_name": "Proposal", "color": "#17a2b8"},
        {"status_name": "Negotiation", "color": "#ffc107"},
        {"status_name": "Closed Won", "color": "#28a745"},
        {"status_name": "Closed Lost", "color": "#dc3545"}
    ]

    for status_data in deal_statuses:
        try:
            if not frappe.db.exists("CRM Deal Status", status_data["status_name"]):
                doc = frappe.get_doc({
                    "doctype": "CRM Deal Status",
                    **status_data
                })
                doc.insert()
        except Exception as e:
            print(f"Skipping CRM Deal Status creation for {status_data['status_name']}: {e}")

    # Skip lead creation to avoid dependency issues - create deals directly
    # Legal CRM Deals
    deals_data = [
        {
            "deal_name": "ABC Manufacturing - Contract Review",
            "naming_series": "CRM-DEAL-.YYYY.-",
            "deal_owner": "Administrator",
            "expected_deal_value": 250000,
            "currency": "KES",
            "expected_closure_date": frappe.utils.add_days(frappe.utils.nowdate(), 30),
            "probability": 75,
            "status": "Qualification",
            "practice_area": "Corporate Law",
            "client_type": "Company",
            "organization": "ABC Manufacturing Ltd",
            "first_name": "ABC Manufacturing",
            "company_registration_number": "CPR-2020-123456",
            "case_type": "Commercial Dispute",
            "case_status": "Active",
            "case_priority": "High",
            "court": "Nairobi High Court",
            "assigned_lawyer": "Adv. Sarah Wanjiku",
            "kra_pin": "P123456789A",
            "billing_address": "ABC Manufacturing Ltd\nIndustrial Area\nNairobi, Kenya"
        },
        {
            "deal_name": "Mary Johnson - Divorce Case",
            "deal_owner": "Administrator",
            "expected_deal_value": 150000,
            "currency": "KES",
            "expected_closure_date": frappe.utils.add_days(frappe.utils.nowdate(), 60),
            "probability": 90,
            "status": "Negotiation",
            "practice_area": "Family Law",
            "client_type": "Individual",
            "first_name": "Mary",
            "last_name": "Johnson",
            "case_type": "Divorce Proceedings",
            "case_status": "Active",
            "case_priority": "Medium",
            "court": "Nakuru Chief Magistrate Court",
            "assigned_lawyer": "Adv. Grace Achieng",
            "kra_pin": "A123456789B",
            "id_passport_number": "12345678",
            "billing_address": "123 Main Street\nNakuru, Kenya"
        },
        {
            "deal_name": "TechStart Solutions - IP Protection",
            "deal_owner": "Administrator",
            "expected_deal_value": 350000,
            "currency": "KES",
            "expected_closure_date": frappe.utils.add_days(frappe.utils.nowdate(), 45),
            "probability": 60,
            "status": "Qualification",
            "practice_area": "Intellectual Property",
            "client_type": "Company",
            "organization": "TechStart Solutions",
            "first_name": "TechStart Solutions",
            "company_registration_number": "CPR-2019-234567",
            "case_type": "Trademark Registration",
            "case_status": "Pending",
            "case_priority": "Medium",
            "court": "KIPI Office",
            "assigned_lawyer": "Adv. David Kiprop",
            "kra_pin": "P987654321C",
            "billing_address": "TechStart Solutions\nWestlands\nNairobi, Kenya"
        },
        {
            "deal_name": "Green Valley Estate - Property Dispute",
            "deal_owner": "Administrator",
            "expected_deal_value": 500000,
            "currency": "KES",
            "expected_closure_date": frappe.utils.add_days(frappe.utils.nowdate(), 90),
            "probability": 40,
            "status": "Proposal",
            "practice_area": "Property Law",
            "client_type": "Company",
            "organization": "Green Valley Estate Ltd",
            "first_name": "Green Valley Estate",
            "company_registration_number": "CPR-2018-345678",
            "case_type": "Property Dispute",
            "case_status": "Active",
            "case_priority": "High",
            "court": "Nairobi Environment and Land Court",
            "assigned_lawyer": "Adv. Sarah Wanjiku",
            "kra_pin": "P456789123D",
            "billing_address": "Green Valley Estate\nKaren\nNairobi, Kenya"
        },
        {
            "deal_name": "Dr. Ahmed Hassan - Medical Malpractice",
            "deal_owner": "Administrator",
            "expected_deal_value": 750000,
            "currency": "KES",
            "expected_closure_date": frappe.utils.add_days(frappe.utils.nowdate(), 120),
            "probability": 30,
            "status": "Negotiation",
            "practice_area": "Medical Law",
            "client_type": "Individual",
            "first_name": "Ahmed",
            "last_name": "Hassan",
            "case_type": "Medical Malpractice",
            "case_status": "Active",
            "case_priority": "High",
            "court": "Nairobi High Court",
            "assigned_lawyer": "Adv. Grace Achieng",
            "kra_pin": "A567891234E",
            "id_passport_number": "87654321",
            "billing_address": "456 Medical Plaza\nParklands\nNairobi, Kenya"
        },
        {
            "deal_name": "East African Traders - Employment Dispute",
            "deal_owner": "Administrator",
            "expected_deal_value": 200000,
            "currency": "KES",
            "expected_closure_date": frappe.utils.add_days(frappe.utils.nowdate(), 25),
            "probability": 85,
            "status": "Proposal",
            "practice_area": "Employment Law",
            "client_type": "Company",
            "organization": "East African Traders Ltd",
            "first_name": "East African Traders",
            "company_registration_number": "CPR-2021-456789",
            "case_type": "Unfair Dismissal",
            "case_status": "Active",
            "case_priority": "Medium",
            "court": "Employment and Labour Relations Court",
            "assigned_lawyer": "Adv. David Kiprop",
            "kra_pin": "P234567891F",
            "billing_address": "East African Traders\nRiver Road\nNairobi, Kenya"
        },
        {
            "deal_name": "Nairobi Tech Hub - Startup Incorporation",
            "deal_owner": "Administrator",
            "expected_deal_value": 100000,
            "currency": "KES",
            "expected_closure_date": frappe.utils.add_days(frappe.utils.nowdate(), 15),
            "probability": 95,
            "status": "Qualification",
            "practice_area": "Corporate Law",
            "client_type": "Company",
            "organization": "Nairobi Tech Hub Ltd",
            "first_name": "Nairobi Tech Hub",
            "company_registration_number": "CPR-2022-567890",
            "case_type": "Company Incorporation",
            "case_status": "Pending",
            "case_priority": "Low",
            "court": "Companies Registry",
            "assigned_lawyer": "Adv. Sarah Wanjiku",
            "kra_pin": "P345678912G",
            "billing_address": "Nairobi Tech Hub\nSilicon Savannah\nNairobi, Kenya"
        },
        {
            "deal_name": "Prof. Jane Mwangi - Academic Dispute",
            "deal_owner": "Administrator",
            "expected_deal_value": 300000,
            "currency": "KES",
            "expected_closure_date": frappe.utils.add_days(frappe.utils.nowdate(), 75),
            "probability": 50,
            "status": "Negotiation",
            "practice_area": "Education Law",
            "client_type": "Individual",
            "first_name": "Jane",
            "last_name": "Mwangi",
            "case_type": "Contract Breach",
            "case_status": "Active",
            "case_priority": "Medium",
            "court": "Nairobi High Court",
            "assigned_lawyer": "Adv. Grace Achieng",
            "kra_pin": "A678912345H",
            "id_passport_number": "11223344",
            "billing_address": "University of Nairobi\nMain Campus\nNairobi, Kenya"
        }
    ]

    for deal_data in deals_data:
        if not frappe.db.exists("Legal CRM Deal", deal_data["deal_name"]):
            print(f"Creating deal: {deal_data['deal_name']}")
            # Try direct database insert to bypass validation issues
            deal_name = deal_data["deal_name"]
            frappe.db.sql("""
                INSERT INTO `tabLegal CRM Deal` 
                (name, creation, modified, modified_by, owner, docstatus, naming_series, status, client_type, organization, first_name, company_registration_number)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                deal_name,
                frappe.utils.now(),
                frappe.utils.now(),
                'Administrator',
                'Administrator',
                0,
                'CRM-DEAL-.YYYY.-',
                'Qualification',
                deal_data["client_type"],
                deal_data.get("organization"),
                deal_data.get("first_name"),
                deal_data.get("company_registration_number")
            ))
            frappe.db.commit()
            print(f"Successfully inserted deal: {deal_name}")

def create_client_services_data():
    """Create service requests and legal services"""
    print("Creating client services data...")

    # Legal Services - Comprehensive test data (create first)
    legal_services_data = [
        {
            "service_code": "LS-001",
            "service_name": "Corporate Contract Drafting & Review",
            "category": "Corporate Law",
            "is_active": 1,
            "featured": 1,
            "description": "Professional drafting and review of corporate contracts including NDAs, service agreements, partnership agreements, and commercial contracts. Our experienced corporate lawyers ensure all contracts are legally sound and protect your business interests.",
            "requirements": "• Company registration documents\n• Contract specifications\n• Parties involved details\n• Desired contract terms",
            "timeline": "3-7 business days for standard contracts, 10-14 days for complex agreements",
            "deliverables": "• Draft contract document\n• Legal review report\n• Final executed contract\n• Contract management guidelines",
            "price": 15000,
            "currency": "KES",
            "billing_type": "Fixed Price",
            "estimated_duration": "1-2 weeks",
            "complexity_level": "Medium",
            "eligibility_criteria": "Available to registered companies and business entities in Kenya",
            "exclusions": "• International contracts requiring foreign law expertise\n• Contracts involving regulated industries (banking, insurance)",
            "terms_and_conditions": "• Payment due within 7 days of service delivery\n• Revisions included in the fixed price\n• Additional revisions billed at hourly rate"
        },
        {
            "service_code": "LS-002",
            "service_name": "Company Incorporation Services",
            "category": "Corporate Law",
            "is_active": 1,
            "featured": 1,
            "description": "Complete company registration services including name reservation, preparation of incorporation documents, and registration with the Companies Registry. Fast-track your business setup with our streamlined incorporation process.",
            "requirements": "• Proposed company name\n• Director/Shareholder details\n• Registered office address\n• Business activity description",
            "timeline": "5-10 business days",
            "deliverables": "• Certificate of Incorporation\n• Memorandum and Articles of Association\n• Share certificates\n• Tax registration\n• Business registration completion",
            "price": 35000,
            "currency": "KES",
            "billing_type": "Fixed Price",
            "estimated_duration": "1-2 weeks",
            "complexity_level": "Medium",
            "eligibility_criteria": "Available to Kenyan citizens and residents",
            "exclusions": "• Foreign-owned companies\n• Regulated entities (banks, insurance companies)",
            "terms_and_conditions": "• All government fees included\n• Name availability check included\n• Document preparation and filing included"
        },
        {
            "service_code": "LS-003",
            "service_name": "Trademark Registration & Protection",
            "category": "Intellectual Property",
            "is_active": 1,
            "featured": 1,
            "description": "Comprehensive trademark registration services including trademark search, filing, and protection. Safeguard your brand identity with professional IP protection services.",
            "requirements": "• Trademark/logo samples\n• Class of goods/services\n• Owner details\n• Priority countries (if applicable)",
            "timeline": "3-6 months (including government processing)",
            "deliverables": "• Trademark search report\n• Filing confirmation\n• Certificate of Registration\n• Protection strategy advice",
            "price": 45000,
            "currency": "KES",
            "billing_type": "Fixed Price",
            "estimated_duration": "3-6 months",
            "complexity_level": "High",
            "eligibility_criteria": "Available to trademark owners and applicants",
            "exclusions": "• International trademark protection\n• Domain name disputes",
            "terms_and_conditions": "• Government fees additional\n• Renewal services available\n• Opposition proceedings extra"
        },
        {
            "service_code": "LS-004",
            "service_name": "Divorce & Family Law Consultation",
            "category": "Family Law",
            "is_active": 1,
            "featured": 0,
            "description": "Compassionate and professional family law services including divorce proceedings, child custody arrangements, property division, and family dispute resolution.",
            "requirements": "• Marriage certificate\n• Children's birth certificates\n• Property documents\n• Financial statements",
            "timeline": "Initial consultation within 48 hours",
            "deliverables": "• Legal consultation report\n• Case strategy plan\n• Court document preparation\n• Mediation support",
            "price": 8000,
            "currency": "KES",
            "billing_type": "Hourly Rate",
            "estimated_duration": "Varies by case",
            "complexity_level": "High",
            "eligibility_criteria": "Available to married couples and family members",
            "exclusions": "• Criminal matters\n• International family law",
            "terms_and_conditions": "• Initial consultation fee required\n• Court fees additional\n• Mediation services available"
        },
        {
            "service_code": "LS-005",
            "service_name": "Property Conveyancing & Transfer",
            "category": "Property Law",
            "is_active": 1,
            "featured": 1,
            "description": "Complete property transfer and conveyancing services including title search, due diligence, contract preparation, and registration. Secure your property transactions with expert legal support.",
            "requirements": "• Property title documents\n• Seller/buyer identification\n• Property valuation report\n• Stamp duty payment",
            "timeline": "2-4 weeks",
            "deliverables": "• Title search report\n• Sale agreement\n• Transfer documents\n• Registration completion\n• Property handover assistance",
            "price": 25000,
            "currency": "KES",
            "billing_type": "Fixed Price",
            "estimated_duration": "2-4 weeks",
            "complexity_level": "Medium",
            "eligibility_criteria": "Available for property owners and buyers in Kenya",
            "exclusions": "• Commercial property transactions\n• International property transfers",
            "terms_and_conditions": "• Government fees additional\n• Title insurance available\n• Due diligence included"
        },
        {
            "service_code": "LS-006",
            "service_name": "Employment Law Advisory",
            "category": "Employment Law",
            "is_active": 1,
            "featured": 0,
            "description": "Expert employment law advice including contract drafting, dispute resolution, termination procedures, and workplace policy development. Protect your business and employees with compliant employment practices.",
            "requirements": "• Employment contracts\n• Company policies\n• Employee details\n• Dispute documentation",
            "timeline": "1-3 business days for standard advice",
            "deliverables": "• Legal opinion report\n• Contract templates\n• Policy recommendations\n• Dispute resolution strategy",
            "price": 12000,
            "currency": "KES",
            "billing_type": "Hourly Rate",
            "estimated_duration": "1-2 weeks",
            "complexity_level": "Medium",
            "eligibility_criteria": "Available to employers and employees",
            "exclusions": "• Litigation services\n• International employment law",
            "terms_and_conditions": "• Initial consultation included\n• Contract templates included\n• Follow-up support available"
        },
        {
            "service_code": "LS-007",
            "service_name": "Criminal Defense Legal Aid",
            "category": "Criminal Law",
            "is_active": 1,
            "featured": 0,
            "description": "Professional criminal defense services for accused persons. Our experienced criminal lawyers provide vigorous defense representation in all criminal matters.",
            "requirements": "• Charge sheet/police report\n• Case details\n• Witness information\n• Evidence documentation",
            "timeline": "Immediate response for urgent matters",
            "deliverables": "• Case assessment report\n• Defense strategy plan\n• Court representation\n• Bail application support",
            "price": 0,
            "currency": "KES",
            "billing_type": "Pro Bono",
            "estimated_duration": "Varies by case complexity",
            "complexity_level": "Very High",
            "eligibility_criteria": "Available to indigent accused persons",
            "exclusions": "• Commercial crimes\n• Organized crime cases",
            "terms_and_conditions": "• Means test required\n• Limited to eligible cases\n• Court fees may apply"
        },
        {
            "service_code": "LS-008",
            "service_name": "Tax Law Compliance & Advisory",
            "category": "Tax Law",
            "is_active": 1,
            "featured": 0,
            "description": "Comprehensive tax compliance services including tax planning, filing assistance, audit support, and tax dispute resolution. Ensure your tax affairs are in order with expert guidance.",
            "requirements": "• Financial statements\n• Tax records\n• Business registration\n• Previous tax returns",
            "timeline": "Monthly compliance support",
            "deliverables": "• Tax compliance calendar\n• Tax return preparation\n• Audit assistance\n• Tax planning advice",
            "price": 20000,
            "currency": "KES",
            "billing_type": "Retainer",
            "estimated_duration": "Ongoing",
            "complexity_level": "Medium",
            "eligibility_criteria": "Available to businesses and individuals",
            "exclusions": "• International tax matters\n• Tax evasion cases",
            "terms_and_conditions": "• Monthly retainer fee\n• Additional services extra\n• KRA filing included"
        },
        {
            "service_code": "LS-009",
            "service_name": "Immigration & Citizenship Services",
            "category": "Immigration Law",
            "is_active": 1,
            "featured": 0,
            "description": "Complete immigration services including visa applications, citizenship applications, work permits, and immigration dispute resolution. Navigate Kenya's immigration system with expert assistance.",
            "requirements": "• Passport copies\n• Birth certificates\n• Marriage certificates\n• Employment letters",
            "timeline": "2-8 weeks (depending on visa type)",
            "deliverables": "• Application preparation\n• Document verification\n• Immigration status updates\n• Appeal support",
            "price": 18000,
            "currency": "KES",
            "billing_type": "Fixed Price",
            "estimated_duration": "1-2 months",
            "complexity_level": "High",
            "eligibility_criteria": "Available to immigrants and Kenyan citizens",
            "exclusions": "• Asylum applications\n• Deportation cases",
            "terms_and_conditions": "• Government fees additional\n• Success not guaranteed\n• Document translation included"
        },
        {
            "service_code": "LS-010",
            "service_name": "Medical Malpractice Defense",
            "category": "Other",
            "is_active": 1,
            "featured": 0,
            "description": "Specialized legal defense for healthcare professionals facing malpractice claims. Our medical law experts provide comprehensive defense strategies and representation.",
            "requirements": "• Medical license\n• Incident report\n• Patient records\n• Witness statements",
            "timeline": "Immediate case assessment",
            "deliverables": "• Case evaluation report\n• Defense strategy development\n• Court representation\n• Settlement negotiation",
            "price": 50000,
            "currency": "KES",
            "billing_type": "Contingency",
            "estimated_duration": "6-18 months",
            "complexity_level": "Very High",
            "eligibility_criteria": "Available to licensed healthcare professionals",
            "exclusions": "• Criminal medical negligence\n• Professional misconduct cases",
            "terms_and_conditions": "• Contingency fee arrangement\n• Expert witness fees additional\n• Settlement approval required"
        }
    ]

    for ls_data in legal_services_data:
        if not frappe.db.exists("Legal Service", ls_data["service_code"]):
            try:
                doc = frappe.get_doc({
                    "doctype": "Legal Service",
                    **ls_data
                })
                doc.insert()
                print(f"Created legal service: {ls_data['service_name']}")
            except Exception as e:
                print(f"Error creating legal service {ls_data['service_name']}: {e}")

    # Service Requests (create after legal services)
    service_requests_data = [
        {
            "service": "LS-001",  # Corporate Contract Drafting & Review
            "client": "ABC Manufacturing Ltd",
            "description": "Need review of employment contract for new CEO",
            "status": "Submitted",
            "priority": "High",
            "urgency": "Normal",
            "request_date": nowdate(),
            "preferred_date": add_days(nowdate(), 7),
            "service_fee": 15000,
            "billing_type": "Fixed Price"
        },
        {
            "service": "LS-004",  # Divorce & Family Law Consultation
            "client": "Mary Johnson",
            "description": "Consultation regarding divorce proceedings and property division",
            "status": "In Progress",
            "priority": "Medium",
            "urgency": "Urgent",
            "request_date": add_days(nowdate(), -2),
            "preferred_date": add_days(nowdate(), 14),
            "service_fee": 8000,
            "billing_type": "Hourly Rate"
        },
        {
            "service": "LS-003",  # Trademark Registration & Protection
            "client": "Kenya Tech Solutions Ltd",
            "description": "Need to register company trademark and protect brand identity",
            "status": "Completed",
            "priority": "Medium",
            "urgency": "Normal",
            "request_date": add_days(nowdate(), -10),
            "preferred_date": add_days(nowdate(), 30),
            "service_fee": 45000,
            "billing_type": "Fixed Price",
            "actual_completion": add_days(nowdate(), -2),
            "payment_status": "Paid"
        },
        {
            "service": "LS-005",  # Property Conveyancing & Transfer
            "client": "XYZ Properties Ltd",
            "description": "Property transfer and conveyancing services for commercial property",
            "status": "Under Review",
            "priority": "High",
            "urgency": "Critical",
            "request_date": nowdate(),
            "preferred_date": add_days(nowdate(), 21),
            "service_fee": 25000,
            "billing_type": "Fixed Price"
        },
        {
            "service": "LS-002",  # Company Incorporation Services
            "client": "Kenya Tech Solutions Ltd",
            "description": "Complete company incorporation and registration services",
            "status": "Approved",
            "priority": "Medium",
            "urgency": "Normal",
            "request_date": add_days(nowdate(), -5),
            "preferred_date": add_days(nowdate(), 10),
            "service_fee": 35000,
            "billing_type": "Fixed Price"
        }
    ]

    for sr_data in service_requests_data:
        if not frappe.db.exists("Service Request", {"service": sr_data["service"], "client": sr_data["client"]}):
            try:
                doc = frappe.get_doc({
                    "doctype": "Service Request",
                    **sr_data
                })
                doc.insert()
                print(f"Created service request for: {sr_data['service']}")
            except Exception as e:
                print(f"Error creating service request for {sr_data['service']}: {e}")

def create_case_management_data():
    """Create legal cases, activities, hearings, tasks, and time entries"""
    print("Creating case management data...")

    # Legal Cases - Simplified test data
    cases_data = [
        {
            "header_case_number": "HC/NRB/2025/101",
            "header_case_year": "2025",
            "case_details_title": "ABC Manufacturing vs. XYZ Suppliers - Breach of Contract"
        },
        {
            "header_case_number": "FC/NRB/2025/102",
            "header_case_year": "2025",
            "case_details_title": "Mary Johnson - Divorce Proceedings"
        }
    ]

    case_name_mapping = {}

    for case_data in cases_data:
        if not frappe.db.exists("Legal Case", {"case_details_title": case_data["case_details_title"]}):
            doc = frappe.get_doc({
                "doctype": "Legal Case",
                **case_data
            })
            doc.insert()
            case_name_mapping[case_data["case_details_title"]] = doc.name
            print(f"Created case: {doc.name} for {case_data['case_details_title']}")
        else:
            # Find existing case
            existing_case = frappe.get_doc("Legal Case", {"case_details_title": case_data["case_details_title"]})
            case_name_mapping[case_data["case_details_title"]] = existing_case.name

    # Case Activities - Comprehensive test data
    activities_data = [
        # Activities for ABC Manufacturing vs. XYZ Suppliers case
        {
            "case": case_name_mapping.get("ABC Manufacturing vs. XYZ Suppliers - Breach of Contract", "ABC Manufacturing vs. XYZ Suppliers - Breach of Contract"),
            "activity_type": "Client Meeting",
            "date": add_days(nowdate(), -28),
            "description": "Initial client consultation to understand the breach of contract dispute. Client provided contract documents and explained the situation.",
            "performed_by": "Administrator",
            "time_spent": 2.5,
            "cost_incurred": 15000,
            "status": "Completed",
            "next_action": "Review contract documents",
            "next_action_date": add_days(nowdate(), -27),
            "notes": "Client is seeking damages of KES 2.5M for delayed delivery of raw materials."
        },
        {
            "case": case_name_mapping.get("ABC Manufacturing vs. XYZ Suppliers - Breach of Contract", "ABC Manufacturing vs. XYZ Suppliers - Breach of Contract"),
            "activity_type": "Research",
            "date": add_days(nowdate(), -26),
            "description": "Legal research on similar breach of contract cases and applicable commercial law provisions.",
            "performed_by": "Administrator",
            "time_spent": 4.0,
            "cost_incurred": 0,
            "status": "Completed",
            "notes": "Found relevant precedents from Commercial Court decisions."
        },
        {
            "case": case_name_mapping.get("ABC Manufacturing vs. XYZ Suppliers - Breach of Contract", "ABC Manufacturing vs. XYZ Suppliers - Breach of Contract"),
            "activity_type": "Drafting",
            "date": add_days(nowdate(), -24),
            "description": "Drafted initial petition and supporting affidavits for filing with the court.",
            "performed_by": "Administrator",
            "time_spent": 6.0,
            "cost_incurred": 5000,
            "status": "Completed",
            "next_action": "File petition with court",
            "next_action_date": add_days(nowdate(), -23)
        },
        {
            "case": case_name_mapping.get("ABC Manufacturing vs. XYZ Suppliers - Breach of Contract", "ABC Manufacturing vs. XYZ Suppliers - Breach of Contract"),
            "activity_type": "Court Filing",
            "date": add_days(nowdate(), -23),
            "description": "Filed initial petition, supporting documents, and court fees with Nairobi High Court Commercial Division.",
            "performed_by": "Administrator",
            "time_spent": 1.5,
            "cost_incurred": 25000,
            "status": "Completed",
            "notes": "Case number HC/NRB/2025/001 assigned. Court fee paid: KES 25,000."
        },
        {
            "case": case_name_mapping.get("ABC Manufacturing vs. XYZ Suppliers - Breach of Contract", "ABC Manufacturing vs. XYZ Suppliers - Breach of Contract"),
            "activity_type": "Phone Call",
            "date": add_days(nowdate(), -20),
            "description": "Called defendant's legal counsel to discuss possibility of settlement before formal service.",
            "performed_by": "Administrator",
            "time_spent": 0.5,
            "cost_incurred": 0,
            "status": "Completed",
            "notes": "Defendant's counsel indicated willingness to discuss settlement terms."
        },
        {
            "case": case_name_mapping.get("ABC Manufacturing vs. XYZ Suppliers - Breach of Contract", "ABC Manufacturing vs. XYZ Suppliers - Breach of Contract"),
            "activity_type": "Negotiation",
            "date": add_days(nowdate(), -18),
            "description": "Settlement negotiations with defendant's representatives. Discussed compensation terms and timeline.",
            "performed_by": "Administrator",
            "time_spent": 3.0,
            "cost_incurred": 0,
            "status": "Completed",
            "next_action": "Prepare settlement agreement",
            "next_action_date": add_days(nowdate(), -15)
        },
        {
            "case": case_name_mapping.get("ABC Manufacturing vs. XYZ Suppliers - Breach of Contract", "ABC Manufacturing vs. XYZ Suppliers - Breach of Contract"),
            "activity_type": "Document Collection",
            "date": add_days(nowdate(), -15),
            "description": "Collected additional evidence including delivery receipts, quality inspection reports, and correspondence.",
            "performed_by": "Administrator",
            "time_spent": 2.0,
            "cost_incurred": 3000,
            "status": "Completed"
        },
        {
            "case": case_name_mapping.get("ABC Manufacturing vs. XYZ Suppliers - Breach of Contract", "ABC Manufacturing vs. XYZ Suppliers - Breach of Contract"),
            "activity_type": "Witness Interview",
            "date": add_days(nowdate(), -12),
            "description": "Interviewed key witnesses including client's procurement manager and quality control officer.",
            "performed_by": "Administrator",
            "time_spent": 4.5,
            "cost_incurred": 0,
            "status": "Completed",
            "notes": "Witness statements recorded and signed."
        },
        {
            "case": case_name_mapping.get("ABC Manufacturing vs. XYZ Suppliers - Breach of Contract", "ABC Manufacturing vs. XYZ Suppliers - Breach of Contract"),
            "activity_type": "Hearing",
            "date": add_days(nowdate(), -8),
            "description": "Attended case management conference at Nairobi High Court. Judge set timeline for defense response.",
            "performed_by": "Administrator",
            "time_spent": 2.0,
            "cost_incurred": 5000,
            "status": "Completed",
            "next_action": "Prepare defense response",
            "next_action_date": add_days(nowdate(), 7)
        },
        {
            "case": case_name_mapping.get("ABC Manufacturing vs. XYZ Suppliers - Breach of Contract", "ABC Manufacturing vs. XYZ Suppliers - Breach of Contract"),
            "activity_type": "Administrative",
            "date": add_days(nowdate(), -5),
            "description": "Updated case file with court orders and prepared internal case progress report.",
            "performed_by": "Administrator",
            "time_spent": 1.0,
            "cost_incurred": 0,
            "status": "Completed"
        },
        # Activities for Mary Johnson divorce case
        {
            "case": case_name_mapping.get("Mary Johnson - Divorce Proceedings", "Mary Johnson - Divorce Proceedings"),
            "activity_type": "Client Meeting",
            "date": add_days(nowdate(), -16),
            "description": "Initial consultation with client regarding divorce proceedings. Discussed grounds for divorce and asset division.",
            "performed_by": "Administrator",
            "time_spent": 2.0,
            "cost_incurred": 12000,
            "status": "Completed",
            "next_action": "File divorce petition",
            "next_action_date": add_days(nowdate(), -14),
            "notes": "Client has two minor children. Contested divorce expected due to asset disputes."
        },
        {
            "case": case_name_mapping.get("Mary Johnson - Divorce Proceedings", "Mary Johnson - Divorce Proceedings"),
            "activity_type": "Research",
            "date": add_days(nowdate(), -15),
            "description": "Researched family law provisions regarding child custody, maintenance, and property division.",
            "performed_by": "Administrator",
            "time_spent": 3.5,
            "cost_incurred": 0,
            "status": "Completed"
        },
        {
            "case": case_name_mapping.get("Mary Johnson - Divorce Proceedings", "Mary Johnson - Divorce Proceedings"),
            "activity_type": "Drafting",
            "date": add_days(nowdate(), -14),
            "description": "Drafted divorce petition including grounds for divorce, child custody arrangements, and asset claims.",
            "performed_by": "Administrator",
            "time_spent": 5.0,
            "cost_incurred": 8000,
            "status": "Completed"
        },
        {
            "case": case_name_mapping.get("Mary Johnson - Divorce Proceedings", "Mary Johnson - Divorce Proceedings"),
            "activity_type": "Court Filing",
            "date": add_days(nowdate(), -13),
            "description": "Filed divorce petition with Nakuru Chief Magistrate Court Family Division.",
            "performed_by": "Administrator",
            "time_spent": 1.0,
            "cost_incurred": 15000,
            "status": "Completed",
            "notes": "Case number FC/NRB/2025/002 assigned. Court fee paid: KES 15,000."
        },
        {
            "case": case_name_mapping.get("Mary Johnson - Divorce Proceedings", "Mary Johnson - Divorce Proceedings"),
            "activity_type": "Phone Call",
            "date": add_days(nowdate(), -12),
            "description": "Called respondent's counsel to serve petition and discuss possibility of amicable settlement.",
            "performed_by": "Administrator",
            "time_spent": 0.75,
            "cost_incurred": 0,
            "status": "Completed",
            "notes": "Respondent's counsel indicated contested proceedings likely."
        },
        {
            "case": case_name_mapping.get("Mary Johnson - Divorce Proceedings", "Mary Johnson - Divorce Proceedings"),
            "activity_type": "Evidence Preparation",
            "date": add_days(nowdate(), -10),
            "description": "Prepared evidence including marriage certificate, birth certificates of children, and financial statements.",
            "performed_by": "Administrator",
            "time_spent": 3.0,
            "cost_incurred": 2000,
            "status": "Completed"
        },
        {
            "case": case_name_mapping.get("Mary Johnson - Divorce Proceedings", "Mary Johnson - Divorce Proceedings"),
            "activity_type": "Hearing",
            "date": add_days(nowdate(), -8),
            "description": "Attended preliminary hearing. Court ordered mediation and temporary maintenance arrangements.",
            "performed_by": "Administrator",
            "time_spent": 2.5,
            "cost_incurred": 3000,
            "status": "Completed",
            "next_action": "Attend mediation session",
            "next_action_date": add_days(nowdate(), 2)
        },
        {
            "case": case_name_mapping.get("Mary Johnson - Divorce Proceedings", "Mary Johnson - Divorce Proceedings"),
            "activity_type": "Settlement Discussion",
            "date": add_days(nowdate(), -5),
            "description": "Participated in court-ordered mediation session discussing child custody and property division.",
            "performed_by": "Administrator",
            "time_spent": 4.0,
            "cost_incurred": 0,
            "status": "Completed",
            "notes": "Partial agreement reached on child custody. Property division remains contested."
        },
        {
            "case": case_name_mapping.get("Mary Johnson - Divorce Proceedings", "Mary Johnson - Divorce Proceedings"),
            "activity_type": "Review",
            "date": add_days(nowdate(), -3),
            "description": "Reviewed mediation report and prepared for next court appearance. Advised client on settlement options.",
            "performed_by": "Administrator",
            "time_spent": 2.0,
            "cost_incurred": 0,
            "status": "Completed"
        },
        {
            "case": case_name_mapping.get("Mary Johnson - Divorce Proceedings", "Mary Johnson - Divorce Proceedings"),
            "activity_type": "Administrative",
            "date": add_days(nowdate(), -1),
            "description": "Updated case file with mediation outcomes and prepared client progress report.",
            "performed_by": "Administrator",
            "time_spent": 1.5,
            "cost_incurred": 0,
            "status": "Completed",
            "next_action": "Prepare for final hearing",
            "next_action_date": add_days(nowdate(), 10)
        }
    ]

    for activity_data in activities_data:
        doc = frappe.get_doc({
            "doctype": "Case Activity",
            **activity_data
        })
        doc.insert()

    # Case Hearings
    hearings_data = [
        {
            "case": case_name_mapping.get("ABC Manufacturing vs. XYZ Suppliers - Breach of Contract", "ABC Manufacturing vs. XYZ Suppliers - Breach of Contract"),
            "hearing_title": "Case Management Conference",
            "hearing_date": add_days(nowdate(), 7),
            "hearing_time": "10:00:00",
            "court": "Nairobi High Court",
            "judge": "Justice Jairus Ngaah",
            "hearing_type": "Case Management",
            "status": "Scheduled"
        },
        {
            "case": case_name_mapping.get("Mary Johnson - Divorce Proceedings", "Mary Johnson - Divorce Proceedings"),
            "hearing_title": "Settlement Conference",
            "hearing_date": add_days(nowdate(), 14),
            "hearing_time": "14:00:00",
            "court": "Nakuru Chief Magistrate Court",
            "judge": "Justice Christine Meoli",
            "hearing_type": "Other",
            "status": "Scheduled"
        }
    ]

    for hearing_data in hearings_data:
        doc = frappe.get_doc({
            "doctype": "Case Hearing",
            **hearing_data
        })
        doc.insert()

    # Tasks
    tasks_data = [
        {
            "subject": "Prepare witness statements",
            "description": "Prepare statements from key witnesses for upcoming hearing",
            "case": case_name_mapping.get("ABC Manufacturing vs. XYZ Suppliers - Breach of Contract", "ABC Manufacturing vs. XYZ Suppliers - Breach of Contract"),
            "assigned_to": "Administrator",
            "priority": "High",
            "due_date": add_days(nowdate(), 5),
            "status": "Open"
        },
        {
            "subject": "Review divorce settlement proposal",
            "description": "Review and advise on settlement proposal",
            "case": case_name_mapping.get("Mary Johnson - Divorce Proceedings", "Mary Johnson - Divorce Proceedings"),
            "assigned_to": "Administrator",
            "priority": "Medium",
            "due_date": add_days(nowdate(), 10),
            "status": "Working"
        }
    ]

    for task_data in tasks_data:
        doc = frappe.get_doc({
            "doctype": "Task",
            **task_data
        })
        doc.insert()

    # Time Entries - Commented out due to missing employees
    # time_entries_data = [
    #     {
    #         "case": case_name_mapping.get("ABC Manufacturing vs. XYZ Suppliers - Breach of Contract", "ABC Manufacturing vs. XYZ Suppliers - Breach of Contract"),
    #         "activity_type": "Research",
    #         "description": "Legal research on contract breach precedents",
    #         "hours": 4.5,
    #         "billing_rate": 5000,
    #         "billing_amount": 22500,
    #         "date": add_days(nowdate(), -2)
    #     },
    #     {
    #         "case": case_name_mapping.get("Mary Johnson - Divorce Proceedings", "Mary Johnson - Divorce Proceedings"),
    #         "activity_type": "Client Meeting",
    #         "description": "Client consultation on divorce proceedings",
    #         "hours": 2.0,
    #         "billing_rate": 4000,
    #         "billing_amount": 8000,
    #         "date": add_days(nowdate(), -1)
    #     }
    # ]

    # for te_data in time_entries_data:
    #     doc = frappe.get_doc({
    #         "doctype": "Time Entry",
    #         **te_data
    #     })
    #     doc.insert()

def create_document_management_data():
    """Create document templates and merge fields"""
    print("Creating document management data...")

    # Document Merge Fields
    merge_fields_data = [
        {"field_name": "client_name", "field_label": "Client Name", "field_type": "Text", "description": "Full name of the client"},
        {"field_name": "client_address", "field_label": "Client Address", "field_type": "Text", "description": "Client's address"},
        {"field_name": "client_contact_person", "field_label": "Client Contact Person", "field_type": "Text", "description": "Primary contact person for the client"},
        {"field_name": "agreement_date", "field_label": "Agreement Date", "field_type": "Date", "description": "Date of agreement"},
        {"field_name": "lawyer_name", "field_label": "Lawyer Name", "field_type": "Text", "description": "Name of the assigned lawyer"},
        {"field_name": "law_firm_name", "field_label": "Law Firm Name", "field_type": "Text", "description": "Name of the law firm"},
        {"field_name": "law_firm_address", "field_label": "Law Firm Address", "field_type": "Text", "description": "Law firm address"},
        {"field_name": "law_firm_phone", "field_label": "Law Firm Phone", "field_type": "Text", "description": "Law firm phone number"},
        {"field_name": "law_firm_email", "field_label": "Law Firm Email", "field_type": "Text", "description": "Law firm email address"},
        {"field_name": "case_number", "field_label": "Case Number", "field_type": "Text", "description": "Official case number"},
        {"field_name": "case_title", "field_label": "Case Title", "field_type": "Text", "description": "Title of the legal case"},
        {"field_name": "court_location", "field_label": "Court Location", "field_type": "Text", "description": "Location of the court"},
        {"field_name": "petitioner_name", "field_label": "Petitioner Name", "field_type": "Text", "description": "Name of the petitioner"},
        {"field_name": "respondent_name", "field_label": "Respondent Name", "field_type": "Text", "description": "Name of the respondent"},
        {"field_name": "filing_date", "field_label": "Filing Date", "field_type": "Date", "description": "Date the document was filed"},
        {"field_name": "retainer_amount", "field_label": "Retainer Amount", "field_type": "Currency", "description": "Amount of legal retainer"},
        {"field_name": "currency", "field_label": "Currency", "field_type": "Text", "description": "Currency code (e.g., KES, USD)"},
        {"field_name": "service_period", "field_label": "Service Period", "field_type": "Text", "description": "Period of legal services"},
        {"field_name": "services_scope", "field_label": "Services Scope", "field_type": "Text", "description": "Scope of legal services"},
        {"field_name": "payment_terms", "field_label": "Payment Terms", "field_type": "Text", "description": "Terms of payment"},
        {"field_name": "execution_date", "field_label": "Execution Date", "field_type": "Date", "description": "Date of document execution"},
        {"field_name": "principal_name", "field_label": "Principal Name", "field_type": "Text", "description": "Name of the principal in power of attorney"},
        {"field_name": "principal_address", "field_label": "Principal Address", "field_type": "Text", "description": "Address of the principal"},
        {"field_name": "attorney_name", "field_label": "Attorney Name", "field_type": "Text", "description": "Name of the attorney"},
        {"field_name": "attorney_address", "field_label": "Attorney Address", "field_type": "Text", "description": "Address of the attorney"},
        {"field_name": "expiry_date", "field_label": "Expiry Date", "field_type": "Date", "description": "Date of expiry"},
        {"field_name": "deponent_name", "field_label": "Deponent Name", "field_type": "Text", "description": "Name of the person making the affidavit"},
        {"field_name": "deponent_address", "field_label": "Deponent Address", "field_type": "Text", "description": "Address of the deponent"},
        {"field_name": "relationship_to_case", "field_label": "Relationship to Case", "field_type": "Text", "description": "Relationship of deponent to the case"},
        {"field_name": "statement_1", "field_label": "Statement 1", "field_type": "Text", "description": "First statement in affidavit"},
        {"field_name": "statement_2", "field_label": "Statement 2", "field_type": "Text", "description": "Second statement in affidavit"},
        {"field_name": "statement_3", "field_label": "Statement 3", "field_type": "Text", "description": "Third statement in affidavit"},
        {"field_name": "location", "field_label": "Location", "field_type": "Text", "description": "Location where document was signed"},
        {"field_name": "engagement_date", "field_label": "Engagement Date", "field_type": "Date", "description": "Date of engagement"},
        {"field_name": "matter_description", "field_label": "Matter Description", "field_type": "Text", "description": "Description of the legal matter"},
        {"field_name": "fee_structure", "field_label": "Fee Structure", "field_type": "Text", "description": "Structure of legal fees"},
        {"field_name": "limitations_clause", "field_label": "Limitations Clause", "field_type": "Text", "description": "Limitations in the engagement"},
        {"field_name": "acceptance_date", "field_label": "Acceptance Date", "field_type": "Date", "description": "Date of acceptance"},
        {"field_name": "seller_name", "field_label": "Seller Name", "field_type": "Text", "description": "Name of the property seller"},
        {"field_name": "seller_address", "field_label": "Seller Address", "field_type": "Text", "description": "Address of the property seller"},
        {"field_name": "buyer_name", "field_label": "Buyer Name", "field_type": "Text", "description": "Name of the property buyer"},
        {"field_name": "buyer_address", "field_label": "Buyer Address", "field_type": "Text", "description": "Address of the property buyer"},
        {"field_name": "property_description", "field_label": "Property Description", "field_type": "Text", "description": "Description of the property"},
        {"field_name": "purchase_price", "field_label": "Purchase Price", "field_type": "Currency", "description": "Price of the property"},
        {"field_name": "completion_date", "field_label": "Completion Date", "field_type": "Date", "description": "Date of completion"},
        {"field_name": "special_conditions", "field_label": "Special Conditions", "field_type": "Text", "description": "Special conditions of the agreement"},
        {"field_name": "application_number", "field_label": "Application Number", "field_type": "Text", "description": "Application number"},
        {"field_name": "applicant_name", "field_label": "Applicant Name", "field_type": "Text", "description": "Name of the applicant"},
        {"field_name": "applicant_address", "field_label": "Applicant Address", "field_type": "Text", "description": "Address of the applicant"},
        {"field_name": "applicant_nationality", "field_label": "Applicant Nationality", "field_type": "Text", "description": "Nationality of the applicant"},
        {"field_name": "trademark_description", "field_label": "Trademark Description", "field_type": "Text", "description": "Description of the trademark"},
        {"field_name": "trademark_class", "field_label": "Trademark Class", "field_type": "Text", "description": "Class of the trademark"},
        {"field_name": "goods_services_description", "field_label": "Goods/Services Description", "field_type": "Text", "description": "Description of goods or services"},
        {"field_name": "first_use_date", "field_label": "First Use Date", "field_type": "Date", "description": "Date of first use"},
        {"field_name": "application_date", "field_label": "Application Date", "field_type": "Date", "description": "Date of application"},
        {"field_name": "appellant_name", "field_label": "Appellant Name", "field_type": "Text", "description": "Name of the appellant"},
        {"field_name": "appellant_address", "field_label": "Appellant Address", "field_type": "Text", "description": "Address of the appellant"},
        {"field_name": "appeal_number", "field_label": "Appeal Number", "field_type": "Text", "description": "Number of the appeal"},
        {"field_name": "assessment_details", "field_label": "Assessment Details", "field_type": "Text", "description": "Details of the tax assessment"},
        {"field_name": "grounds_of_appeal", "field_label": "Grounds of Appeal", "field_type": "Text", "description": "Grounds for the appeal"},
        {"field_name": "relief_sought", "field_label": "Relief Sought", "field_type": "Text", "description": "Relief sought in the appeal"},
        {"field_name": "petition_date", "field_label": "Petition Date", "field_type": "Date", "description": "Date of the petition"},
        {"field_name": "case_details", "field_label": "Case Details", "field_type": "Text", "description": "Details of the criminal case"},
        {"field_name": "representation_scope", "field_label": "Representation Scope", "field_type": "Text", "description": "Scope of legal representation"},
        {"field_name": "client_responsibilities", "field_label": "Client Responsibilities", "field_type": "Text", "description": "Responsibilities of the client"},
        {"field_name": "permit_class", "field_label": "Permit Class", "field_type": "Text", "description": "Class of work permit"},
        {"field_name": "passport_number", "field_label": "Passport Number", "field_type": "Text", "description": "Passport number"},
        {"field_name": "nationality", "field_label": "Nationality", "field_type": "Text", "description": "Nationality"},
        {"field_name": "employer_name", "field_label": "Employer Name", "field_type": "Text", "description": "Name of the employer"},
        {"field_name": "employer_address", "field_label": "Employer Address", "field_type": "Text", "description": "Address of the employer"},
        {"field_name": "work_permit_number", "field_label": "Work Permit Number", "field_type": "Text", "description": "Work permit number"},
        {"field_name": "job_title", "field_label": "Job Title", "field_type": "Text", "description": "Job title"},
        {"field_name": "salary", "field_label": "Salary", "field_type": "Currency", "description": "Salary amount"},
        {"field_name": "qualifications", "field_label": "Qualifications", "field_type": "Text", "description": "Required qualifications"},
        {"field_name": "employer_representative", "field_label": "Employer Representative", "field_type": "Text", "description": "Name of employer representative"},
        {"field_name": "plaintiff_name", "field_label": "Plaintiff Name", "field_type": "Text", "description": "Name of the plaintiff"},
        {"field_name": "plaintiff_address", "field_label": "Plaintiff Address", "field_type": "Text", "description": "Address of the plaintiff"},
        {"field_name": "plaintiff_residence", "field_label": "Plaintiff Residence", "field_type": "Text", "description": "Residence of the plaintiff"},
        {"field_name": "defendant_name", "field_label": "Defendant Name", "field_type": "Text", "description": "Name of the defendant"},
        {"field_name": "defendant_address", "field_label": "Defendant Address", "field_type": "Text", "description": "Address of the defendant"},
        {"field_name": "incident_date", "field_label": "Incident Date", "field_type": "Date", "description": "Date of the incident"},
        {"field_name": "injuries_description", "field_label": "Injuries Description", "field_type": "Text", "description": "Description of injuries"},
        {"field_name": "damages_amount", "field_label": "Damages Amount", "field_type": "Currency", "description": "Amount of damages claimed"},
        {"field_name": "prayer_for_relief", "field_label": "Prayer for Relief", "field_type": "Text", "description": "Prayer for relief"},
        {"field_name": "complaint_date", "field_label": "Complaint Date", "field_type": "Date", "description": "Date of the complaint"},
        {"field_name": "project_title", "field_label": "Project Title", "field_type": "Text", "description": "Title of the project"},
        {"field_name": "proponent_name", "field_label": "Proponent Name", "field_type": "Text", "description": "Name of the project proponent"},
        {"field_name": "project_location", "field_label": "Project Location", "field_type": "Text", "description": "Location of the project"},
        {"field_name": "executive_summary", "field_label": "Executive Summary", "field_type": "Text", "description": "Executive summary of the report"},
        {"field_name": "project_description", "field_label": "Project Description", "field_type": "Text", "description": "Description of the project"},
        {"field_name": "environmental_baseline", "field_label": "Environmental Baseline", "field_type": "Text", "description": "Environmental baseline conditions"},
        {"field_name": "potential_impacts", "field_label": "Potential Impacts", "field_type": "Text", "description": "Potential environmental impacts"},
        {"field_name": "mitigation_measures", "field_label": "Mitigation Measures", "field_type": "Text", "description": "Environmental mitigation measures"},
        {"field_name": "environmental_management_plan", "field_label": "Environmental Management Plan", "field_type": "Text", "description": "Environmental management plan"},
        {"field_name": "conclusion", "field_label": "Conclusion", "field_type": "Text", "description": "Conclusion of the assessment"},
        {"field_name": "consultant_name", "field_label": "Consultant Name", "field_type": "Text", "description": "Name of the consultant"},
        {"field_name": "consultant_qualification", "field_label": "Consultant Qualification", "field_type": "Text", "description": "Qualification of the consultant"},
        {"field_name": "report_date", "field_label": "Report Date", "field_type": "Date", "description": "Date of the report"},
        {"field_name": "article_number", "field_label": "Article Number", "field_type": "Text", "description": "Constitution article number"},
        {"field_name": "violation_date", "field_label": "Violation Date", "field_type": "Date", "description": "Date of rights violation"},
        {"field_name": "violation_location", "field_label": "Violation Location", "field_type": "Text", "description": "Location of rights violation"},
        {"field_name": "violation_details", "field_label": "Violation Details", "field_type": "Text", "description": "Details of the rights violation"},
        {"field_name": "petition_number", "field_label": "Petition Number", "field_type": "Text", "description": "Number of the petition"},
        {"field_name": "school_name", "field_label": "School Name", "field_type": "Text", "description": "Name of the school"},
        {"field_name": "school_address", "field_label": "School Address", "field_type": "Text", "description": "Address of the school"},
        {"field_name": "policy_title", "field_label": "Policy Title", "field_type": "Text", "description": "Title of the policy"},
        {"field_name": "effective_date", "field_label": "Effective Date", "field_type": "Date", "description": "Date the policy becomes effective"},
        {"field_name": "policy_purpose", "field_label": "Policy Purpose", "field_type": "Text", "description": "Purpose of the policy"},
        {"field_name": "policy_scope", "field_label": "Policy Scope", "field_type": "Text", "description": "Scope of the policy"},
        {"field_name": "legal_framework", "field_label": "Legal Framework", "field_type": "Text", "description": "Legal framework for the policy"},
        {"field_name": "policy_statement", "field_label": "Policy Statement", "field_type": "Text", "description": "Statement of the policy"},
        {"field_name": "procedures", "field_label": "Procedures", "field_type": "Text", "description": "Procedures for implementation"},
        {"field_name": "responsibilities", "field_label": "Responsibilities", "field_type": "Text", "description": "Responsibilities under the policy"},
        {"field_name": "monitoring_review", "field_label": "Monitoring Review", "field_type": "Text", "description": "Monitoring and review procedures"},
        {"field_name": "approver_name", "field_label": "Approver Name", "field_type": "Text", "description": "Name of the policy approver"},
        {"field_name": "approver_position", "field_label": "Approver Position", "field_type": "Text", "description": "Position of the policy approver"},
        {"field_name": "approval_date", "field_label": "Approval Date", "field_type": "Date", "description": "Date of policy approval"}
    ]

    for mf_data in merge_fields_data:
        if not frappe.db.exists("Legal Document Merge Field", mf_data["field_name"]):
            doc = frappe.get_doc({
                "doctype": "Legal Document Merge Field",
                **mf_data
            })
            doc.insert()

    # Document Templates
    templates_data = [
        {
            "template_name": "Employment Contract Template",
            "description": "Standard employment contract template",
            "document_type": "Contract",
            "practice_area": "Employment Law",
            "is_active": 1,
            "template_content": """
<h1>EMPLOYMENT CONTRACT</h1>

This Employment Contract is made on {{agreement_date}} between:

<strong>Employer:</strong> {{company_name}}<br>
<strong>Employee:</strong> {{client_name}}<br>
<strong>Address:</strong> {{client_address}}

<strong>Position:</strong> {{position}}<br>
<strong>Commencement Date:</strong> {{start_date}}<br>
<strong>Salary:</strong> {{salary}}

Terms and conditions...

Signed: ____________________ Date: {{agreement_date}}
            """
        },
        {
            "template_name": "Divorce Petition Template",
            "description": "Standard divorce petition template",
            "document_type": "Petition",
            "practice_area": "Family Law",
            "is_active": 1,
            "template_content": """
<h1>DIVORCE PETITION</h1>

IN THE HIGH COURT OF KENYA AT NAIROBI

<div style="text-align: center;">
<strong>{{petitioner_name}}</strong><br>
PETITIONER
</div>

<div style="text-align: center;">
VERSUS
</div>

<div style="text-align: center;">
<strong>{{respondent_name}}</strong><br>
RESPONDENT
</div>

<strong>CASE NO:</strong> {{case_number}}

PETITION FOR DISSOLUTION OF MARRIAGE

The Petitioner states that...

Filed on: {{filing_date}}
            """
        },
        {
            "template_name": "Retainer Agreement Template",
            "description": "Legal services retainer agreement template",
            "document_type": "Retainer Agreement",
            "practice_area": "Corporate Law",
            "is_active": 1,
            "template_content": """
<h1>LEGAL SERVICES RETAINER AGREEMENT</h1>

This Retainer Agreement is made on {{agreement_date}} between:

<strong>Client:</strong> {{client_name}}<br>
<strong>Address:</strong> {{client_address}}<br>

<strong>Law Firm:</strong> {{law_firm_name}}<br>
<strong>Address:</strong> {{law_firm_address}}<br>

<strong>Retainer Amount:</strong> {{retainer_amount}} {{currency}}<br>
<strong>Services Period:</strong> {{service_period}}<br>

<strong>Scope of Services:</strong><br>
{{services_scope}}

<strong>Payment Terms:</strong><br>
{{payment_terms}}

Executed on: {{execution_date}}
            """
        },
        {
            "template_name": "Power of Attorney Template",
            "description": "General power of attorney template",
            "document_type": "Power of Attorney",
            "practice_area": "Corporate Law",
            "is_active": 1,
            "template_content": """
<h1>POWER OF ATTORNEY</h1>

KNOW ALL MEN BY THESE PRESENTS:

That I, {{principal_name}}, of {{principal_address}}, do hereby appoint {{attorney_name}}, of {{attorney_address}}, to be my true and lawful attorney-in-fact, with full power and authority to:

1. Manage and conduct all my business affairs<br>
2. Sign documents on my behalf<br>
3. Represent me in legal matters<br>
4. Collect debts and payments due to me<br>

This Power of Attorney shall remain in effect until {{expiry_date}}.

IN WITNESS WHEREOF, I have hereunto set my hand this {{execution_date}}.

_______________________________<br>
{{principal_name}}<br>
Principal
            """
        },
        {
            "template_name": "Affidavit Template",
            "description": "Standard affidavit template for court proceedings",
            "document_type": "Affidavit",
            "practice_area": "Criminal Law",
            "is_active": 1,
            "template_content": """
<h1>AFFIDAVIT</h1>

IN THE HIGH COURT OF KENYA AT {{court_location}}

<strong>{{case_title}}</strong><br>
CASE NO: {{case_number}}

I, {{deponent_name}}, of {{deponent_address}}, do hereby make oath and state as follows:

1. I am {{relationship_to_case}} and am conversant with the facts of this case.<br>
2. {{statement_1}}<br>
3. {{statement_2}}<br>
4. {{statement_3}}<br>

I make this affidavit in good faith believing the same to be true.

SWORN at {{location}} this {{date}}

_______________________________<br>
{{deponent_name}}<br>
Deponent

BEFORE ME

_______________________________<br>
Commissioner for Oaths
            """
        },
        {
            "template_name": "Engagement Letter Template",
            "description": "Client engagement letter for legal services",
            "document_type": "Engagement Letter",
            "practice_area": "Corporate Law",
            "is_active": 1,
            "template_content": """
<h1>ENGAGEMENT LETTER</h1>

<strong>{{law_firm_name}}</strong><br>
{{law_firm_address}}<br>
{{law_firm_phone}}<br>
{{law_firm_email}}<br>

<strong>Date:</strong> {{engagement_date}}

<strong>{{client_name}}</strong><br>
{{client_address}}

<strong>Dear {{client_contact_person}},</strong>

We are pleased to confirm our engagement by you to provide legal services in relation to {{matter_description}}.

<strong>Scope of Services:</strong><br>
{{services_scope}}

<strong>Fees:</strong><br>
{{fee_structure}}

<strong>Payment Terms:</strong><br>
{{payment_terms}}

<strong>Limitations:</strong><br>
{{limitations_clause}}

Please sign and return a copy of this letter to confirm your acceptance of these terms.

Yours sincerely,

_______________________________<br>
{{lawyer_name}}<br>
Partner

<strong>Accepted and Agreed:</strong><br>

_______________________________<br>
{{client_contact_person}}<br>
{{client_name}}<br>
Date: __________________________
            """
        },
        {
            "template_name": "Property Sale Agreement Template",
            "description": "Property sale agreement template",
            "document_type": "Contract",
            "practice_area": "Property Law",
            "is_active": 1,
            "template_content": """
<h1>PROPERTY SALE AGREEMENT</h1>

This Agreement is made on {{agreement_date}} between:

<strong>Seller:</strong> {{seller_name}}, of {{seller_address}} (hereinafter called "the Seller")<br>

<strong>Buyer:</strong> {{buyer_name}}, of {{buyer_address}} (hereinafter called "the Buyer")

<strong>Property Description:</strong><br>
{{property_description}}

<strong>Purchase Price:</strong> {{purchase_price}} {{currency}}

<strong>Payment Terms:</strong><br>
{{payment_terms}}

<strong>Completion Date:</strong> {{completion_date}}

<strong>Special Conditions:</strong><br>
{{special_conditions}}

IN WITNESS WHEREOF the parties hereto have set their hands on the day and year first above written.

SIGNED by the Seller:<br>
_______________________________<br>
{{seller_name}}

SIGNED by the Buyer:<br>
_______________________________<br>
{{buyer_name}}

In the presence of:<br>
_______________________________<br>
Witness
            """
        },
        {
            "template_name": "Trademark Registration Application Template",
            "description": "Trademark registration application template",
            "document_type": "Petition",
            "practice_area": "Intellectual Property",
            "is_active": 1,
            "template_content": """
<h1>TRADEMARK REGISTRATION APPLICATION</h1>

BEFORE THE DEPARTMENT OF INTELLECTUAL PROPERTY

<strong>Application No:</strong> {{application_number}}

<strong>Applicant:</strong> {{applicant_name}}<br>
<strong>Address:</strong> {{applicant_address}}<br>
<strong>Nationality:</strong> {{applicant_nationality}}

<strong>Trademark:</strong> {{trademark_description}}

<strong>Class:</strong> {{trademark_class}}

<strong>Goods/Services:</strong><br>
{{goods_services_description}}

<strong>Date of First Use:</strong> {{first_use_date}}

<strong>Application Date:</strong> {{application_date}}

I, {{applicant_name}}, hereby apply for registration of the above trademark under the Trademarks Act.

_______________________________<br>
{{applicant_name}}<br>
Applicant

Dated: {{application_date}}
            """
        },
        {
            "template_name": "Tax Appeal Petition Template",
            "description": "Tax appeal petition template",
            "document_type": "Petition",
            "practice_area": "Tax Law",
            "is_active": 1,
            "template_content": """
<h1>TAX APPEAL PETITION</h1>

IN THE HIGH COURT OF KENYA AT NAIROBI

<strong>Appellant:</strong> {{appellant_name}}<br>
<strong>Address:</strong> {{appellant_address}}

<strong>Respondent:</strong> The Commissioner of Domestic Taxes<br>
Kenya Revenue Authority

<strong>Appeal No:</strong> {{appeal_number}}

<strong>Original Assessment:</strong> {{assessment_details}}

<strong>Grounds of Appeal:</strong><br>
{{grounds_of_appeal}}

<strong>Relief Sought:</strong><br>
{{relief_sought}}

Dated: {{petition_date}}

_______________________________<br>
{{appellant_name}}<br>
Appellant

Through:<br>
_______________________________<br>
Advocate
            """
        },
        {
            "template_name": "Criminal Defense Engagement Template",
            "description": "Criminal defense engagement letter",
            "document_type": "Engagement Letter",
            "practice_area": "Criminal Law",
            "is_active": 1,
            "template_content": """
<h1>CRIMINAL DEFENSE ENGAGEMENT LETTER</h1>

<strong>{{law_firm_name}}</strong><br>
{{law_firm_address}}

<strong>{{client_name}}</strong><br>
{{client_address}}

<strong>Date:</strong> {{engagement_date}}

<strong>Re: Criminal Case - {{case_details}}</strong>

Dear {{client_name}},

We confirm our engagement to represent you in the above criminal matter.

<strong>Scope of Representation:</strong><br>
{{representation_scope}}

<strong>Legal Fees:</strong><br>
{{fee_structure}}

<strong>Retainer:</strong> {{retainer_amount}} {{currency}}

<strong>Payment Terms:</strong><br>
{{payment_terms}}

<strong>Client Responsibilities:</strong><br>
{{client_responsibilities}}

Please contact us immediately if you are arrested or charged with any offense.

Yours sincerely,

_______________________________<br>
{{lawyer_name}}<br>
Criminal Defense Attorney

<strong>Accepted:</strong><br>
_______________________________<br>
{{client_name}}<br>
Date: {{acceptance_date}}
            """
        },
        {
            "template_name": "Immigration Work Permit Application Template",
            "description": "Work permit application template",
            "document_type": "Petition",
            "practice_area": "Immigration Law",
            "is_active": 1,
            "template_content": """
<h1>WORK PERMIT APPLICATION</h1>

DIRECTORATE OF IMMIGRATION AND CITIZENSHIP SERVICES

<strong>Application for:</strong> Class {{permit_class}} Work Permit

<strong>Applicant:</strong> {{applicant_name}}<br>
<strong>Passport No:</strong> {{passport_number}}<br>
<strong>Nationality:</strong> {{nationality}}

<strong>Employer:</strong> {{employer_name}}<br>
<strong>Address:</strong> {{employer_address}}<br>
<strong>Work Permit No:</strong> {{work_permit_number}}

<strong>Position:</strong> {{job_title}}<br>
<strong>Salary:</strong> {{salary}} {{currency}}

<strong>Qualifications:</strong><br>
{{qualifications}}

<strong>Application Date:</strong> {{application_date}}

I declare that the information provided is true and correct.

_______________________________<br>
{{applicant_name}}<br>
Applicant

_______________________________<br>
{{employer_representative}}<br>
Employer Representative
            """
        },
        {
            "template_name": "Medical Malpractice Complaint Template",
            "description": "Medical malpractice complaint template",
            "document_type": "Petition",
            "practice_area": "Medical Law",
            "is_active": 1,
            "template_content": """
<h1>MEDICAL MALPRACTICE COMPLAINT</h1>

IN THE HIGH COURT OF KENYA AT {{court_location}}

<strong>Plaintiff:</strong> {{plaintiff_name}}<br>
<strong>Address:</strong> {{plaintiff_address}}

<strong>Defendant:</strong> {{defendant_name}}<br>
<strong>Address:</strong> {{defendant_address}}

<strong>Case No:</strong> {{case_number}}

<strong>COMPLAINT</strong>

1. Plaintiff is a resident of {{plaintiff_residence}}.<br>
2. Defendant is a medical practitioner licensed to practice in Kenya.<br>
3. On {{incident_date}}, Plaintiff sought medical treatment from Defendant.<br>
4. Defendant negligently provided medical care resulting in {{injuries_description}}.<br>
5. As a result of Defendant's negligence, Plaintiff suffered damages in the amount of {{damages_amount}} {{currency}}.

<strong>PRAYER</strong><br>
{{prayer_for_relief}}

Dated: {{complaint_date}}

_______________________________<br>
{{plaintiff_name}}<br>
Plaintiff

Through:<br>
_______________________________<br>
Advocate
            """
        },
        {
            "template_name": "Environmental Impact Assessment Template",
            "description": "Environmental compliance document template",
            "document_type": "Correspondence",
            "practice_area": "Environmental Law",
            "is_active": 1,
            "template_content": """
<h1>ENVIRONMENTAL IMPACT ASSESSMENT REPORT</h1>

<strong>Project Title:</strong> {{project_title}}<br>
<strong>Proponent:</strong> {{proponent_name}}<br>
<strong>Location:</strong> {{project_location}}

<strong>Executive Summary:</strong><br>
{{executive_summary}}

<strong>Project Description:</strong><br>
{{project_description}}

<strong>Environmental Baseline:</strong><br>
{{environmental_baseline}}

<strong>Potential Impacts:</strong><br>
{{potential_impacts}}

<strong>Mitigation Measures:</strong><br>
{{mitigation_measures}}

<strong>Environmental Management Plan:</strong><br>
{{environmental_management_plan}}

<strong>Conclusion:</strong><br>
{{conclusion}}

<strong>Report Prepared By:</strong><br>
{{consultant_name}}<br>
{{consultant_qualification}}<br>
Date: {{report_date}}
            """
        },
        {
            "template_name": "Human Rights Petition Template",
            "description": "Human rights violation petition template",
            "document_type": "Petition",
            "practice_area": "Human Rights",
            "is_active": 1,
            "template_content": """
<h1>HUMAN RIGHTS PETITION</h1>

BEFORE THE HIGH COURT OF KENYA AT NAIROBI

CONSTITUTIONAL AND HUMAN RIGHTS DIVISION

<strong>Petitioner:</strong> {{petitioner_name}}<br>
<strong>Address:</strong> {{petitioner_address}}

<strong>Respondent:</strong> {{respondent_name}}<br>
<strong>Address:</strong> {{respondent_address}}

<strong>Petition No:</strong> {{petition_number}}

<strong>PARTICULARS OF THE PETITION</strong>

1. The Petitioner alleges violation of fundamental rights under Article {{article_number}} of the Constitution.<br>
2. The violation occurred on {{violation_date}} at {{violation_location}}.<br>
3. Details of violation: {{violation_details}}<br>
4. The Petitioner has exhausted all other remedies available.<br>

<strong>PRAYER</strong><br>
{{prayer_for_relief}}

<strong>Verification:</strong><br>
I, {{petitioner_name}}, verify that the contents of this petition are true to the best of my knowledge.

_______________________________<br>
{{petitioner_name}}<br>
Petitioner

Dated: {{petition_date}}
            """
        },
        {
            "template_name": "Education Law Compliance Template",
            "description": "School policy and compliance document template",
            "document_type": "Correspondence",
            "practice_area": "Education Law",
            "is_active": 1,
            "template_content": """
<h1>SCHOOL COMPLIANCE POLICY</h1>

<strong>{{school_name}}</strong><br>
{{school_address}}

<strong>Policy Title:</strong> {{policy_title}}<br>
<strong>Effective Date:</strong> {{effective_date}}

<strong>Purpose:</strong><br>
{{policy_purpose}}

<strong>Scope:</strong><br>
{{policy_scope}}

<strong>Legal Framework:</strong><br>
{{legal_framework}}

<strong>Policy Statement:</strong><br>
{{policy_statement}}

<strong>Procedures:</strong><br>
{{procedures}}

<strong>Responsibilities:</strong><br>
{{responsibilities}}

<strong>Monitoring and Review:</strong><br>
{{monitoring_review}}

<strong>Approved By:</strong><br>
_______________________________<br>
{{approver_name}}<br>
{{approver_position}}<br>
Date: {{approval_date}}
            """
        }
    ]

    for template_data in templates_data:
        if not frappe.db.exists("Legal Document Template", template_data["template_name"]):
            doc = frappe.get_doc({
                "doctype": "Legal Document Template",
                **template_data
            })
            doc.insert()

if __name__ == "__main__":
    create_test_data()