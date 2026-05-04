import requests
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from admin_app.models import admin_dashboard_models

class PathaoCourier:
    def __init__(self):
        try:
            courier = admin_dashboard_models.PathaoCourier.objects.get(provider='pathao', status=True)
            self.base_url = courier.base_url.rstrip("/")
            self.client_id = courier.api_key
            self.client_secret = courier.secret_key
            self.username = courier.username
            self.password = courier.password
            self.store_id = courier.store_id
            self.city_id = courier.city_id
            self.zone_id = courier.zone_id
            self.area_id = courier.area_id

        except ObjectDoesNotExist:
            raise Exception("No Pathao courier credentials found. Please add them via Django Admin → Couriers.")
 
        self.headers = self._build_headers()

 
    def _get_access_token(self):
        url = f"{self.base_url}/aladdin/api/v1/issue-token"
        payload = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "username": self.username,
            "password": self.password,
            "grant_type": "password",
        }
        response = requests.post(url, json=payload, timeout=15)
        data     = response.json()
        token    = data.get("access_token")
        if not token:
            raise Exception(f"Pathao authentication failed: {data}")

        return token
 
    def _build_headers(self):
        token = self._get_access_token()
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type":  "application/json",
        }
 
    def place_order(self, merchant_order_id, recipient_name, recipient_phone, recipient_address, cod_amount, item_description=""):
        url = f"{self.base_url}/aladdin/api/v1/orders"

        payload = {
            "store_id": self.store_id,
            "merchant_order_id": merchant_order_id,
            "recipient_name": recipient_name,
            "recipient_phone": recipient_phone,
            "recipient_address": recipient_address,

            "delivery_type": 48,
            "item_type": 2,
            "item_quantity": 1,
            "item_weight": 0.5,
            "amount_to_collect": float(cod_amount),
            "item_description": item_description[:200],
        }

        response = requests.post(url, json=payload, headers=self.headers)
        return response.json()
 
    def check_status_by_consignment_id(self, consignment_id):
        url = f"{self.base_url}/aladdin/api/v1/orders/{consignment_id}"
        response = requests.get(url, headers=self.headers, timeout=15)
        return response.json()
 
    def get_stores(self):
        url = f"{self.base_url}/aladdin/api/v1/stores"
        response = requests.get(url, headers=self.headers, timeout=15)
        return response.json()
 
    def get_cities(self):
        url = f"{self.base_url}/aladdin/api/v1/cities"
        response = requests.get(url, headers=self.headers, timeout=15)
        return response.json()
 
    def get_zones(self, city_id):
        url = f"{self.base_url}/aladdin/api/v1/cities/{city_id}/zone-list"
        response = requests.get(url, headers=self.headers, timeout=15)
        return response.json()
 
    def get_balance(self):
        url = f"{self.base_url}/aladdin/api/v1/merchant/payment-accounts"
        response = requests.get(url, headers=self.headers, timeout=15)
        return response.json()