import requests
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from admin_app.models import admin_dashboard_models

class SteadfastCourier:
    def __init__(self):
        try:
            courier = admin_dashboard_models.Courier.objects.get(status=True)
            self.base_url = courier.base_url
            self.headers = {
                "Api-Key": courier.api_key,
                "Secret-Key": courier.secret_key,
                "Content-Type": "application/json",
            }
        except ObjectDoesNotExist:
            raise Exception("No courier credentials found. Please add API credentials.")

    def place_order(self, invoice, recipient_name, recipient_phone, recipient_address, cod_amount, note=""):
        url = f"{self.base_url}/create_order"
        payload = {
            "invoice": invoice,
            "recipient_name": recipient_name,
            "recipient_phone": recipient_phone,
            "recipient_address": recipient_address,
            "cod_amount": float(cod_amount),
            "note": note,
        }
        response = requests.post(url, json=payload, headers=self.headers)
        return response.json()
    
    def check_status_by_consignment_id(self, consignment_id):
        url = f"{self.base_url}/status_by_cid/{consignment_id}"
        response = requests.get(url, headers=self.headers)
        return response.json()
    
    def check_status_by_invoice(self, invoice):
        url = f"{self.base_url}/status_by_invoice/{invoice}"
        response = requests.get(url, headers=self.headers)
        return response.json()
    
    def get_balance(self):
        url = f"{self.base_url}/get_balance"
        response = requests.get(url, headers=self.headers)
        return response.json()