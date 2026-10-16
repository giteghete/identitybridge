import requests

DOMAIN = "dev-obxdm8meqyvei8we.us.auth0.com"
LIVE_TOKEN = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik9IVTJYblJKbm9HbjFRYk5KYm5NQyJ9.eyJpc3MiOiJodHRwczovL2Rldi1vYnhkbThtZXF5dmVpOHdlLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiIwQ3ZQVk9zVER3alVsMGdIUkZ3OUNBWGpjZVVBZUl1eEBjbGllbnRzIiwiYXVkIjoiaHR0cHM6Ly9kZXYtb2J4ZG04bWVxeXZlaTh3ZS51cy5hdXRoMC5jb20vYXBpL3YyLyIsImlhdCI6MTc5MjEyNDIxNiwiZXhwIjoxNzkyMjEwNjE2LCJzY29wZSI6InJlYWQ6dXNlcnMgdXBkYXRlOnVzZXJzIGRlbGV0ZTp1c2VycyBjcmVhdGU6dXNlcnMiLCJndHkiOiJjbGllbnQtY3JlZGVudGlhbHMiLCJhenAiOiIwQ3ZQVk9zVER3alVsMGdIUkZ3OUNBWGpjZVVBZUl1eCJ9.G8s3Ec--KP58agBU5j-zNzd3NQGWpsB38zsiMMOvnaAaTKcH8fOhB15kjsY70NTKdmnQ3bOM1C9kYDfZ6YOYi_6iLD9Giu2RghXqbiLT-ftxX2K4obKM33tcVklx3xJgAFH7EClLloQFAkuH7F_izcyQMP2j6yXGABGS9yj1xcUHhlGN8DpG3JTDvbOCPlMBDyu5XXAc_cqFssmUuZGE5uY-b_rXS3_tgBK8_CzXLNgUz30kmT_n_GzdqbhhHnsX8N0P9dxKoQz4g_jV7Thdrr1y2uvDdJx5SJx9GsR40bTSR9OKrbA4zeuA25Stz-C4dneqBC36UWE0orH9gvLwZw" # Use your same management token
TOKEN_TYPE = "Bearer"

# We target Jane Doe by encoding her unique account string into the API path
# In Auth0, standard database users are prefixed with 'auth0|'
TARGET_USER_ID = "auth0|jane_doe_iga_example_com" 

print("🎬 INITIALIZING LIFECYCLE TERMINATION ENGINE...")

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
