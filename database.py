
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from config import settings

DATABASE_URL = settings.DATABASE_URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Enterprise(Base):
    __tablename__ = "enterprises"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)  # Добавляем поле name
    description = Column(Text, nullable=False)
    waste_description = Column(Text, nullable=False)
    role = Column(String(50), nullable=False)
    contact = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)

class QueryHistory(Base):
    __tablename__ = "query_history"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    query_text = Column(Text)
    role = Column(String(50))
    response = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

# Создаем таблицы
try:
    Base.metadata.create_all(bind=engine)
    print("✅ Таблицы успешно созданы в MySQL")
except Exception as e:
    print(f"❌ Ошибка при создании таблиц: {e}")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()