# Sheria CRM Extensions

This module extends Frappe CRM with legal-specific functionality to replace the separate Client management system in Sheria.

## Overview

The CRM Extensions provide:
- **Legal CRM Lead**: Extended CRM Lead with KRA PIN validation, trust accounting, and legal fields
- **Legal CRM Deal**: Extended CRM Deal with case management, billing information, and legal workflow integration
- **Data Migration**: Scripts to migrate existing Client records to the new CRM structure

## Installation

1. **Install Frappe CRM** (if not already installed):
   ```bash
   bench get-app crm
   bench install-app crm
   ```

2. **Install CRM Extensions**:
   The extensions are automatically installed when you install the Sheria app.

3. **Run Migration** (optional, for existing data):
   ```python
   from sheria_app.crm_extensions.migrations.migrate_clients_to_crm import migrate_clients_to_crm_leads
   migrate_clients_to_crm_leads()
   ```

## Features

### Legal CRM Lead
- **KRA PIN Validation**: Validates Kenyan tax identification numbers
- **Client Type Management**: Individual vs Company client handling
- **Trust Balance Integration**: Real-time trust account balance display
- **Legal Fields**: Practice area, court, case priority
- **Enhanced Contact Creation**: Includes legal-specific contact information

### Legal CRM Deal
- **Case Management Integration**: Links to legal cases and matters
- **Billing Information**: Payment terms, credit limits, billing addresses
- **Trust Account Transactions**: View trust account activity within deals
- **Lawyer Assignment**: Assign lawyers to specific matters
- **Automatic Legal Case Creation**: Creates legal cases from won deals

## Usage

### Creating Legal Leads
1. Navigate to **CRM > Lead**
2. Select "Legal CRM Lead" doctype
3. Fill in client information including:
   - Client type (Individual/Company)
   - KRA PIN (required for tax compliance)
   - Legal practice area and court
   - Trust account information

### Managing Legal Deals
1. Convert qualified leads to deals
2. Add legal-specific information:
   - Case type and status
   - Assigned lawyer
   - Billing and payment terms
3. Monitor trust account balances
4. Track case progress through deal pipeline

### Integration Benefits
- **Unified Client View**: Single source of truth for all client interactions
- **Enhanced SLA Management**: Legal-specific response time tracking
- **Automated Workflows**: Lead-to-deal conversion with legal case creation
- **Compliance**: Built-in KRA PIN and regulatory validations
- **Financial Integration**: Trust accounting directly in CRM

## Configuration

### Required Doctypes
Ensure these Sheria doctypes exist:
- Practice Area
- Court
- Lawyer
- Case Type
- Case Status
- Trust Account Ledger
- Trust Account Transaction

### Permissions
The following roles have access to CRM Extensions:
- System Manager
- Legal Admin
- Lawyer

## Migration Guide

### From Separate Client Management
1. **Backup Data**: Always backup before migration
2. **Run Migration Script**: Execute the client migration
3. **Verify Data**: Check migrated leads for accuracy
4. **Update Workflows**: Modify any custom scripts using Client doctype
5. **Train Users**: Update user training for new CRM interface

### Field Mapping
| Client Field | CRM Lead Field | Notes |
|-------------|----------------|-------|
| client_name | lead_name/organization | Organization for companies |
| client_type | client_type | Same field |
| kra_pin | kra_pin | With validation |
| practice_area | practice_area | Same field |
| assigned_lawyer | lead_owner | Maps to lead owner |

## Troubleshooting

### Common Issues
1. **KRA PIN Validation Errors**: Ensure PIN follows format A/P + 9 digits + letter
2. **Migration Failures**: Check for duplicate KRA PINs before migration
3. **Permission Errors**: Ensure users have CRM Lead/Deal permissions

### Support
For issues with CRM Extensions:
1. Check Frappe CRM documentation
2. Review Sheria app logs
3. Contact development team

## Future Enhancements
- Integration with legal case management workflows
- Advanced trust accounting features
- Client portal integration
- Automated document generation
- Court deadline tracking