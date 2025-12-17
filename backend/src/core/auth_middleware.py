from fastapi import Request, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from backend.src.services.neon_db import get_db
from backend.src.models.auth_models import Session as DbSession, User

async def get_current_user(request: Request, db: Session = Depends(get_db)):
    # 1. Get session token from cookie
    session_token = request.cookies.get("better-auth.session_token")
    
    if not session_token:
        # Check Authorization header as fallback (Bearer token)
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            session_token = auth_header.split(" ")[1]
            
    if not session_token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    # 2. Verify session in DB
    # Query: SELECT * FROM session WHERE token = :token AND expiresAt > NOW()
    session_record = db.query(DbSession).filter(
        DbSession.token == session_token,
        DbSession.expiresAt > datetime.utcnow()
    ).first()

    if not session_record:
        raise HTTPException(status_code=401, detail="Invalid or expired session")

    # 3. Get User
    user = db.query(User).filter(User.id == session_record.userId).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user
