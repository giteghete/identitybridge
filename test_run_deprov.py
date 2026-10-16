
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
    # 1. Point to the specific user's endpoint path
    # To fix or change a user, the standard REST convention is a PATCH or PUT request
    url = f"https://{DOMAIN}/api/v2/users/{TARGET_USER_ID}"
    
    # Wait! Auth0 requires the actual internal User ID string or an encoded email.
    # Let's use the search endpoint to find her account dynamically instead!
    search_url = f"https://{DOMAIN}/api/v2/users"
    headers = {
        "Authorization": f"{TOKEN_TYPE} {LIVE_TOKEN}",
        "Content-Type": "application/json"
    }
    params = {"q": 'email:"jane.doe.iga@example.com"', "search_engine": "v3"}
    
    print("🔍 Searching for Jane Doe's cloud record...")
    user_search = requests.get(search_url, headers=headers, params=params).json()
    
    if user_search and len(user_search) > 0:
        cloud_id = user_search[0]["user_id"]
        print(f"🎯 Target Found! Internal Cloud ID is: {cloud_id}")
        
        # 2. Fire a PATCH request to block her login and update her lifecycle metadata
        update_url = f"https://{DOMAIN}/api/v2/users/{cloud_id}"
        
        leaver_payload = {
            "blocked": True, # This physically freezes the account and cuts off all login sessions instantly!
            "user_metadata": {
                "department": "Engineering",
                "lifecycle_state": "Leaver-Terminated" # Updating the IGA audit trail
            }
        }
        
        print("⛔ Triggering Leaver Event (Suspending account and blocking access)...")
        response = requests.patch(update_url, json=leaver_payload, headers=headers)
        
        if response.status_code == 200:
            print("\n🏆 SUCCESS! User record successfully deprovisioned.")
            print(f"🔒 Account Status: BLOCKED/SUSPENDED")
            print(f"📋 Audit State: {response.json().get('user_metadata', {}).get('lifecycle_state')}")
            print("--------------------------------------------------")
        else:
            print(f"\n❌ Leaver Event Failed! HTTP Status: {response.status_code}")
            print(response.text)
    else:
        print("❌ Could not find an active account for jane.doe.iga@example.com")

except Exception as e:
    print(f"💥 Runtime Error: {e}")
