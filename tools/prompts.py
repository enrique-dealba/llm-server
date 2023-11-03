import re
from typing import List, Union

from langchain.prompts import StringPromptTemplate
from langchain.agents import Tool, AgentOutputParser
from langchain.schema import AgentAction, AgentFinish

class CustomPromptTemplate(StringPromptTemplate):
    template: str
    # The list of available tools
    tools: List[Tool]
    agent_thoughts: list
    
    def format(self, **kwargs) -> str:
        # Get the intermediate steps (AgentAction, Observation tuples)
        # Formats them in a particular way
        intermediate_steps = kwargs.pop("intermediate_steps")
        thoughts = ""
        for action, observation in intermediate_steps:
            self.agent_thoughts += [str(action.log) + "\nObservation: " + str(observation)]
            thoughts += action.log
            thoughts += f"\nObservation: {observation}\nThought: "
        
        kwargs["agent_scratchpad"] = thoughts
        kwargs["tools"] = "\n".join([f"{tool.name}: {tool.description}" for tool in self.tools])
        kwargs["tool_names"] = ", ".join([tool.name for tool in self.tools])
        return self.template.format(**kwargs)

class CustomOutputParser(AgentOutputParser):
    
    def parse(self, llm_output: str) -> Union[AgentAction, AgentFinish]:
        # Checks if agent should finish
        pre_final = "Final Answer:" # deleted the ':'
        post_final = "Final Answer"
        if pre_final in llm_output:
            return AgentFinish(
                return_values={"output": llm_output.split(pre_final)[-1].strip()},
                log=llm_output,
            )
        elif post_final in llm_output:
            return AgentFinish(
                return_values={"output": llm_output.split(post_final)[-1].strip()},
                log=llm_output,
            )
        # Parse out the action and action input
        regex = r"Action\s*\d*\s*:(.*?)\nAction\s*\d*\s*Input\s*\d*\s*:[\s]*(.*)"
        match = re.search(regex, llm_output, re.DOTALL)
        if not match:
            raise ValueError(f"Could not parse LLM output: `{llm_output}`")
        action = match.group(1).strip()
        action_input = match.group(2)

        return AgentAction(tool=action, tool_input=action_input.strip(" ").strip('"'), log=llm_output)


## MISTRAL TEMPLATE #1
mistral_template_1 = """<s> [INST] You are an assistant for creating a sequential workflow based on the users query. If you don't know the answer, just say that you don't know. 

Create a plan represented in JSON by only using the tools listed below. The workflow should be a JSON array containing only the sequence index, function name and input. A step in the workflow can receive the output from a previous step as input.
[/INST] </s>

[INST] Available Tools: {tools}

Use the following format:

Task: the input task you must solve by outputting a valid response to the user task
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)

Previous conversation history:
{history}

New question: {input}
{agent_scratchpad}[/INST]"""

## MISTRAL TEMPLATE #2
mistral_template_2 = """# Prompt

Objective:
Your objective is to create a sequential workflow based on the users query.

Create a plan represented by only using the tools listed below. The workflow should contain only the sequence index, function name and input. A step in the workflow can receive the output from a previous step as input.

Available Tools: {tools}

Use the following format:

Task: the input task you must solve by outputting a valid response to the user task
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)

Previous conversation history:
{history}

New question: {input}
{agent_scratchpad}"""

## Llama-index style prefix for ReAct
PREFIX = """\
Given a user question, and a list of tools, output a list of relevant sub-questions \
in json markdown that when composed can help answer the full user question:

"""

## MISTRAL TEMPLATE #3
mistral_template_3 = PREFIX + """Available Tools: {tools}

Use the following format:

Task: the input task you must solve by outputting a valid response to the user task
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)

Previous conversation history:
{history}

User question: {input}
{agent_scratchpad}"""