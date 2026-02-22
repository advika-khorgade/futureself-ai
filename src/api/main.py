"""FastAPI REST API for FutureSelf AI."""
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime, timedelta
from jose import JWTError, jwt
import os
from dotenv import load_dotenv

from ..auth import AuthManager
from ..workflow import DecisionWorkflowRunner
from ..schemas import DecisionInput
from ..history import HistoryManager

load_dotenv()

# JWT Configuration
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Initialize FastAPI
app = FastAPI(
    title="FutureSelf AI API",
    description="Multi-agent decision intelligence platform API",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Pydantic Models
class UserRegister(BaseModel):
    username: str = Field(..., min_length=3)
    email: str
    password: str = Field(..., min_length=8)

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: int
    username: str

class DecisionAnalyzeRequest(BaseModel):
    decision: str = Field(..., min_length=10)
    context: Optional[str] = None
    timeframe: Optional[str] = None
    tags: Optional[List[str]] = []

class DecisionResponse(BaseModel):
    id: int
    decision_text: str
    recommendation: str
    confidence_level: float
    risk_score: float
    opportunity_score: float
    tags: List[str]
    created_at: datetime
    full_analysis: Optional[dict] = None

# Helper Functions
def create_access_token(data: dict):
    """Create JWT access token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify JWT token and return user_id."""
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials"
            )
        return user_id
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )

# API Endpoints

@app.get("/")
async def root():
    """API root endpoint."""
    return {
        "message": "FutureSelf AI API",
        "version": "1.0.0",
        "docs": "/api/docs"
    }

@app.post("/api/v1/auth/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register(user: UserRegister):
    """Register a new user."""
    success, message = AuthManager.register_user(
        user.username,
        user.email,
        user.password
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message
        )
    
    # Auto-login after registration
    success, message, user_data = AuthManager.login_user(user.username, user.password)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration successful but login failed"
        )
    
    access_token = create_access_token({"user_id": user_data["id"]})
    
    return Token(
        access_token=access_token,
        user_id=user_data["id"],
        username=user_data["username"]
    )

@app.post("/api/v1/auth/login", response_model=Token)
async def login(user: UserLogin):
    """Login user and return JWT token."""
    success, message, user_data = AuthManager.login_user(user.username, user.password)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=message
        )
    
    access_token = create_access_token({"user_id": user_data["id"]})
    
    return Token(
        access_token=access_token,
        user_id=user_data["id"],
        username=user_data["username"]
    )

@app.post("/api/v1/decisions/analyze", status_code=status.HTTP_201_CREATED)
async def analyze_decision(
    request: DecisionAnalyzeRequest,
    user_id: int = Depends(verify_token)
):
    """Analyze a decision using multi-agent AI system."""
    try:
        # Create decision input
        decision_input = DecisionInput(
            decision=request.decision,
            context=request.context,
            timeframe=request.timeframe
        )
        
        # Run analysis
        runner = DecisionWorkflowRunner()
        result = runner.run(decision_input)
        
        if result.error:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Analysis failed: {result.error}"
            )
        
        # Save to history
        decision_id = HistoryManager.save_decision(user_id, result, request.tags)
        
        # Return response
        return {
            "id": decision_id,
            "decision": request.decision,
            "recommendation": result.recommendation.recommendation,
            "confidence_level": result.recommendation.confidence_level,
            "risk_score": result.recommendation.overall_risk_score,
            "opportunity_score": result.recommendation.overall_opportunity_score,
            "key_insights": result.recommendation.key_insights,
            "risk_reward_balance": result.recommendation.risk_reward_balance,
            "next_steps": [
                {
                    "action": step.action,
                    "priority": step.priority,
                    "timeframe": step.timeframe
                }
                for step in result.recommendation.next_steps
            ]
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@app.get("/api/v1/decisions/history")
async def get_history(
    limit: int = 50,
    search: Optional[str] = None,
    user_id: int = Depends(verify_token)
):
    """Get user's decision history."""
    try:
        if search:
            decisions = HistoryManager.search_decisions(user_id, search)
        else:
            decisions = HistoryManager.get_user_history(user_id, limit=limit)
        
        # Convert to dict format
        result = []
        for d in decisions:
            if hasattr(d, 'id'):  # Object format
                result.append({
                    "id": d.id,
                    "decision_text": d.decision_text,
                    "recommendation": d.recommendation,
                    "risk_score": d.risk_score,
                    "opportunity_score": d.opportunity_score,
                    "confidence_level": d.confidence_level,
                    "tags": d.tags.split(',') if d.tags else [],
                    "created_at": d.created_at.isoformat()
                })
            else:  # Dict format
                result.append({
                    "id": d['id'],
                    "decision_text": d['decision_text'],
                    "recommendation": d['recommendation'],
                    "risk_score": d['risk_score'],
                    "opportunity_score": d['opportunity_score'],
                    "confidence_level": d['confidence_level'],
                    "tags": d['tags'],
                    "created_at": d['created_at'].isoformat()
                })
        
        return {"decisions": result, "count": len(result)}
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@app.get("/api/v1/decisions/{decision_id}")
async def get_decision(
    decision_id: int,
    user_id: int = Depends(verify_token)
):
    """Get a specific decision by ID."""
    try:
        decision = HistoryManager.get_decision_by_id(decision_id)
        
        if not decision:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Decision not found"
            )
        
        return decision
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@app.delete("/api/v1/decisions/{decision_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_decision(
    decision_id: int,
    user_id: int = Depends(verify_token)
):
    """Delete a decision."""
    try:
        success = HistoryManager.delete_decision(decision_id, user_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Decision not found or unauthorized"
            )
        
        return None
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@app.get("/api/v1/analytics/summary")
async def get_analytics_summary(user_id: int = Depends(verify_token)):
    """Get analytics summary for user."""
    try:
        decisions = HistoryManager.get_user_history(user_id, limit=1000)
        
        if not decisions:
            return {
                "total_decisions": 0,
                "avg_risk_score": 0,
                "avg_opportunity_score": 0,
                "avg_confidence": 0
            }
        
        # Calculate statistics
        total = len(decisions)
        risk_scores = [d.get('risk_score') or d.risk_score for d in decisions if (d.get('risk_score') if isinstance(d, dict) else d.risk_score)]
        opp_scores = [d.get('opportunity_score') or d.opportunity_score for d in decisions if (d.get('opportunity_score') if isinstance(d, dict) else d.opportunity_score)]
        conf_levels = [d.get('confidence_level') or d.confidence_level for d in decisions if (d.get('confidence_level') if isinstance(d, dict) else d.confidence_level)]
        
        return {
            "total_decisions": total,
            "avg_risk_score": sum(risk_scores) / len(risk_scores) if risk_scores else 0,
            "avg_opportunity_score": sum(opp_scores) / len(opp_scores) if opp_scores else 0,
            "avg_confidence": sum(conf_levels) / len(conf_levels) if conf_levels else 0
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@app.get("/api/v1/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
