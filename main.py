from fastapi import FastAPI
from pydantic import BaseModel
import re

app = FastAPI()

class PasswordRequest(BaseModel):
    password: str

def validate_password(pwd: str):
    issues = []
    if len(pwd) < 8:
        issues.append("A jelszónak legalább 8 karakter hosszúnak kell lennie.")
    if not re.search(r'[a-z]', pwd):
        issues.append("Kisbetűt kell tartalmaznia.")
    if not re.search(r'[A-Z]', pwd):
        issues.append("Nagybetűt kell tartalmaznia.")
    if not re.search(r'\d', pwd):
        issues.append("Számot kell tartalmaznia.")
    if not re.search(r'[!@#$%^&*()_\-+=\[\]{};:\'",.<>?/\\|]', pwd):
        issues.append("Speciális karaktert kell tartalmaznia (!@#$...).")
    return issues

@app.post("/check_password")
def check_password(req: PasswordRequest):
    issues = validate_password(req.password)
    if not issues:
        return {"valid": True, "message": "A jelszó érvényes."}
    else:
        return {"valid": False, "message": "A jelszó érvénytelen.", "errors": issues}