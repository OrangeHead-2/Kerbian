from fastapi import Depends, HTTPException

def require_role(required_roles):
    def decorator(user=Depends(verify_token)):
        if user["role"] not in required_roles:
            raise HTTPException(status_code=403, detail="Forbidden")
        return user
    return decorator