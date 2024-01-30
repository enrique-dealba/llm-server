from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate


class MemoryLLM:
    """LLM with memory that responds to user prompts."""

    def __init__(self, llm):
        """Initializes MemoryLLM with a specified LLM."""
        self.llm = llm
        self.llm_chain = None

    def setup_memory(self):
        """Sets up the conversational memory for the LLM."""
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
        """Processes prompt using memory-augmented LLM and returns response."""
        self.setup_memory()
        response = self.llm_chain.predict(prompt=prompt)
        return response

    def __call__(self, prompt):
        """Allows MemoryLLM to be called directly with a prompt."""
        return self.run(prompt)
