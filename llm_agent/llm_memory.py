from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
)


class MemoryLLM:
    """LLM with memory that responds to user queries."""

    def __init__(self, llm):
        self.llm = llm
        self.llm_chain = None

    def setup_memory(self):
        prompt_template = ChatPromptTemplate(
            messages=[
                SystemMessagePromptTemplate.from_template(
                    "You are a helpful assistant having a conversation with a person."
                ),
                MessagesPlaceholder(variable_name="chat_history"),
                HumanMessagePromptTemplate.from_template("{question}"),
            ]
        )

        memory = ConversationBufferMemory(
            k=7,  # Number of memories
            memory_key="chat_history",
            return_messages=True,
        )

        self.llm_chain = LLMChain(
            llm=self.llm, prompt=prompt_template, verbose=True, memory=memory
        )

    def run(self, prompt: str):
        self.setup_memory()
        response = self.llm_chain({"question": prompt})
        return response

    def __call__(self, prompt):
        return self.run(prompt)
