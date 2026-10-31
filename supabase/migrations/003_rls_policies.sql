-- 003_rls_policies.sql
-- Row Level Security (RLS) Policies

ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.customers ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.products ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.plans ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.subscriptions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.subscription_items ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.invoices ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.invoice_items ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.discounts ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.payments ENABLE ROW LEVEL SECURITY;

-- Helper function to get current user role
CREATE OR REPLACE FUNCTION public.get_current_role()
RETURNS TEXT AS $$
    SELECT role FROM public.profiles WHERE id = auth.uid();
$$ LANGUAGE sql STABLE SECURITY DEFINER;

-- 1. Profiles Policy
CREATE POLICY "Users can read their own profile"
    ON public.profiles FOR SELECT
    USING (id = auth.uid() OR public.get_current_role() IN ('admin', 'staff'));

CREATE POLICY "Admin can manage all profiles"
    ON public.profiles FOR ALL
    USING (public.get_current_role() = 'admin');

-- 2. Products & Plans (Public/Authenticated read, Admin write)
CREATE POLICY "Anyone authenticated can view active products"
    ON public.products FOR SELECT
    TO authenticated
    USING (true);

CREATE POLICY "Admin can manage products"
    ON public.products FOR ALL
    USING (public.get_current_role() = 'admin');

CREATE POLICY "Anyone authenticated can view plans"
    ON public.plans FOR SELECT
    TO authenticated
    USING (true);

CREATE POLICY "Admin can manage plans"
    ON public.plans FOR ALL
    USING (public.get_current_role() = 'admin');

-- 3. Customers Policy
CREATE POLICY "Customers view own record"
    ON public.customers FOR SELECT
    USING (profile_id = auth.uid() OR public.get_current_role() IN ('admin', 'staff'));

CREATE POLICY "Staff and Admin manage customers"
    ON public.customers FOR ALL
    USING (public.get_current_role() IN ('admin', 'staff'));

-- 4. Subscriptions Policy
CREATE POLICY "Customer view own subscriptions"
    ON public.subscriptions FOR SELECT
    USING (
        customer_id IN (SELECT id FROM public.customers WHERE profile_id = auth.uid())
        OR public.get_current_role() IN ('admin', 'staff')
    );

CREATE POLICY "Staff and Admin manage subscriptions"
    ON public.subscriptions FOR ALL
    USING (public.get_current_role() IN ('admin', 'staff'));

-- 5. Invoices Policy
CREATE POLICY "Customer view own invoices"
    ON public.invoices FOR SELECT
    USING (
        customer_id IN (SELECT id FROM public.customers WHERE profile_id = auth.uid())
        OR public.get_current_role() IN ('admin', 'staff')
    );

CREATE POLICY "Staff and Admin manage invoices"
    ON public.invoices FOR ALL
    USING (public.get_current_role() IN ('admin', 'staff'));

-- 6. Payments Policy
CREATE POLICY "Customer view payments for their invoices"
    ON public.payments FOR SELECT
    USING (
        invoice_id IN (
            SELECT id FROM public.invoices 
            WHERE customer_id IN (SELECT id FROM public.customers WHERE profile_id = auth.uid())
        )
        OR public.get_current_role() IN ('admin', 'staff')
    );

CREATE POLICY "Staff and Admin record payments"
    ON public.payments FOR ALL
    USING (public.get_current_role() IN ('admin', 'staff'));
