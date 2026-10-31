# Brightloop Technical Architecture

Brightloop employs a 3-tier decoupled architecture:

## 1. Frontend: Next.js (App Router)
- **Role**: Responsive UI, role-based dashboards, interactive forms, and analytical charts.
- **Tech**: Next.js 14/15, TypeScript, Tailwind CSS, Lucide React, Recharts.
- **Routing**:
  - `(auth)`: Login, registration, password recovery.
  - `admin/*`: Admin dashboard and business management views.
  - `staff/*`: Daily operational views.
  - `portal/*`: Customer self-service portal.

## 2. Backend: Python FastAPI
- **Role**: High-performance domain logic, mathematical billing computations, state machines, and API security.
- **Engines**:
  - **Subscription Lifecycle**: `draft` -> `quotation` -> `confirmed` -> `active` -> `paused` / `closed`.
  - **Billing & Tax Engine**: Base price + variant pricing + discounts + taxes.
  - **Idempotent Invoicing**: Prevents double-billing within the same billing period.
  - **Reconciliation**: Partial and full balance tracking.
  - **Analytics Engine**: Real-time MRR, ARR, churn, and overdue tracking.

## 3. Database & Auth: Supabase (PostgreSQL)
- **PostgreSQL 15+**: 10 normalized core tables.
- **Supabase Auth**: JWT generation, bcrypt password hashing.
- **Row Level Security (RLS)**: Enforces database-level isolation between customers and staff/admin.
