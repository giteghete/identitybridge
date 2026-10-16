
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
    headers = {
        "Authorization": f"{TOKEN_TYPE} {LIVE_TOKEN}",
        "Content-Type": "application/json"
    }
    
    # 1. Dynamically locate the user's active cloud record
    search_url = f"https://{DOMAIN}/api/v2/users"
    params = {"q": 'email:"jane.doe.iga@example.com"', "search_engine": "v3"}
    
    print("🔍 Fetching active profile for jane.doe.iga@example.com...")
    user_search = requests.get(search_url, headers=headers, params=params).json()
    
    if user_search and len(user_search) > 0:
        user_record = user_search[0]
        cloud_id = user_record["user_id"]
        
        # Pull current metadata to detect the delta (the change)
        old_metadata = user_record.get("user_metadata", {})
        old_dept = old_metadata.get("department", "Unknown")
        old_state = old_metadata.get("lifecycle_state", "Unknown")
        
        print(f"🎯 Target Located. Current Department: {old_dept} | State: {old_state}")
        
        # 2. Define the lifecycle change (Simulating a Mover event to Sales)
        new_dept = "Sales"
        new_state = "Mover-Promoted"
        
        # Verification check: If the user is already in Sales, skip to prevent redundant API thrashing
        if old_dept == new_dept:
            print(f"ℹ️ User is already assigned to {new_dept}. No lifecycle change required.")
        else:
            print(f"🔄 Change Detected! Shifting department from [{old_dept}] ➡️ [{new_dept}]...")
            
            # 3. Fire a PATCH request to dynamically update the user record
            update_url = f"https://{DOMAIN}/api/v2/users/{cloud_id}"
            mover_payload = {
                "user_metadata": {
                    "department": new_dept,
                    "lifecycle_state": new_state
                }
            }
            
            response = requests.patch(update_url, json=mover_payload, headers=headers)
            
            if response.status_code == 200:
                updated_user = response.json()
                resulting_metadata = updated_user.get("user_metadata", {})
                
                print("\n🏆 SUCCESS! Mover lifecycle update applied programmatically.")
                print(f"📋 Verified New Department: {resulting_metadata.get('department')}")
                print(f"📋 Verified Audit State: {resulting_metadata.get('lifecycle_state')}")
                print("--------------------------------------------------")
            else:
                print(f"\n❌ Mover Update Failed! HTTP Status: {response.status_code}")
                print(response.text)
    else:
        print("❌ Action Aborted: Could not find an active account for jane.doe.iga@example.com")

except Exception as e:
    print(f"💥 Runtime Error: {e}")
