import firebase_admin
from firebase_admin import credentials, auth
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

app = FastAPI()

# 1. Initialize Firebase (Do this ONLY once)
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

# 2. Define the Reusable Security Dependency
security = HTTPBearer()

def verify_token(res: HTTPAuthorizationCredentials = Depends(security)):
    try:
        decoded_token = auth.verify_id_token(res.credentials)
        return decoded_token
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired Firebase token",
        )

# 3. Define your Routes
@app.get("/profile")
def get_profile(user = Depends(verify_token)):
    return {"status": "success", "uid": user['uid'], "email": user.get('email')}

@app.get("/secure-data")
async def get_secure_data(user = Depends(verify_token)):
    return {"message": f"Hello {user['uid']}, this is secure data!"}