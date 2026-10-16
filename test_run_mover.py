import requests


DOMAIN = "dev-obxdm8meqyvei8we.us.auth0.com" 
LIVE_TOKEN = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik9IVTJYblJKbm9HbjFRYk5KYm5NQyJ9.eyJpc3MiOiJodHRwczovL2Rldi1vYnhkbThtZXF5dmVpOHdlLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiIwQ3ZQVk9zVER3alVsMGdIUkZ3OUNBWGpjZVVBZUl1eEBjbGllbnRzIiwiYXVkIjoiaHR0cHM6Ly9kZXYtb2J4ZG04bWVxeXZlaTh3ZS51cy5hdXRoMC5jb20vYXBpL3YyLyIsImlhdCI6MTc5MjEyNDIxNiwiZXhwIjoxNzkyMjEwNjE2LCJzY29wZSI6InJlYWQ6dXNlcnMgdXBkYXRlOnVzZXJzIGRlbGV0ZTp1c2VycyBjcmVhdGU6dXNlcnMiLCJndHkiOiJjbGllbnQtY3JlZGVudGlhbHMiLCJhenAiOiIwQ3ZQVk9zVER3alVsMGdIUkZ3OUNBWGpjZVVBZUl1eCJ9.G8s3Ec--KP58agBU5j-zNzd3NQGWpsB38zsiMMOvnaAaTKcH8fOhB15kjsY70NTKdmnQ3bOM1C9kYDfZ6YOYi_6iLD9Giu2RghXqbiLT-ftxX2K4obKM33tcVklx3xJgAFH7EClLloQFAkuH7F_izcyQMP2j6yXGABGS9yj1xcUHhlGN8DpG3JTDvbOCPlMBDyu5XXAc_cqFssmUuZGE5uY-b_rXS3_tgBK8_CzXLNgUz30kmT_n_GzdqbhhHnsX8N0P9dxKoQz4g_jV7Thdrr1y2uvDdJx5SJx9GsR40bTSR9OKrbA4zeuA25Stz-C4dneqBC36UWE0orH9gvLwZw" # Keep your same token here
TOKEN_TYPE = "Bearer"

print("🎬 INITIALIZING LIFECYCLE MOVER ENGINE...")

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
