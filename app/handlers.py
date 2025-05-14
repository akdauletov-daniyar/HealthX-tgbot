from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import CommandStart
import logging

from app.generators import gpt3_5

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = Router()

class Form(StatesGroup):
    symptoms = State()
    
    
@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    welcome_message = """👋 Добро пожаловать, я - медицинский ассистент Health-X!
Я могу помочь вам определить ваш диагноз, основываясь на ваших симптомах.

Чтобы получить предполагаемый диагноз, пожалуйста, подробно опишите свои симптомы. Например:
- Какие симптомы вы испытываете?
- Как давно у вас появились признаки заболевания?
- Есть ли какие-либо специфические возможные раздржители?
- Замечали ли вы какие-либо другие сопутствующие симптомы?

Попытайтесь предоставить как можно больше подробностей для более точной оценки"""
    
    await message.answer(welcome_message)
    await state.clear()


@router.message(Form.symptoms)
async def process_symptoms(message: Message):
    try:
        await message.answer("🔍 Анализирую ваши симптомы. Пожалуйста, подождите...")
        logger.info(f"Processing symptoms from user: {message.from_user.id}")
        
        response = await gpt3_5(message.text)
        if not response or not response.choices:
            raise Exception("No response received from OpenAI")
            
        await message.answer(response.choices[0].message.content)
        logger.info("Successfully sent response to user")
        
    except Exception as e:
        error_message = f"Error processing request: {str(e)}"
        logger.error(error_message)
        await message.answer(
            "Приношу свои извинения, но при обработке вашего запроса возникла ошибка."
            "Пожалуйста, повторите попытку через несколько минут или обратитесь к медицинскому специалисту для получения немедленной помощи."
            "Если проблема сохраняется, обратитесь в службу поддержки."
        )

@router.message(F.text)
async def process_text(message: Message, state: FSMContext):
    await state.set_state(Form.symptoms)
    await process_symptoms(message)

