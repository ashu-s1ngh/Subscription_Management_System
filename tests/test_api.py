from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health() -> None:
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_admin_can_create_customer_and_staff_cannot_create_product() -> None:
    customer = client.post("/api/v1/customers", headers={"X-Role": "staff"}, json={"name": "Ada Lovelace", "email": "ada@example.com"})
    assert customer.status_code == 201
    product = client.post("/api/v1/products", headers={"X-Role": "staff"}, json={"name": "Restricted"})
    assert product.status_code == 403


def test_subscription_invoice_and_payment_flow() -> None:
    customer = client.post("/api/v1/customers", headers={"X-Role": "admin"}, json={"name": "Grace Hopper", "email": "grace@example.com"}).json()
    plan = client.get("/api/v1/plans").json()[0]
    subscription = client.post("/api/v1/subscriptions", headers={"X-Role": "staff"}, json={"customer_id": customer["id"], "plan_id": plan["id"]})
    assert subscription.status_code == 201
    invoice = client.post(f"/api/v1/subscriptions/{subscription.json()['id']}/invoice", headers={"X-Role": "staff"}).json()
    payment = client.post("/api/v1/payments", headers={"X-Role": "staff"}, json={"invoice_id": invoice["id"], "amount": invoice["total"]})
    assert payment.status_code == 201
    assert client.get("/api/v1/invoices").json()[-1]["status"] == "paid"


def test_subscription_accepts_explicit_start_date() -> None:
    customer = client.post("/api/v1/customers", headers={"X-Role": "admin"}, json={"name": "Linus Torvalds", "email": "linus@example.com"}).json()
    plan = client.get("/api/v1/plans").json()[0]
    response = client.post("/api/v1/subscriptions", headers={"X-Role": "admin"}, json={"customer_id": customer["id"], "plan_id": plan["id"], "start_on": "2026-10-31"})
    assert response.status_code == 201
    assert response.json()["start_on"] == "2026-10-31"
