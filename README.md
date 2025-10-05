# Sheria App - Law Management System

A comprehensive legal practice management system built on ERPNext v15, designed to streamline case management, time tracking, billing, client services, and trust accounting for law firms.

## Features

### 🏛️ Legal Practice Management
- **Case Management**: Complete case lifecycle management with status tracking, activities, and hearings
- **Time Tracking**: Billable time entry with approval workflows and automatic billing calculations
- **Task Management**: Assign and track tasks with priorities and due dates
- **Court Management**: Maintain court information and schedule hearings with reminders
- **Lawyer Profiles**: Manage lawyer information and assignments

### 👥 Client Services
- **Client Management**: Comprehensive client profiles with trust account balances
- **Service Requests**: Client service request workflow with approval processes
- **Legal Services**: Define and manage legal services with pricing
- **Consultations**: Schedule and manage client consultations
- **Feedback System**: Collect and analyze client satisfaction feedback

### 💰 Trust Accounting & Billing
- **Trust Account Transactions**: Secure recording of client fund deposits and withdrawals
- **Trust Account Ledger**: Complete audit trail of all trust account activities
- **Balance Validation**: Automatic balance checks and compliance validation
- **ERPNext Integration**: Seamless integration with Sales Invoice for billing
- **Compliance Reporting**: Generate trust accounting compliance reports

### 📊 Dashboards & Analytics
- **Interactive Dashboards**: Real-time metrics and KPIs for practice management
- **Case Analytics**: Case status distribution and performance metrics
- **Time Tracking Reports**: Billing analysis and productivity reports
- **Client Analytics**: Service performance and satisfaction trends
- **Trust Accounting Reports**: Balance monitoring and transaction analysis

### 🔄 Automated Workflows
- **Time Entry Approval**: Multi-level approval workflow for time entries
- **Service Request Approval**: Automated approval process for client services
- **Case Management**: Status-driven workflows for case progression
- **Email Notifications**: Automated reminders for hearings and deadlines

## DocTypes Implemented

### Core Legal Practice
- `Legal Case` - Main case management
- `Case Hearing` - Court hearing scheduling
- `Case Activity` - Case progress tracking
- `Time Entry` - Billable time recording
- `Task` - Task assignment and tracking
- `Court` - Court information management
- `Lawyer` - Legal professional profiles

### Client Services
- `Client` - Client profile management (enhanced with trust_balance)
- `Service Request` - Client service requests
- `Legal Service` - Service definitions
- `Service Category` - Service categorization
- `Consultation` - Client consultation scheduling
- `Client Feedback` - Feedback collection

### Trust Accounting
- `Trust Account Transaction` - Client fund transactions
- `Trust Account Ledger` - Audit trail ledger

## API Endpoints

### Billing Integration
- `generate_invoice_from_time_entries` - Create invoices from approved time entries
- `get_client_unbilled_time` - Retrieve unbilled time for clients
- `update_time_entry_billing_status` - Update billing status after invoicing

### Trust Accounting
- `validate_trust_balance` - Validate trust account balances
- `get_client_trust_balance` - Get current client trust balance
- `create_trust_ledger_entry` - Create ledger entries for transactions

### Client Services
- `get_client_service_history` - Get client's service history
- `calculate_service_fees` - Calculate fees for services

## Workspaces

### Legal Practice Workspace
- Quick actions for common tasks
- Recent cases and upcoming hearings
- Time entries and active tasks
- Pending invoices and unbilled time
- Case management charts and reports

### Client Services Workspace
- Active service requests and consultations
- Client feedback and service management
- Service performance analytics
- Client portfolio reports

### Trust Accounting Workspace
- Trust account overview and balances
- Recent transactions and audit trail
- Client balance monitoring
- Compliance reports and reconciliation

## Installation & Setup

1. **Install ERPNext v15**
2. **Install Sheria App**:
   ```bash
   bench get-app sheria https://github.com/your-repo/sheria
   bench install-app sheria
   ```
3. **Run Migrations**:
   ```bash
   bench migrate
   ```
4. **Create Workspaces**:
   ```python
   from sheria.sheria.workspace import create_default_workspaces
   create_default_workspaces()
   ```

## Configuration

### User Roles & Permissions
- **Legal Admin**: Full system access
- **Lawyer**: Case management and time tracking
- **Paralegal**: Task management and case activities
- **Assistant**: Basic data entry
- **Client**: Limited portal access

### Workflow Setup
1. Configure approval workflows in Workflow Settings
2. Set up email templates for notifications
3. Configure trust accounting rules and compliance settings

## Usage Guide

### Case Management
1. Create a new Legal Case
2. Assign lawyers and set case details
3. Schedule hearings and track activities
4. Record time entries for billable work
5. Generate invoices from approved time entries

### Trust Accounting
1. Record client fund deposits in Trust Account Transactions
2. System automatically updates client trust balances
3. Withdraw funds only when proper authorization is obtained
4. Review audit trail in Trust Account Ledger
5. Generate compliance reports regularly

### Client Services
1. Set up legal services and pricing
2. Clients can submit service requests
3. Schedule consultations and track feedback
4. Monitor service performance through dashboards

## Compliance & Security

- **Trust Accounting**: Compliant with legal ethics rules for client fund handling
- **Audit Trail**: Complete transaction history with user tracking
- **Data Security**: Role-based access control and data encryption
- **Backup & Recovery**: Automated backups with point-in-time recovery

## Support & Documentation

For detailed documentation, API references, and support:
- Visit the [Wiki](https://github.com/your-repo/sheria/wiki)
- Check [API Documentation](https://github.com/your-repo/sheria/api-docs)
- Report issues on [GitHub Issues](https://github.com/your-repo/sheria/issues)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

---

**Built with ❤️ for legal professionals worldwide**</content>
<parameter name="filePath">/Users/mac/ERPNext/lawms/apps/sheria/README.md# sheria_app
