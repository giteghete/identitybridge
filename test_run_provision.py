
import requests

# Production Configuration Variables
DOMAIN = "://auth0.com" 

# NOTE: In production, these should be loaded securely from environment variables (.env)
# hardcoding values here is strictly for local sandbox validation loops.
LIVE_TOKEN = "PLACEHOLDER_REPLACE_WITH_YOUR_VERIFIED_MANAGEMENT_TOKEN"
CLIENT_ID = "PLACEHOLDER_REPLACE_WITH_YOUR_CLIENT_ID"
CLIENT_SECRET = "PLACEHOLDER_REPLACE_WITH_YOUR_CLIENT_SECRET"

# We target Jane Doe by encoding her unique account string into the API path
# In Auth0, standard database users are prefixed with 'auth0|'
TARGET_USER_ID = "auth0|jane_doe_iga_example_com" 

try:
    # 1. Point to our identity creation directory
    user_url = f"https://{DOMAIN}/api/v2/users"
    headers = {
        "Authorization": f"{TOKEN_TYPE} {LIVE_TOKEN}",
        "Content-Type": "application/json"
    }
    
    # 2. Build a standard enterprise Joiner payload with metadata
    joiner_payload = {
        "email": "jane.doe.iga@example.com",
        "user_metadata": {
            "first_name": "Jane",
            "last_name": "Doe",
            "department": "Engineering",
            "lifecycle_state": "Joiner-Active"
        },
        "connection": "Username-Password-Authentication", # Default core directory
        "password": "SecurePassword123!", # Required password string
        "email_verified": True
    }
    
    print("🚀 Triggering Joiner Provisioning Event for Jane Doe...")
    response = requests.post(user_url, json=joiner_payload, headers=headers)
    
    if response.status_code == 201:
        print("\n🏆 SUCCESS! User record created programmatically.")
        print(f"🆔 Generated Cloud ID: {response.json().get('user_id')}")
        print("--------------------------------------------------")
    else:
        print(f"\n❌ Provisioning Failed! HTTP Status: {response.status_code}")
        print(response.text)

except Exception as e:
    print(f"💥 Runtime Error: {e}")

