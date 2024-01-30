from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate


template_1 = """<s>[INST] You are a helpful assistant.[/INST]</s> 
{chat_history}
Human: {prompt}
Assistant:"""

template_2 = """<s>[INST] You are a helpful assistant.[/INST]
{chat_history}
Human: {prompt}</s> 
Assistant:"""

template_3 = """<s>[INST] You are a helpful assistant.[/INST]</s>
{chat_history}
Human: {prompt}"""

template_4 = """<s>[INST] You are a helpful assistant.[/INST]</s>
{chat_history}
Human: <s>[INST] {prompt} [/INST]</s>"""

template_5 = """<s>[INST] You are a helpful assistant.[/INST]</s>
{chat_history}
Human: <s>[INST] {prompt} [/INST]</s>
Assistant:"""

template_6 = """<s>[INST] You are a helpful assistant.[/INST]</s>
{chat_history}
<s>[INST] {prompt} [/INST]</s>
Assistant:"""

template_7 = """<s>[INST] You are a helpful assistant.[/INST]</s>
{chat_history}
<s>[INST] {prompt} [/INST]</s>"""

template_8 = """{chat_history}
<s>[INST] {prompt} [/INST]</s>"""

template_9 = """{chat_history}
<s>[INST] {prompt} [/INST]</s>
Assistant:"""


class MemoryLLM:
    """LLM with memory that responds to user prompts."""

    def __init__(self, llm):
        """Initializes MemoryLLM with a specified LLM."""
        self.llm = llm
        self.llm_chain = None

    def setup_memory(self):
        """Sets up the conversational memory for the LLM."""
        prompt = PromptTemplate(
            input_variables=["chat_history", "prompt"], template=template_1
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
