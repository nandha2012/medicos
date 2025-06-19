from services.external_api_service import ExternalAPIService
from dotenv import load_dotenv
import os
load_dotenv()

# Shared API instance (customize base URL and headers here)
api = ExternalAPIService(
    base_url=os.getenv("EXTERNAL_API_END_POINT"),
    headers={"Content-Type": "application/json"}
)
