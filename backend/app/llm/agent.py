from langchain_core.prompts import ChatPromptTemplate, PromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory, ConfigurableFieldSpec, RunnableConfig
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage
from langchain_community.chat_message_histories import ChatMessageHistory
from dotenv import load_dotenv
from langsmith import traceable
from app.database import get_db
from app.models import Message
import os

load_dotenv()
system_id = os.getenv("SYSTEM_ID")
def get_chat_history(conversation_id: str):
    db = next(get_db())
    db_messages = db.query(Message).filter(
        Message.conversation_id == conversation_id
    ).order_by(Message.date.asc()).all()


    langchain_history = ChatMessageHistory()
    for msg in db_messages:
        if msg.sender_id != system_id:
            langchain_history.add_message(HumanMessage(content=msg.content))
        else:
            langchain_history.add_message(AIMessage(content=msg.content))

    return langchain_history

class StudAgent:
    def __init__(self, courses, faculty, department, group, ai_key):
        self.courses = courses
        self.faculty = faculty
        self.department = department
        self.group = group
        self.agent = ChatGoogleGenerativeAI(
            google_api_key=ai_key,
            model='gemini-2.5-flash'
        )


    # --- System prompt ---
        self.chat_prompt = ChatPromptTemplate([
            ("system",""""
    Ти помічник студента Івано-Франківського національного технічного університету нафти і газу студенту групи {group}, що навчається на факультеті {faculty}, на кафедрі {department}.
    Ти допомагаєш студенту з навчальними питаннями, пов'язаними з його курсами: {courses}, а саме надаєш відповіді на питання, пояснюєш матеріал, допомагаєш з домашніми завданнями та підготовкою до іспитів.
    Ти фільтруєш розклад за тими дисциплінами, що вивчає студент. Надавай корректні, точні та зрозумілі відповіді, використовуючи просту мову.
    Якщо ти не знаєш відповіді на питання, чесно про це скажи.
    Не вигадуй інформацію, якщо не впевнений у відповіді.
    Відповідай українською мовою.
    Якщо студент задає питання не пов'язане з навчанням, поясни йому, що ти спецалізований помічник з навчання та дане питання не входить в твою компетенцію.
    Якщо тобі не вистачає інформації про студента, запитай його щодо уточнення цих даних.
    """),
            MessagesPlaceholder(variable_name="history"),
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
        chat_pipeline = self.chat_prompt | self.agent

        self.pipeline_with_history = RunnableWithMessageHistory(
            chat_pipeline,
            get_session_history=get_chat_history,
            history_messages_key='history',
            history_factory_config=[
                ConfigurableFieldSpec(
                    id='chat_history',
                    annotation=str,
                    name='Chat History',
                    description='Chat History',
                    default=None,
                )
            ]
        )
    # End of __init__

    # Main tool to generate responses
    @traceable
    def ask(self, message, conversation_id):
        config = RunnableConfig(configurable={"chat_history": conversation_id})
        response = self.pipeline_with_history.invoke(
            {"user_input": message,
             "group": self.group,
             "faculty": self.faculty,
             "department": self.department,
             "courses": self.courses},
            config=config
        )
        return response.content if hasattr(response, 'content') else response

    # Initial title generation
    @traceable
    def get_title(self, message):
        title_messages = self.title_prompt.format(
            user_message=message,
        )
        response =  self.agent.invoke(title_messages)

        return response.content if hasattr(response, 'content') else response

