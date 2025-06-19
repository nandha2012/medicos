# services/external_api_service.py

import requests

class ExternalAPIService:
    def __init__(self, base_url, headers=None):
        self.base_url = base_url
        self.headers = headers or {}

    def get(self, endpoint, params=None):
        url = f"{self.base_url}/{endpoint}"
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"GET request failed: {e}")
            return None

    def post(self, endpoint, data=None, json=None):
        url = f"{self.base_url}/{endpoint}"
        try:
            response = requests.post(url, headers=self.headers, data=data, json=json)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"POST request failed: {e}")
            return None

    def put(self, endpoint, data=None):
        url = f"{self.base_url}/{endpoint}"
        try:
            response = requests.put(url, headers=self.headers, data=data)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"PUT request failed: {e}")
            return None

    def delete(self, endpoint):
        url = f"{self.base_url}/{endpoint}"
        try:
            response = requests.delete(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"DELETE request failed: {e}")
            return None
