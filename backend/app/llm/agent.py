from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_classic.memory import ConversationBufferMemory
from langchain.messages import SystemMessage
from rich.console import Console
from rich.markdown import Markdown
from dotenv import load_dotenv
from app.services.classifier import predict_label, preprocess_text, vectorizer, classifier
from langsmith import traceable
import os

load_dotenv()

# Gemini key
key = os.getenv("GEMINI_API_KEY")
if not key:
    print("No api key!!!")
    exit(0)


class StudAgent:
    def __init__(self, courses, faculty, department, group, ai_key):
        # Saving the user data
        self.courses = courses
        self.faculty = faculty
        self.department = department
        self.group = group
        # Agent creation
        self.agent = ChatGoogleGenerativeAI(
            google_api_key=ai_key,
            model='gemini-2.5-flash'
        )



    # --- System prompt ---
        self.chat_prompt = ChatPromptTemplate([
            ("system",""""
    Ти помічник студента Івано-Франківського національного технічного університету нафти і газу студенту групи {group}, що навчається на фуакультеті {faculty}, на кафедрі {department}.
    Ти допомагаєш студенту з навчальними питаннями, пов'язаними з його курсами: {courses}, а саме надаєш відповіді на питання, пояснюєш матеріал, допомагаєш з домашніми завданнями та підготовкою до іспитів.
    Ти фільтруєш розклад за тими дисциплінами, що вивчає студент. Надавай корректні, точні та зрозумілі відповіді, використовуючи просту мову.
    Якщо ти не знаєш відповіді на питання, чесно про це скажи.
    Не вигадуй інформацію, якщо не впевнений у відповіді.
    Відповідай українською мовою.
    Якщо студент задає питання не пов'язане з навчанням, поясни йому, що ти спецалізований помічник з навчання та дане питання не входить в твою компетенцію.
    Якщо тобі не вистачає інформації про студента, запитай його щодо уточнення цих даних.
    """),
            ("human", "{user_input}")
        ])
    # -------------------------
        self.title_prompt = PromptTemplate(
            input_variables=["user_message"],
            template="""
                        Проаналізуй повідомлення:
                        "{user_message}"
                        і створи короткий заголовок, який описує його суть. 
                        Відповідай лише заголовком.
                    """
        )
    # Main tool to generate responses
    @traceable
    def ask(self, message):
        chat_messages = self.chat_prompt.format_messages(
            courses= self.courses,
            faculty=self.faculty,
            department=self.department,
            group=self.group,
            user_input=message
        )

        response = self.agent.invoke(chat_messages)
        return response.content if hasattr(response, 'content') else response

    # Initial title generation
    @traceable
    def get_title(self, message):
        title_messages = self.title_prompt.format(
            user_message=message,
        )
        response =  self.agent.invoke(title_messages)
        return response.content if hasattr(response, 'content') else response
    def update_user_info(self, courses, faculty, department, group):
        self.courses = courses
        self.faculty = faculty
        self.department = department
        self.group = group

# Agent instance to export
stud_agent = StudAgent(
    courses=[],
    faculty=None,
    department=None,
    group=None,
    ai_key=key
)


if __name__ == '__main__':
    chat_agent = StudAgent(
        # --- Student data ---
        courses=[''],
        faculty = 'Факультет інформаційних технологій',
        department = 'Інженерія програмного забезпечення',
        group = 'ІП-22-1',
        # api key
        ai_key=key
    )
    user_message = "Як справлятись з вигоранням студенту?"
    label = predict_label(preprocess_text(user_message))
    print(label)
    response = chat_agent.ask(user_message)
    title = chat_agent.get_title(user_message)

    console = Console()
    console.print(title)
    console.print(response)