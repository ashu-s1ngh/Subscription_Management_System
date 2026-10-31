-- Demo Seed Data for Brightloop
-- Products
INSERT INTO public.products (id, name, type, sales_price, cost_price, description, variants)
VALUES
    ('a0000000-0000-0000-0000-000000000001', 'Business Management Software', 'software', 999.00, 300.00, 'Cloud-based complete ERP and management suite.', 
     '[{"name": "Standard", "price_adjustment": 0}, {"name": "Odoo Integration", "price_adjustment": 560}]'::jsonb),
    ('a0000000-0000-0000-0000-000000000002', 'Cloud Analytics Pro', 'service', 499.00, 150.00, 'Real-time financial analytics dashboard.',
     '[{"name": "Basic", "price_adjustment": 0}, {"name": "Enterprise", "price_adjustment": 400}]'::jsonb)
ON CONFLICT (id) DO NOTHING;

-- Plans
INSERT INTO public.plans (id, product_id, name, price, billing_cycle, min_quantity, allow_pause)
VALUES
    ('b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'Monthly Starter', 999.00, 'monthly', 1, true),
    ('b0000000-0000-0000-0000-000000000002', 'a0000000-0000-0000-0000-000000000001', 'Annual Growth', 9990.00, 'yearly', 1, true),
    ('b0000000-0000-0000-0000-000000000003', 'a0000000-0000-0000-0000-000000000002', 'Analytics Monthly', 499.00, 'monthly', 1, true)
ON CONFLICT (id) DO NOTHING;
