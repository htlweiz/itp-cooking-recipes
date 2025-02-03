from fastapi_msal import MSALAuthorization, MSALClientConfig
import dotenv
import os

client_config: MSALClientConfig = MSALClientConfig()

dotenv.load_dotenv()

client_config.client_id = os.getenv("CLIENT_ID")
client_config.client_credential = os.getenv("CLIENT_SECRET")
client_config.tenant = os.getenv("TENANT_ID")

msal_auth = MSALAuthorization(client_config=client_config)
