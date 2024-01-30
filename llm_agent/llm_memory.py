from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    PromptTemplate,
    SystemMessagePromptTemplate,
)


class MemoryLLM:
    """LLM with memory that responds to user queries."""

    def __init__(self, llm):
        self.llm = llm
        self.llm_chain = None

    def setup_memory(self):
        template = """You are a helpful assistant having a conversation with a human.
    {chat_history}
    Human: {prompt}
    Assistant:"""

        prompt = PromptTemplate(
            input_variables=["chat_history", "prompt"], template=template
        )

        memory = ConversationBufferMemory(k=7, memory_key="chat_history")

        self.llm_chain = LLMChain(
            llm=self.llm,
            prompt=prompt,
            verbose=True,
            memory=memory,
        )

    def run(self, prompt: str):
        self.setup_memory()
        response = self.llm_chain.predict(prompt=prompt)
        return response

    def __call__(self, prompt):
        return self.run(prompt)
