import requests
from django.core.exceptions import ObjectDoesNotExist
from admin_app.models import admin_dashboard_models


class RedXCourier:
    def __init__(self):
        try:
            courier = admin_dashboard_models.PathaoCourier.objects.get(provider='redx', status=True)
            self.base_url = courier.base_url.rstrip("/")
            self.api_key = courier.api_key
            self.store_id = courier.store_id
            self.area_id = courier.area_id
        except ObjectDoesNotExist:
            raise Exception("No RedX courier credentials found. Please add them via Django Admin → Couriers.")

        self.headers = self._build_headers()

    def _build_headers(self):
        return {
            "API-ACCESS-TOKEN": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    # ── Parcel ────────────────────────────────────────────────────────────────

    def place_order(
        self,
        merchant_order_id,
        recipient_name,
        recipient_phone,
        recipient_address,
        delivery_area,
        delivery_area_id,
        cod_amount,
        value,
        parcel_weight=500,
        item_description="",
        pickup_store_id=None,
        parcel_details=None,
        is_closed_box=False,
    ):
        """
        Create a new parcel.
        parcel_details: list of dicts [{"name": ..., "category": ..., "value": ...}]
        parcel_weight : grams (default 500 g)
        """
        url = f"{self.base_url}/parcel"
        payload = {
            "customer_name": recipient_name,
            "customer_phone": recipient_phone,
            "delivery_area": delivery_area,
            "delivery_area_id": delivery_area_id,
            "customer_address": recipient_address,
            "merchant_invoice_id": merchant_order_id,
            "cash_collection_amount": str(cod_amount),
            "parcel_weight": str(parcel_weight),
            "instruction": item_description[:200],
            "value": value,
            "is_closed_box": str(is_closed_box).lower(),
        }
        if pickup_store_id:
            payload["pickup_store_id"] = pickup_store_id
        if parcel_details:
            payload["parcel_details_json"] = parcel_details

        response = requests.post(url, json=payload, headers=self.headers, timeout=15)
        return response.json()   # {"tracking_id": "..."}

    def get_parcel_details(self, tracking_id):
        """GET /parcel/info/<tracking_id>"""
        url = f"{self.base_url}/parcel/info/{tracking_id}"
        response = requests.get(url, headers=self.headers, timeout=15)
        return response.json()

    def track_parcel(self, tracking_id):
        """GET /parcel/track/<tracking_id> — returns timeline of status events."""
        url = f"{self.base_url}/parcel/track/{tracking_id}"
        response = requests.get(url, headers=self.headers, timeout=15)
        return response.json()

    def cancel_parcel(self, tracking_id, reason=""):
        """
        PATCH /parcels — cancel a parcel by setting status → cancelled.
        """
        url = f"{self.base_url}/parcels"
        payload = {
            "entity_type": "parcel-tracking-id",
            "entity_id": tracking_id,
            "update_details": {
                "property_name": "status",
                "new_value": "cancelled",
                "reason": reason,
            },
        }
        response = requests.patch(url, json=payload, headers=self.headers, timeout=15)
        return response.json()   # {"success": True, "message": "Request Accepted"}

    def update_parcel(self, tracking_id, property_name, new_value, reason=""):
        """
        Generic PATCH /parcels — update any parcel property (address, status, etc.).
        """
        url = f"{self.base_url}/parcels"
        payload = {
            "entity_type": "parcel-tracking-id",
            "entity_id": tracking_id,
            "update_details": {
                "property_name": property_name,
                "new_value": new_value,
                "reason": reason,
            },
        }
        response = requests.patch(url, json=payload, headers=self.headers, timeout=15)
        return response.json()

    # ── Areas ─────────────────────────────────────────────────────────────────

    def get_areas(self):
        """GET /areas — all delivery areas."""
        url = f"{self.base_url}/areas"
        response = requests.get(url, headers=self.headers, timeout=15)
        return response.json()

    def get_areas_by_postcode(self, post_code):
        """GET /areas?post_code=<post_code>"""
        url = f"{self.base_url}/areas"
        response = requests.get(url, headers=self.headers, params={"post_code": post_code}, timeout=15)
        return response.json()

    def get_areas_by_district(self, district_name):
        """GET /areas?district_name=<district_name>"""
        url = f"{self.base_url}/areas"
        response = requests.get(url, headers=self.headers, params={"district_name": district_name}, timeout=15)
        return response.json()

    # ── Pickup Stores ─────────────────────────────────────────────────────────

    def create_pickup_store(self, name, phone, address, area_id):
        """POST /pickup/store"""
        url = f"{self.base_url}/pickup/store"
        payload = {"name": name, "phone": phone, "address": address, "area_id": area_id}
        response = requests.post(url, json=payload, headers=self.headers, timeout=15)
        return response.json()

    def get_pickup_stores(self):
        """GET /pickup/stores"""
        url = f"{self.base_url}/pickup/stores"
        response = requests.get(url, headers=self.headers, timeout=15)
        return response.json()

    def get_pickup_store_details(self, pickup_store_id):
        """GET /pickup/store/info/<pickup_store_id>"""
        url = f"{self.base_url}/pickup/store/info/{pickup_store_id}"
        response = requests.get(url, headers=self.headers, timeout=15)
        return response.json()

    # ── Charge Calculator ─────────────────────────────────────────────────────

    def calculate_charge(self, delivery_area_id, pickup_area_id, cash_collection_amount, weight):
        """
        GET /charge/charge_calculator
        weight: grams
        Returns {"deliveryCharge": 60, "codCharge": 0}
        """
        url = f"{self.base_url}/charge/charge_calculator"
        params = {
            "delivery_area_id": delivery_area_id,
            "pickup_area_id": pickup_area_id,
            "cash_collection_amount": cash_collection_amount,
            "weight": weight,
        }
        response = requests.get(url, headers=self.headers, params=params, timeout=15)
        return response.json()