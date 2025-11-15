
import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
import requests
from config import settings

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Состояния диалога
DESCRIPTION, ROLE = range(2)

# Клавиатура для выбора роли
role_keyboard = [['Технолог', 'Торговый представитель']]
role_markup = ReplyKeyboardMarkup(role_keyboard, one_time_keyboard=True, resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    welcome_text = """
🏭 Добро пожаловать в бот циркулярной экономики Беларуси!

🤖 Я помогу вам:
• Технологам - найти поставщиков сырья из отходов других предприятий
• Торговым представителям - найти покупателей ваших отходов

📝 Для начала работы:
1. Кратко опишите ваше предприятие и виды отходов/потребностей
2. Выберите вашу роль

🚀 Начнем! Введите описание вашего предприятия или отходов:
"""
    
    await update.message.reply_text(welcome_text)
    return DESCRIPTION

async def receive_description(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Получаем описание предприятия"""
    user_description = update.message.text
    context.user_data['description'] = user_description
    
    await update.message.reply_text(
        "Теперь выберите вашу роль:",
        reply_markup=role_markup
    )
    return ROLE

async def receive_role(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Получаем роль пользователя и обрабатываем запрос"""
    role_text = update.message.text
    role_map = {
        'Технолог': 'technologist',
        'Торговый представитель': 'sales'
    }
    
    if role_text not in role_map:
        await update.message.reply_text("Пожалуйста, выберите роль с помощью кнопки.")
        return ROLE
    
    role = role_map[role_text]
    description = context.user_data['description']
    
    # Показываем, что бот "думает"
    await update.message.reply_text("🔍 Анализирую базу предприятий...")
    
    try:
        # Отправляем запрос на наш FastAPI backend
        response = requests.post(
            "http://localhost:8000/api/recommend",
            json={
                "description": description,
                "role": role
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            
            # Форматируем ответ
            if data['similar_enterprises']:
                result_text = "🏭 Найдены подходящие предприятия:\n\n"
                
                for i, enterprise in enumerate(data['similar_enterprises'], 1):
                    result_text += f"{i}. {enterprise}\n\n"
                
                result_text += f" Рекомендации:\n{data['recommendation']}"
            else:
                result_text = "❌ Подходящих предприятий не найдено.\n\n"
                result_text += f" Рекомендации:\n{data['recommendation']}"
            
            await update.message.reply_text(result_text)
            
        else:
            await update.message.reply_text("❌ Произошла ошибка при обработке запроса. Попробуйте позже.")
    
    except Exception as e:
        logging.error(f"Error processing request: {e}")
        await update.message.reply_text("❌ Ошибка соединения с сервером.")
    
    # Предлагаем начать заново
    await update.message.reply_text(
        "🔄 Хотите сделать новый запрос? Введите /start",
        reply_markup=None
    )
    
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отмена диалога"""
    await update.message.reply_text(
        "Диалог отменен. Используйте /start для начала работы.",
        reply_markup=None
    )
    return ConversationHandler.END

def main():
    """Запуск бота"""
    application = Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            DESCRIPTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_description)],
            ROLE: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_role)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    
    application.add_handler(conv_handler)
    
    print("Бот запущен...")
    application.run_polling()

if __name__ == '__main__':
    main()