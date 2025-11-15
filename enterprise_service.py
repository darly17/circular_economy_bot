
# [file name]: enterprise_service.py
from typing import List, Dict
from database import SessionLocal, Enterprise
from llm_client import select_enterprises_with_llm, generate_recommendation

def initialize_sample_enterprises():
    """Инициализирует базу данных предзаполненными предприятиями"""
    db = SessionLocal()
    try:
        # Проверяем, есть ли уже предприятия
        existing_count = db.query(Enterprise).count()
        if existing_count > 0:
            print(f"✅ В базе уже есть {existing_count} предприятий")
            return
        
        # Предзаполненные предприятия (с полем name)
        sample_enterprises = [
            {
                "name": "ОАО 'Белорусский металлургический завод'",
                "description": "Крупное металлургическое предприятие, производитель стального проката",
                "waste_description": "металлическая стружка, шлаки, огнеупорные материалы",
                "role": "sales",
                "contact": "bmz@mail.com"
            },
            {
                "name": "ОАО 'Минский тракторный завод'",
                "description": "Производитель сельскохозяйственной техники",
                "waste_description": "металлоотходы, пластик, упаковочные материалы",
                "role": "sales", 
                "contact": "mtz@sales.by"
            },
            {
                "name": "ОАО 'Гродно Азот'",
                "description": "Химическое предприятие, производство удобрений",
                "waste_description": "химические отходы, пластиковая тара, техническая вода",
                "role": "sales",
                "contact": "grodno_azot@chem.by"
            },
            {
                "name": "ЗАО 'Белвест'",
                "description": "Обувная фабрика, производство кожаной обуви",
                "waste_description": "кожаные обрезки, текстильные отходы, резина",
                "role": "sales",
                "contact": "belvest@shoes.by"
            },
            {
                "name": "ОАО 'Спартак'",
                "description": "Кондитерская фабрика",
                "waste_description": "пищевые отходы, упаковка, сахарная пудра",
                "role": "sales",
                "contact": "spartak@sweet.by"
            },
            {
                "name": "ИП 'ЭкоТех'",
                "description": "Переработчик вторичного сырья",
                "waste_description": "требуется металлолом, пластиковые отходы, макулатура",
                "role": "technologist",
                "contact": "ecotech@recycle.by"
            },
            {
                "name": "ООО 'Зеленая энергия'",
                "description": "Производитель биотоплива",
                "waste_description": "использует органические отходы, древесные отходы",
                "role": "technologist",
                "contact": "green_energy@bio.by"
            },
            {
                "name": "ИП 'АртКерамика'",
                "description": "Производство строительных материалов",
                "waste_description": "использует промышленные отходы, стеклобой",
                "role": "technologist",
                "contact": "art_ceramic@build.by"
            }
        ]
        
        # Добавляем предприятия в базу данных
        for enterprise_data in sample_enterprises:
            enterprise = Enterprise(**enterprise_data)
            db.add(enterprise)
        
        db.commit()
        print("✅ Предзаполненные предприятия добавлены в MySQL")
        
    except Exception as e:
        print(f"❌ Ошибка при инициализации предприятий: {e}")
        db.rollback()
    finally:
        db.close()

def get_all_enterprises() -> List[Dict]:
    """Получает все предприятия из базы данных"""
    db = SessionLocal()
    try:
        enterprises = db.query(Enterprise).all()
        
        result = []
        for enterprise in enterprises:
            result.append({
                "id": enterprise.id,
                "name": enterprise.name,
                "description": enterprise.description,
                "waste_description": enterprise.waste_description,
                "role": enterprise.role,
                "contact": enterprise.contact,
                "created_at": enterprise.created_at
            })
        
        return result
    finally:
        db.close()

def get_enterprises_by_role(target_role: str) -> List[Dict]:
    """Получает предприятия по роли"""
    all_enterprises = get_all_enterprises()
    return [e for e in all_enterprises if e["role"] == target_role]

def find_best_enterprises_with_llm(user_description: str, user_role: str, n_results: int = 3) -> List[Dict]:
    """Находит наиболее подходящие предприятия через LLM из всей базы данных"""
    
    # Определяем какую роль ищем (технологам нужны продавцы и наоборот)
    target_role = "sales" if user_role == "technologist" else "technologist"
    
    # Получаем все предприятия нужной роли
    target_enterprises = get_enterprises_by_role(target_role)
    
    if not target_enterprises:
        return []
    
    # Используем LLM для выбора наиболее подходящих предприятий
    selected_enterprises = select_enterprises_with_llm(
        user_description=user_description,
        user_role=user_role,
        all_enterprises=target_enterprises,
        n_results=n_results
    )
    
    return selected_enterprises

def enhance_search_results_with_llm(user_description: str, user_role: str):
    """Улучшает поиск с помощью LLM выбора из всей базы"""
    
    # Находим лучшие предприятия через LLM
    best_enterprises = find_best_enterprises_with_llm(
        user_description=user_description,
        user_role=user_role
    )
    
    # Форматируем предприятия для вывода
    formatted_enterprises = []
    for enterprise in best_enterprises:
        formatted_info = (
            f"🏭 {enterprise['name']}\n"
            f"📝 {enterprise['description']}\n"
            f"🗑️ Отходы: {enterprise['waste_description']}\n"
            f"📞 Контакт: {enterprise['contact']}"
        )
        formatted_enterprises.append(formatted_info)
    
    # Генерируем рекомендации через LLM
    recommendation = generate_recommendation(
        user_description=user_description,
        user_role=user_role,
        similar_enterprises=formatted_enterprises
    )
    
    return {
        "similar_enterprises": formatted_enterprises,
        "recommendation": recommendation
    }