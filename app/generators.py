import os
from dotenv import load_dotenv
from openai import AsyncOpenAI
import logging

load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize OpenAI client
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables")

client = AsyncOpenAI(api_key=api_key)

async def gpt3_5(symptoms):
    try:
        system_prompt = """Вы - ассистент по медицинской диагностике. Основываясь на представленных симптомах, вы должны:
1. Перечислить возможные диагнозы (сначала наиболее вероятные)
2. Для каждого диагноза укажите:
   - Краткое описание
   - Рекомендуемые методы лечения
   - Необходимые меры предосторожности
   - Общие лекарства (если применимо)
3. В конце ответа кратко напомни о том, что данный ассистент не является заменой профессиональной медицинской консультации.

Отвечай кратко, но детально. Не используй форматирование текста в стиле Markdown."""

        logger.info(f"Making API call to OpenAI with symptoms: {symptoms[:100]}...")
        
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Please analyze these symptoms and provide a medical assessment: {symptoms}"}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        
        logger.info("Successfully received response from OpenAI")
        return response
        
    except Exception as e:
        logger.error(f"Error in gpt3_5: {str(e)}")
        raise Exception(f"OpenAI API Error: {str(e)}")
