
# [file name]: backend.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
import database as db
import enterprise_service as es

app = FastAPI(title="Circular Economy Bot API")

class EnterpriseRequest(BaseModel):
    description: str
    role: str  # "technologist" или "sales"

class RecommendationResponse(BaseModel):
    similar_enterprises: List[str]
    recommendation: str

@app.on_event("startup")
async def startup_event():
    """Инициализация при запуске"""
    es.initialize_sample_enterprises()

@app.post("/api/recommend", response_model=RecommendationResponse)
async def get_recommendations(
    request: EnterpriseRequest, 
    database: Session = Depends(db.get_db)
):
    # 1. Сохраняем запрос в SQL БД
    enterprise = db.Enterprise(
        name="Пользовательский запрос",  # Добавляем обязательное поле name
        description=request.description,
        waste_description=request.description,
        role=request.role,
        contact="не указан"
    )
    database.add(enterprise)
    database.commit()
    database.refresh(enterprise)
    
    # 2. Используем LLM для выбора наиболее подходящих предприятий из всей базы
    enhanced_results = es.enhance_search_results_with_llm(
        user_description=request.description,
        user_role=request.role
    )
    
    # 3. Сохраняем историю запроса
    history = db.QueryHistory(
        user_id=enterprise.id,
        query_text=request.description,
        role=request.role,
        response=enhanced_results["recommendation"]
    )
    database.add(history)
    database.commit()
    
    return RecommendationResponse(
        similar_enterprises=enhanced_results["similar_enterprises"],
        recommendation=enhanced_results["recommendation"]
    )

@app.get("/api/enterprises")
async def get_all_enterprises(database: Session = Depends(db.get_db)):
    """Получить все предприятия"""
    enterprises = database.query(db.Enterprise).all()
    return enterprises

@app.post("/api/enterprises")
async def add_enterprise(
    name: str,
    description: str,
    waste_description: str,
    role: str,
    contact: str,
    database: Session = Depends(db.get_db)
):
    """Ручное добавление предприятия"""
    
    enterprise = db.Enterprise(
        name=name,
        description=description,
        waste_description=waste_description,
        role=role,
        contact=contact
    )
    database.add(enterprise)
    database.commit()
    database.refresh(enterprise)
    
    return {"message": "Предприятие успешно добавлено", "enterprise_id": enterprise.id}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)