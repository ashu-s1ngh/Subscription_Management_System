# Brightloop User Flow Architecture

Based on the system architecture diagram:

```
                          Open Website
                               │
                               ▼
                          Landing Page
                               │
                               ▼
                        Login / Sign Up
                               │
                               ▼
                        Authenticated? ──No──► Login / Sign Up
                               │ (Yes)
                               ▼
                           User Role
                               │
      ┌────────────────────────┼────────────────────────┐
      ▼                        ▼                        ▼
    Admin                    Staff                   Customer
      │                        │                        │
      ▼                        ▼                        ▼
Admin Dashboard          Staff Dashboard         Customer Portal
      │                        │                        │
      ├─ Products & Plans      ├─ Customer Management   ├─ My Subscriptions
      ├─ Manage Customers      ├─ Manage Subscriptions  ├─ My Invoices
      ├─ Subscriptions         ├─ Quotations            └─ Account Settings
      ├─ Invoices & Payments   └─ Invoices & Payments           │
      ├─ Discounts & Taxes             │                        │
      ├─ Analytics & Reports           │                        │
      └─ Staff Management              │                        │
              │                        │                        │
              └────────────────────────┴────────────────────────┘
                                       │
                                       ▼
                                    Logout
```

## Role Permissions & Modules

### 1. Admin
- **Full Business Control**:
  - Products & Plans configuration
  - Customer directory & full CRUD
  - Subscriptions & Quotation approvals
  - Invoices & Payments ledger
  - Discount coupons & Tax rates
  - Business analytics & MRR reporting
  - Staff management & account provisioning

### 2. Staff
- **Daily Operations**:
  - Customer Management
  - Quotation preparation & conversion
  - Subscription management & activation
  - Invoice generation
  - Manual payment recording

### 3. Customer
- **Self-Service Customer Portal**:
  - View subscribed plans & statuses
  - View invoices & balance due
  - Payment history & receipts
  - Profile & account settings
