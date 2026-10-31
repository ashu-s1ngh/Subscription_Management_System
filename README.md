# Brightloop API

FastAPI business-logic service for the Brightloop subscription MVP.

## Run locally

```powershell
C:/Users/Ashu/AppData/Local/Programs/Python/Python313/python.exe -m pip install -r requirements.txt
C:/Users/Ashu/AppData/Local/Programs/Python/Python313/python.exe -m uvicorn app.main:app --reload
```

Open `/docs` for the interactive API. The temporary store seeds one product and plan at startup. Send `X-Role: admin` or `X-Role: staff` while the Supabase Auth integration is being wired; the `require_role` dependency is the replacement point for JWT/Supabase claims.

## MVP endpoints

- `POST/GET /api/v1/products`, `/plans`, `/customers`, `/discounts`
- `POST/GET /api/v1/subscriptions`
- `PATCH /api/v1/subscriptions/{id}/status`
- `POST /api/v1/subscriptions/{id}/invoice`
- `GET /api/v1/invoices`
- `POST /api/v1/payments`
- `GET /api/v1/analytics`
