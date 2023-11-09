import os

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, Response, StreamingResponse
from langchain.llms import VLLM

from llm_agent import LLMAgent


class Config:
    def __init__(self):
        self.opt_model = "facebook/opt-125m"
        self.mistral_model = "mistralai/Mistral-7B-Instruct-v0.1"
        self.zephyr_model = "HuggingFaceH4/zephyr-7b-beta"
        self.llm_model = os.getenv("MODEL", self.zephyr_model)

        # LLM Configs
        self.num_gpus = 1
        self.temperature = 0.2
        self.max_new_tokens = 512

    def create_llm(self):
        return VLLM(
            model=self.llm_model,
            temperature=self.temperature,
            use_beam_search=False,
            max_new_tokens=self.max_new_tokens,
            tensor_parallel_size=self.num_gpus,
            trust_remote_code=True,
        )

app = FastAPI()

# opt_model = "facebook/opt-125m" # For testing
# mistral_model = "mistralai/Mistral-7B-Instruct-v0.1"
# zephyr_model = "HuggingFaceH4/zephyr-7b-beta" # works with RAG and ReAct

# # Setting model directly
# llm_model = os.getenv("MODEL", "HuggingFaceH4/zephyr-7b-beta")

# NUM_GPUS = 1
# llm = VLLM(
#     model=llm_model,
#     temperature=0.2,
#     use_beam_search=False,
#     max_new_tokens=512,
#     tensor_parallel_size=NUM_GPUS,
#     trust_remote_code=True,
# )

# class LLMAgent:
#     """LLM Agent server that performs user tasks."""
#     def __init__(self, llm):
#         self.llm = llm
#         self.output_parser = CustomOutputParser()

#         self.custom_template = None
#         self.agent = None
#         self.memory = None
#         self.tools = None
#         self.agent_executor = None

#         self.queries = []
#         self.agent_thoughts = []

#     def add_query(self, query):
#         self.queries.append(query)

#     def init_agent(self):
#         custom_tools = []

#         ## Add list of API tools
#         custom_tools += [get_skyfield_planets_tool]
#         # custom_tools += [get_planet_distance_tool]
#         # custom_tools += [get_latitude_longitude_tool]
#         # custom_tools += [get_skyfield_satellites_tool]
#         # custom_tools += [get_next_visible_time_for_satellite_tool]

#         api_template = mistral_template_7 # or 1, 2, 3, etc
        
#         self.custom_template = CustomPromptTemplate(
#             template=api_template,
#             tools=custom_tools,
#             agent_thoughts=self.agent_thoughts,
#             input_variables=["input", "intermediate_steps", "history"]
#         )

#         llm_chain = LLMChain(llm=self.llm, prompt=self.custom_template)
#         tool_names = [t.name for t in custom_tools]

#         self.agent = LLMSingleActionAgent(
#             llm_chain=llm_chain,
#             output_parser=self.output_parser,
#             stop=["\nObservation:"],
#             allowed_tools=tool_names
#         )

#         num_memories = 3 # keep small, at most <=10
#         self.memory = ConversationBufferWindowMemory(k=num_memories)
#         self.tools = custom_tools

#         max_iterations = 5 # changed from 8 -> 5
#         self.agent_executor = AgentExecutor.from_agent_and_tools(
#             agent=self.agent,
#             tools=self.tools,
#             verbose=True,
#             memory=self.memory,
#             max_iterations=max_iterations
#         )

#     def validate_agent(self):
#         assert self.custom_template is not None
#         assert self.agent is not None
#         assert self.memory is not None
#         assert self.tools is not None
#         assert self.agent_executor is not None

#     def get_task(self, prompt: str) -> str:
#         # Prompt for Mistral-based agent.
#         prefix = "[INST] "
#         suffix = " [/INST]"
#         # template = f'''Given the following user task: `{prompt}`, Use your Skyfield tools for planets to answer the user question'''
#         template_agostic = f'''Given the following user task: `{prompt}`, Use your tools to answer the user question'''
#         new_prompt = prefix + template_agostic + suffix
#         return new_prompt

#     def reset_thoughts(self):
#         self.agent_thoughts = []

#     def get_responses(self, prompt, responses):
#         task = self.get_task(prompt)

#         response = ""
#         try:
#             response = self.agent_executor.run(task)
#         except ValueError as e:
#             print(f"agent_executor error: {e}")

#         agent_thoughts = self.custom_template.agent_thoughts

#         if response == "":
#             responses += agent_thoughts
#             responses += ["I don't know."]
#             self.reset_thoughts()
#             return responses
        
#         responses += [response]
        
#         return responses
    
#     def run(self, prompt: str):
#         responses = []

#         self.init_agent()
#         self.validate_agent()

#         responses = self.get_responses(prompt, responses)

#         self.reset_thoughts()
#         return responses

# Initialize configurations and dependencies
config = Config()

llm = config.create_llm()
llm_agent = LLMAgent(llm=llm)

app = FastAPI()

@app.post("/generate")
async def generate(request: Request):
    request_dict = await request.json()
    query = request_dict.pop("text", None)
    
    llm_agent.add_query(query)

    response = llm_agent.run(query)

    ret = {"text": response, "queries": llm_agent.queries}

    return JSONResponse(ret)
