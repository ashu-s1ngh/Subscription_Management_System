from __future__ import annotations

from datetime import date, datetime, timezone
from decimal import Decimal
from typing import Any, TypeVar
from uuid import UUID, uuid4

from .mvp_models import (
    Customer, Discount, Invoice, Payment, Plan, Product, Subscription,
)

T = TypeVar("T")


class NotFoundError(Exception):
    pass


class ConflictError(Exception):
    pass


class Store:
    """Temporary persistence adapter; replace collections with Supabase queries later."""

    def __init__(self) -> None:
        self.products: dict[UUID, Product] = {}
        self.plans: dict[UUID, Plan] = {}
        self.customers: dict[UUID, Customer] = {}
        self.discounts: dict[UUID, Discount] = {}
        self.subscriptions: dict[UUID, Subscription] = {}
        self.invoices: dict[UUID, Invoice] = {}
        self.payments: dict[UUID, Payment] = {}

    @staticmethod
    def timestamps() -> dict[str, Any]:
        now = datetime.now(timezone.utc)
        return {"id": uuid4(), "created_at": now, "updated_at": now}

    def get(self, collection: dict[UUID, T], item_id: UUID) -> T:
        try:
            return collection[item_id]
        except KeyError as exc:
            raise NotFoundError(f"Record {item_id} was not found") from exc

    @staticmethod
    def touch(item: T) -> T:
        if hasattr(item, "updated_at"):
            item.updated_at = datetime.now(timezone.utc)  # type: ignore[attr-defined]
        return item

    def seed(self) -> None:
        product = Product(**self.timestamps(), name="Brightloop Pro", description="All-in-one subscription plan")
        self.products[product.id] = product
        plan = Plan(**self.timestamps(), product_id=product.id, name="Pro Monthly", price=Decimal("49.00"), billing_interval="monthly")
        self.plans[plan.id] = plan


store = Store()
store.seed()


def today() -> date:
    return datetime.now(timezone.utc).date()

