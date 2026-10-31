# Brightloop API

FastAPI business-logic service for the Brightloop subscription MVP.

## Run locally

```bash
python -m venv .venv

# macOS/Linux
source .venv/bin/activate

# Windows PowerShell
# .venv\Scripts\Activate.ps1

python -m pip install -r backend/requirements.txt
python -m uvicorn app.main:app --app-dir backend --reload
```

The API will be available at `http://127.0.0.1:8000`; interactive documentation is at `http://127.0.0.1:8000/docs`. The canonical backend lives in `backend/`. The temporary store seeds one product and plan at startup. Send `X-Role: admin` or `X-Role: staff` while the Supabase Auth integration is being wired; the `require_role` dependency is the replacement point for JWT/Supabase claims.

## MVP endpoints

- `POST/GET /api/v1/products`, `/plans`, `/customers`, `/discounts`
- `POST/GET /api/v1/subscriptions`
- `PATCH /api/v1/subscriptions/{id}/status`
- `POST /api/v1/subscriptions/{id}/invoice`
- `GET /api/v1/invoices`
- `POST /api/v1/payments`
- `GET /api/v1/analytics`
# Brightloop — Subscription Management System

> **From customer registration to recurring revenue — everything managed in one place.**

Brightloop is a subscription management platform designed to help businesses manage products, subscription plans, customers, quotations, subscriptions, invoices, payments, discounts, and revenue reporting from one place.

This repository is being developed as a hackathon MVP. The goal is to demonstrate a complete subscription-to-payment workflow with role-based access.

---

## Table of Contents

- [1. Problem Statement](#1-problem-statement)
- [2. Project Goals](#2-project-goals)
- [3. Core Features](#3-core-features)
- [4. User Roles](#4-user-roles)
- [5. Main User Flow](#5-main-user-flow)
- [6. Subscription and Billing Pipeline](#6-subscription-and-billing-pipeline)
- [7. Technology Stack](#7-technology-stack)
- [8. System Architecture](#8-system-architecture)
- [9. Project Structure](#9-project-structure)
- [10. Database Design](#10-database-design)
- [11. API Contract](#11-api-contract)
- [12. Local Development Setup](#12-local-development-setup)
- [13. Environment Variables](#13-environment-variables)
- [14. Security](#14-security)
- [15. Demo Walkthrough](#15-demo-walkthrough)
- [16. MVP Scope and Future Improvements](#16-mvp-scope-and-future-improvements)
- [17. Team Responsibilities](#17-team-responsibilities)
- [18. Contributing](#18-contributing)

---

## 1. Problem Statement

Subscription-based businesses often manage customers and plans in spreadsheets, remember renewals manually, create invoices one by one, and reconcile payments separately.

This can lead to:
- Missed subscription renewals.
- Incorrect invoices.
- Payment tracking problems.
- Difficulty understanding recurring revenue.
- Increased manual work.

Brightloop aims to bring these operations into one platform and make the complete subscription lifecycle easier to manage.

## 2. Project Goals

- Centralize products, plans, customers, and subscriptions.
- Manage subscription states and billing periods.
- Generate invoices from subscriptions.
- Calculate applicable taxes and discounts.
- Record payments against invoices.
- Track outstanding balances and overdue invoices.
- Provide separate experiences for Admin, Staff, and Customers.
- Show business metrics such as active subscriptions and collected revenue.

## 3. Core Features

### Authentication and Access Control

- Email and password registration and login through Supabase Auth.
- Password reset through Supabase Auth.
- Role-based navigation for Admin, Staff, and Customer.
- Customer-specific data access.
- Secure authentication and authorization.

### Product and Plan Management

- Create and manage products.
- Store product name, type, sales price, cost price, and notes.
- Support product variants and price adjustments.
- Create subscription plans.
- Configure pricing and billing frequency.
- Support daily, weekly, monthly, and yearly billing cycles.
- Configure minimum quantities and plan availability dates.

### Customer and Quotation Management

- Maintain customer profiles.
- View customer subscription history.
- Prepare quotations using selected products and plans.
- Define quotation validity periods.
- Convert accepted quotations into subscriptions.

### Subscription Management

- Create subscriptions linked to customers and plans.
- Track start dates and expiry dates.
- Manage subscription items and quantities.
- Support Draft, Quotation, Confirmed, Active, Paused, and Closed states.
- Allow pause, resume, close, or renewal according to plan rules.

### Invoice and Billing Management

- Generate invoices from subscription details.
- Calculate subtotal, discounts, taxes, and final amounts.
- Generate unique invoice numbers.
- Track invoice issue dates and due dates.
- Prevent duplicate invoice generation for the same billing period.
- Support invoice confirmation and cancellation.

### Discounts and Payments

- Support fixed-amount and percentage discounts.
- Configure eligibility conditions and usage limits.
- Apply discounts automatically when eligible.
- Record payments against invoices.
- Store payment method, amount, date, and notes.
- Track paid amounts and outstanding balances.
- Mark invoices as Paid when fully paid.

### Dashboard and Analytics

- Display active subscription count.
- Display collected revenue.
- Display outstanding balances.
- Identify overdue invoices.
- Show revenue trends.
- Display subscription summaries.
- Provide date-based reporting where supported.

---

## 4. User Roles

| Role | Main Permissions |
|---|---|
| Admin | Full business access, products, plans, customers, subscriptions, invoices, payments, discounts, taxes, reports, and staff management. |
| Staff | Day-to-day customer operations, quotations, subscriptions, invoices, and payment records. |
| Customer | Access their own profile, subscriptions, invoices, and payment history. |

### Admin

- Manage products and plans.
- Manage customers.
- Create and manage subscriptions.
- Manage quotations.
- Generate and manage invoices.
- View and record payments.
- Configure taxes and discounts.
- View analytics and reports.
- Add and manage staff members.

### Staff

- View customers.
- Create quotations.
- Create subscriptions.
- Manage permitted subscription operations.
- Generate invoices.
- Record payments.
- Track overdue invoices.

Staff members cannot create other staff accounts or modify admin-only configurations.

### Customer

- Register and log in.
- View profile information.
- View available plans.
- View their own subscriptions.
- Check subscription status and renewal information.
- View their own invoices.
- View payment history.
- Manage permitted account settings.

Customers must never be able to access another customer's information.

---

## 5. Main User Flow

### Overall Entry Flow

```text
Open Website
     |
     v
Landing Page
     |
     v
Sign Up / Login
     |
     v
Authentication
     |
     v
Identify User Role
     |
     +-------------------+
     |         |         |
     v         v         v
   Admin     Staff    Customer
     |         |         |
     v         v         v
  Admin     Staff    Customer
Dashboard  Dashboard   Portal
