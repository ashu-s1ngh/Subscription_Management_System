# Brightloop API

FastAPI business-logic service for the Brightloop subscription MVP.

## Run locally

```bash
python -m venv .venv

# macOS/Linux
source .venv/bin/activate

# Windows PowerShell
# .venv\Scripts\Activate.ps1

python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`; interactive documentation is at `http://127.0.0.1:8000/docs`. The temporary store seeds one product and plan at startup. Send `X-Role: admin` or `X-Role: staff` while the Supabase Auth integration is being wired; the `require_role` dependency is the replacement point for JWT/Supabase claims.

## MVP endpoints

- `POST/GET /api/v1/products`, `/plans`, `/customers`, `/discounts`
- `POST/GET /api/v1/subscriptions`
- `PATCH /api/v1/subscriptions/{id}/status`
- `POST /api/v1/subscriptions/{id}/invoice`
- `GET /api/v1/invoices`
- `POST /api/v1/payments`
- `GET /api/v1/analytics`
