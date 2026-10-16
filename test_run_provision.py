import requests

DOMAIN = "dev-obxdm8meqyvei8we.us.auth0.com" 
LIVE_TOKEN = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik9IVTJYblJKbm9HbjFRYk5KYm5NQyJ9.eyJpc3MiOiJodHRwczovL2Rldi1vYnhkbThtZXF5dmVpOHdlLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiIwQ3ZQVk9zVER3alVsMGdIUkZ3OUNBWGpjZVVBZUl1eEBjbGllbnRzIiwiYXVkIjoiaHR0cHM6Ly9kZXYtb2J4ZG04bWVxeXZlaTh3ZS51cy5hdXRoMC5jb20vYXBpL3YyLyIsImlhdCI6MTc5MjEyNDIxNiwiZXhwIjoxNzkyMjEwNjE2LCJzY29wZSI6InJlYWQ6dXNlcnMgdXBkYXRlOnVzZXJzIGRlbGV0ZTp1c2VycyBjcmVhdGU6dXNlcnMiLCJndHkiOiJjbGllbnQtY3JlZGVudGlhbHMiLCJhenAiOiIwQ3ZQVk9zVER3alVsMGdIUkZ3OUNBWGpjZVVBZUl1eCJ9.G8s3Ec--KP58agBU5j-zNzd3NQGWpsB38zsiMMOvnaAaTKcH8fOhB15kjsY70NTKdmnQ3bOM1C9kYDfZ6YOYi_6iLD9Giu2RghXqbiLT-ftxX2K4obKM33tcVklx3xJgAFH7EClLloQFAkuH7F_izcyQMP2j6yXGABGS9yj1xcUHhlGN8DpG3JTDvbOCPlMBDyu5XXAc_cqFssmUuZGE5uY-b_rXS3_tgBK8_CzXLNgUz30kmT_n_GzdqbhhHnsX8N0P9dxKoQz4g_jV7Thdrr1y2uvDdJx5SJx9GsR40bTSR9OKrbA4zeuA25Stz-C4dneqBC36UWE0orH9gvLwZw" # Keep your same token here
TOKEN_TYPE = "Bearer"

print("🎬 INITIALIZING IDENTITY PROVISIONING ENGINE...")

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

