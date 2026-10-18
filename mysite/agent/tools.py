from langchain_core.tools import tool
from langchain_ollama import ChatOllama
from mysite.api.user import create_user, list_user, detail_user, update_user, delete_user

model = ChatOllama(
    model="llama3.2:latest",
    temperature=0
)

@tool
async def count_words(text: str):
    """Считает количество слов в тексте."""
    return len(text.split())

@tool
async def to_lower(text: str):
    """Преобразует текст в нижний регистр."""
    return text.lower()

@tool
async def count_tokens(text: str):
    """Получает количество токенов из метаданных модели."""
    response = await model.ainvoke(text)
    usage_token = response.usage_metadata or {}

    return {
        "input_tokens": usage_token.get("input_tokens", 0),
        "output_tokens": usage_token.get("output_tokens", 0),
        "total_tokens": usage_token.get("total_tokens", 0),
    }

@tool
async def get_list():
    """Показывает список всех профилей пользователей."""
    return await list_user()

@tool
async def get_detail(user_id: int):
    """Находит профиль пользователя по id."""
    return await detail_user(user_id)

@tool
async def post_user():
    """Создает профиль пользователя."""
    return await create_user()

@tool
async def put_user(user_id: int):
    """Изменяет профиль пользователя."""
    return await update_user(user_id)

@tool
async def del_user(user_id: int):
    """Удаляет профиль пользователя по id."""
    return await delete_user(user_id)

tools = [count_words, count_tokens, get_list, post_user, put_user, del_user, to_lower]

model_tool = model.bind_tools(tools)



