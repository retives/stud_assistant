from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.messages import SystemMessage
from rich.console import Console
from rich.markdown import Markdown
from dotenv import load_dotenv
import os

console = Console()
load_dotenv()

# Gemini key
ai_key = os.getenv("GEMINI_API_KEY")
if not ai_key:
    print("No api key!!!")
    exit(0)

# Agent creation
agent = ChatGoogleGenerativeAI(
    google_api_key=ai_key,
    model='gemini-2.5-flash'
)
# --- Student data ---
courses = ['']
faculty = 'Факультет інформаційних технологій'
department = 'Інженерія програмного забезпечення'
group = 'ІП-22-1'
# -------------------

# --- System prompt ---
sys_prompt = """
Ти помічник студента Івано-Франківського національного технічного університету нафти і газу студенту групи {group}, що навчається на фуакультеті {faculty}, на кафедрі {department}.
Ти допомагаєш студенту з навчальними питаннями, пов'язаними з його курсами: {courses}, а саме надаєш відповіді на питання, пояснюєш матеріал, допомагаєш з домашніми завданнями та підготовкою до іспитів.
Ти фільтруєш розклад за тими дисциплінами, що вивчає студент. Надавай корректні, точні та зрозумілі відповіді, використовуючи просту мову.
Якщо ти не знаєш відповіді на питання, чесно про це скажи.
Не вигадуй інформацію, якщо не впевнений у відповіді.
Відповідай українською мовою.
Якщо студент задає питання не пов'язане з навчанням, поясни йому, що ти спецалізований помічник з навчання та дане питання не входить в твою компетенцію.
"""
# -------------------------

chat_template = ChatPromptTemplate.from_messages([
    ('system', sys_prompt),
    ('human', '{user_input}')
])

print(chat_template.input_variables)

messages = chat_template.format_messages(
    courses=courses,
    department=department,
    faculty=faculty,
    group=group,
    user_input="Де знаходиться 1 корпус ІФНТУНГ?"
)

response = agent.invoke(messages)
console.print(Markdown(response.content))