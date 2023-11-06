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
        def parse_string(input_str):
            """ Robustly parses input string removing surrounding quotes (', ", `) """
            if len(input_str) < 2:
                return input_str
            
            first_char = input_str[0]
            last_char = input_str[-1]
            
            # Check if the first and last characters are matching quotes
            if first_char == last_char and first_char in "\"'`":
                return input_str[1:-1]
            
            return input_str
        def parse_repeated_string(input_str):
            """
            Parses a repeated string with backticks and potential punctuation, 
            removing the backticks and duplicates.
            """
            # Removing backticks and punctuation, then splitting by spaces
            words = re.sub(r"[`',]", "", input_str).split()

            unique_words = list(set(words))

            return " ".join(unique_words)

        # Checks if agent should finish
        pre_final = "Final Answer:" # deleted the ':'
        post_final = "Final Answer"
        if pre_final in llm_output:
            print("pre_final detected!!!")
            return AgentFinish(
                return_values={"output": llm_output.split(pre_final)[-1].strip()},
                log=llm_output,
            )
        elif post_final in llm_output:
            print("post_final detected!!!")
            return AgentFinish(
                return_values={"output": llm_output.split(post_final)[-1].strip()},
                log=llm_output,
            )
        # Parse out the action and action input
        regex = r"Action\s*\d*\s*:(.*?)\nAction\s*\d*\s*Input\s*\d*\s*:[\s]*(.*)"
        match = re.search(regex, llm_output, re.DOTALL)
        if not match:
            raise ValueError(f"Could not parse LLM output: `{llm_output}`")

        # Action parsing
        print("="*40)
        action = match.group(1).strip()
        print("Action before:", action)
        action = parse_string(action)
        print("Action after parse:", action)

        # Action input parsing
        action_input = match.group(2)
        print("action_input before:", action_input)
        action_input = parse_repeated_string(action_input)
        print("action_input after parse:", action_input)
        print("="*40)

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
When you have or know the answer to the user question use the format:
Thought: I now know the final answer
Final Answer: The final answer should answer the user question

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
When you have or know the answer to the user question use the format:
Thought: I now know the final answer
Final Answer: The final answer should answer the user question

Previous conversation history:
{history}

New question: {input}
{agent_scratchpad}"""

## Llama-index style prefix for ReAct
PREFIX = """\
Given a user question, and a list of tools, output a list of relevant sub-questions \
in json markdown that when composed can help answer the full user question:

"""

ZEPHYR_SYSTEM_PREFIX = "<|system|>\n"
ZEPHYR_SYSTEM_SUFFIX = "</s>\n"

## MISTRAL TEMPLATE #3
mistral_template_agent = PREFIX + """Available Tools: {tools}

Use the following format:

Task: the input task you must solve by outputting a valid response to the user task
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
When you have or know the answer to the user question use the format:
Thought: I now know the final answer
Final Answer: The final answer should answer the user question

Previous conversation history:
{history}

User question: {input}
{agent_scratchpad}"""

mistral_template_3 = ZEPHYR_SYSTEM_PREFIX + mistral_template_agent + ZEPHYR_SYSTEM_SUFFIX

mistral_template_4 = mistral_template_agent

ZEPHYR_USER = "<|user|>"
ZEPHYR_SUFFIX = "</s>"

mistral_template_agent2 = PREFIX + """Available Tools: {tools}

Use the following format:

Task: the input task you must solve by outputting a valid response to the user task
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
When you have or know the answer to the user question use the format:
Thought: I now know the final answer
Final Answer: The final answer should answer the user question

Previous conversation history:
{history}

<|user|>
User question: {input} </s>
{agent_scratchpad}"""

mistral_template_5 = mistral_template_agent2

mistral_template_6 = ZEPHYR_SYSTEM_PREFIX + mistral_template_agent2 + ZEPHYR_SYSTEM_SUFFIX

mistral_template_agent3 = PREFIX + """ <|system|>
Available Tools: {tools}

Use the following format:

Task: the input task you must solve by outputting a valid response to the user task
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
When you have or know the answer to the user question use the format:
Thought: I now know the final answer
Final Answer: The final answer should answer the user question
</s>

Previous conversation history:
{history}

<|user|>
User question: {input} </s>
{agent_scratchpad}"""

mistral_template_7 = mistral_template_agent3

mistral_template_8 = ZEPHYR_SYSTEM_PREFIX + mistral_template_agent3 + ZEPHYR_SYSTEM_SUFFIX
