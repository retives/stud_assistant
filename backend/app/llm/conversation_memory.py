from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, StringPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_core.messages import BaseMessage, SystemMessage
from pydantic import BaseModel, Field
from app.llm.agent import StudAgent

class ConversationSummaryBufferMemory(BaseChatMessageHistory, BaseModel):
    messages: list[BaseMessage] = Field(default_factory=list)
    llm: StudAgent = Field(default_factory=StudAgent)

    def __init__(self, llm:StudAgent):
        super().__init__(llm=llm)
    
    def add_messages(self, messages: list[BaseMessage]):

        self.messages.extend(messages)
        summary_prompt = ChatPromptTemplate(
            SystemMessagePromptTemplate(
                "Тобі треба проаналізувати користувацькі повідомлення та нові повідомлення " \
                "та згенерувати новий короткий підсумок повідомлень. Зберігай максимумінформативності за мінімум слів."
            ),
            HumanMessagePromptTemplate(
                "Історія повідомлень: \n{existing_summary}\n\n"\
                "Нові повідомлення: \n{messages}"
            )
        )
        new_summary = self.llm.invoke(
            summary_prompt.format_messages(
                existing_summary=self.messages.content,
                messages = [x.content for x in messages]
            )
        )
        self.messages = [SystemMessage(content=new_summary.content)]
        
    def clear(self):
        self.messages = []