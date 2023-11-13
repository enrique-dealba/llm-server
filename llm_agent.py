from langchain.agents import AgentExecutor, LLMSingleActionAgent
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferWindowMemory

from tools.custom_tools import (get_planet_distance_tool,
                                get_skyfield_planets_tool,
                                get_latitude_longitude_tool,
                                get_skyfield_satellites_tool,
                                get_next_visible_time_for_satellite_tool)
from tools.prompts import (CustomOutputParser, CustomPromptTemplate,
                           mistral_template_1, mistral_template_2,
                           mistral_template_3, mistral_template_4,
                           mistral_template_5, mistral_template_6,
                           mistral_template_7, mistral_template_8,
                           mistral_1, mistral_2, mistral_3,
                           mistral_4, mistral_5)


class LLMAgent:
    """LLM Agent server that performs user tasks."""
    def __init__(self, llm):
        self.llm = llm
        self.output_parser = CustomOutputParser()

        self.custom_template = None
        self.agent = None
        self.memory = None
        self.tools = None
        self.agent_executor = None

        self.queries = []
        self.agent_thoughts = []

    def add_query(self, query):
        self.queries.append(query)

    def init_agent(self):
        custom_tools = []

        ## Add list of API tools
        # custom_tools += [get_skyfield_planets_tool]
        # custom_tools += [get_planet_distance_tool]
        # custom_tools += [get_latitude_longitude_tool]
        # custom_tools += [get_skyfield_satellites_tool]
        custom_tools += [get_next_visible_time_for_satellite_tool]

        # TODO: mistral_1 - 5 testing
        api_template = mistral_1 # or 1, 2, 3, etc
        
        self.custom_template = CustomPromptTemplate(
            template=api_template,
            tools=custom_tools,
            agent_thoughts=self.agent_thoughts,
            input_variables=["input", "intermediate_steps", "history"]
        )

        llm_chain = LLMChain(llm=self.llm, prompt=self.custom_template)
        tool_names = [t.name for t in custom_tools]

        self.agent = LLMSingleActionAgent(
            llm_chain=llm_chain,
            output_parser=self.output_parser,
            stop=["\nObservation:"],
            allowed_tools=tool_names
        )

        num_memories = 3 # keep small, at most <=10
        self.memory = ConversationBufferWindowMemory(k=num_memories)
        self.tools = custom_tools

        max_iterations = 5 # changed from 8 -> 5
        self.agent_executor = AgentExecutor.from_agent_and_tools(
            agent=self.agent,
            tools=self.tools,
            verbose=True,
            memory=self.memory,
            max_iterations=max_iterations
        )

    def validate_agent(self):
        assert self.custom_template is not None
        assert self.agent is not None
        assert self.memory is not None
        assert self.tools is not None
        assert self.agent_executor is not None

    def get_task(self, prompt: str) -> str:
        # Prompt for Mistral-based agent.
        prefix = "[INST] "
        suffix = " [/INST]"
        # template = f'''Given the following user task: `{prompt}`, Use your Skyfield tools for planets to answer the user question'''
        template_agostic = f'''Given the following user task: `{prompt}`, Use your tools to answer the user question'''
        new_prompt = prefix + template_agostic + suffix
        return new_prompt

    def reset_thoughts(self):
        self.agent_thoughts = []

    def get_responses(self, prompt, responses):
        task = self.get_task(prompt)

        response = ""
        try:
            response = self.agent_executor.run(task)
        except ValueError as e:
            print(f"agent_executor error: {e}")

        agent_thoughts = self.custom_template.agent_thoughts

        if response == "":
            responses += agent_thoughts
            responses += ["I don't know."]
            self.reset_thoughts()
            return responses
        
        responses += [response]
        
        return responses
    
    def run(self, prompt: str):
        responses = []

        self.init_agent()
        self.validate_agent()

        responses = self.get_responses(prompt, responses)

        self.reset_thoughts()
        return responses
