# import os
# from haystack.agents.base import Tool
# from haystack.agents.conversational import ConversationalAgent
# from haystack.agents.memory import ConversationSummaryMemory
# from haystack.document_stores import InMemoryDocumentStore
# from haystack.nodes import BM25Retriever, PromptNode
# from haystack.pipelines import DocumentSearchPipeline
# import chainlit as cl
# import logging
# from xbrlparser import write_financial_data
# from chainlit.input_widget import TextInput


# openai_api_key = os.environ.get("OPENAI_API_KEY")
# if not openai_api_key:
#  raise ValueError("Please set the OPENAI_API_KEY environment variable")


# # Create a TextInput widget
# url_input = TextInput(label="Please provide the URL of the XBRL document you want to parse (This URL should end with '.htm').")

# # Get the value entered by the user
# xbrl_url = url_input.value

# write_financial_data(url=xbrl_url)


# @cl.cache
# def get_retriever():
#  document_store = InMemoryDocumentStore(use_bm25=True)

#  # Load your data
#  with open(r"reader.txt", "r") as f:
#   data = f.read()
#  documents = [{"content": data}]
#  document_store.write_documents(documents)

#  return BM25Retriever(document_store)

# @cl.cache
# def get_agent(retriever):
#  pipeline = DocumentSearchPipeline(retriever)

#  search_tool = Tool(
#   name="xbrl_report_parser",
#   pipeline_or_node=pipeline,
#   description="useful for when you need to answer questions about financial statements of companies",
#   output_variable="documents",
#  )

#  conversational_agent_prompt_node = PromptNode(
#   "gpt-3.5-turbo",
#   api_key=openai_api_key,
#   max_length=256,
#   stop_words=["Observation:"],
#  )

#  memory = ConversationSummaryMemory(
#   conversational_agent_prompt_node,
#   prompt_template="deepset/conversational-summary",
#   summary_frequency=3,
#  )

#  agent_prompt = """
# In the following conversation, a human user interacts with an AI Agent. The human user poses questions, and the AI Agent goes through several steps to provide well-informed answers.
# The AI Agent must use the available tools to find the up-to-date information. The final answer to the question should be truthfully based solely on the output of the tools. The AI Agent should ignore its knowledge when answering the questions.
# The AI Agent has access to these tools:
# {tool_names_with_descriptions}

# The following is the previous conversation between a human and The AI Agent:
# {memory}

# AI Agent responses must start with one of the following:

# Thought: [the AI Agent's reasoning process]
# Tool: [tool names] (on a new line) Tool Input: [input as a question for the selected tool WITHOUT quotation marks and on a new line] (These must always be provided together and on separate lines.)
# Observation: [tool's result]
# Final Answer: [final answer to the human user's question]
# When selecting a tool, the AI Agent must provide both the "Tool:" and "Tool Input:" pair in the same response, but on separate lines.

# The AI Agent should not ask the human user for additional information, clarification, or context.
# If the AI Agent cannot find a specific answer after exhausting available tools and approaches, it answers with Final Answer: inconclusive

# Question: {query}
# Thought:
# {transcript}
# """

#  return ConversationalAgent(
#   prompt_node=conversational_agent_prompt_node,
#   memory=memory,
#   prompt_template=agent_prompt,
#   tools=[search_tool],
#  )

# retriever = get_retriever()
# agent = get_agent(retriever)
# cl.HaystackAgentCallbackHandler(agent)

# @cl.author_rename
# def rename(orig_author: str):
#  rename_dict = {"custom-at-query-time": "Agent Step"}
#  return rename_dict.get(orig_author, orig_author)

# @cl.on_chat_start
# async def init():
#     # Ask for the URL of the XBRL document
#     question = "Please provide the URL of the XBRL document you want to parse (This URL should end with '.htm')."
#     await cl.Message(author="Agent", content=question).send()

# @cl.on_message
# async def get_xbrl_url(message):
#     if message.author == "User":
#         xbrl_url = message.content
#         if not xbrl_url.endswith('.htm'):
#             await cl.Message(author="Agent", content="The provided URL does not end with '.htm'. Please provide a valid URL.").send()
#             return

#         try:
#             write_financial_data(url=xbrl_url)
            
#             with open('reader.txt', 'r') as f:
#                 updated_xbrl_content = f.read()
            
#             documents = [{"content": updated_xbrl_content}]
#             retriever.document_store.write_documents(documents)

#             await cl.Message(author="Agent", content="The XBRL document has been successfully fetched and written to the file. You can now ask questions about the new data.").send()
#         except Exception as e:
#             await cl.Message(author="Agent", content=f"An error occurred: {e}").send()

# # @cl.on_chat_start
# # async def init():
# #     question = "Hi"
# #     await cl.Message(author="User", content=question).send()
# #     response = await cl.make_async(agent.run)(question)
# #     await cl.Message(author="Agent", content=response["answers"][0].answer).send()

# #     # Ask for the URL of the XBRL document
# #     question = "Please provide the URL of the XBRL document you want to parse (This URL should end with '.htm')."
# #     await cl.Message(author="Agent", content=question).send()

# # @cl.on_message
# # async def get_xbrl_url(message):
# #     if message.author == "User":
# #         xbrl_url = message.content
# #         try:
# #             # Assuming fetch_ixbrl is an async function that fetches the content of the XBRL file
# #             await write_financial_data(url=xbrl_url)
            
# #             # Now, read the newly written file to confirm it has the updated content
# #             with open('read.txt', 'r') as f:
# #                 updated_xbrl_content = f.read()
            
# #             # Update the document_store with the contents of the new XBRL
# #             documents = [{"content": updated_xbrl_content}]
# #             retriever.document_store.write_documents(documents)
# #         except Exception as e:
# #             # Handle any exceptions that occur during the fetch and write process
# #             print(f"An error occurred: {e}")


# @cl.on_message
# async def answer(message: cl.Message):
#  response = await cl.make_async(agent.run)(message.content)
#  await cl.Message(author="Agent", content=response["answers"][0].answer).send()




# import os
# from haystack.agents.base import Tool
# from haystack.agents.conversational import ConversationalAgent
# from haystack.agents.memory import ConversationSummaryMemory
# from haystack.document_stores import InMemoryDocumentStore
# from haystack.nodes import BM25Retriever, PromptNode
# from haystack.pipelines import DocumentSearchPipeline
# import chainlit as cl
# import logging
# from xbrlparser import write_financial_data
# from chainlit.input_widget import TextInput


# openai_api_key = os.environ.get("OPENAI_API_KEY")
# if not openai_api_key:
#  raise ValueError("Please set the OPENAI_API_KEY environment variable")


# @cl.cache
# def get_retriever():
#  document_store = InMemoryDocumentStore(use_bm25=True)

#  # Load your data
#  with open(r"reader.txt", "r") as f:
#   data = f.read()
#  documents = [{"content": data}]
#  document_store.write_documents(documents)

#  return BM25Retriever(document_store)

# @cl.cache
# def get_agent(retriever):
#  pipeline = DocumentSearchPipeline(retriever)

#  search_tool = Tool(
#   name="xbrl_report_parser",
#   pipeline_or_node=pipeline,
#   description="useful for when you need to answer questions about financial statements of companies",
#   output_variable="documents",
#  )

#  conversational_agent_prompt_node = PromptNode(
#   "gpt-3.5-turbo",
#   api_key=openai_api_key,
#   max_length=256,
#   stop_words=["Observation:"],
#  )

#  memory = ConversationSummaryMemory(
#   conversational_agent_prompt_node,
#   prompt_template="deepset/conversational-summary",
#   summary_frequency=3,
#  )

#  agent_prompt = """
# In the following conversation, a human user interacts with an AI Agent. The human user poses questions, and the AI Agent goes through several steps to provide well-informed answers.
# The AI Agent must use the available tools to find the up-to-date information. The final answer to the question should be truthfully based solely on the output of the tools. The AI Agent should ignore its knowledge when answering the questions.
# The AI Agent has access to these tools:
# {tool_names_with_descriptions}

# The following is the previous conversation between a human and The AI Agent:
# {memory}

# AI Agent responses must start with one of the following:

# Thought: [the AI Agent's reasoning process]
# Tool: [tool names] (on a new line) Tool Input: [input as a question for the selected tool WITHOUT quotation marks and on a new line] (These must always be provided together and on separate lines.)
# Observation: [tool's result]
# Final Answer: [final answer to the human user's question]
# When selecting a tool, the AI Agent must provide both the "Tool:" and "Tool Input:" pair in the same response, but on separate lines.

# The AI Agent should not ask the human user for additional information, clarification, or context.
# If the AI Agent cannot find a specific answer after exhausting available tools and approaches, it answers with Final Answer: inconclusive

# Question: {query}
# Thought:
# {transcript}
# """

#  return ConversationalAgent(
#   prompt_node=conversational_agent_prompt_node,
#   memory=memory,
#   prompt_template=agent_prompt,
#   tools=[search_tool],
#  )

# retriever = get_retriever()
# agent = get_agent(retriever)
# cl.HaystackAgentCallbackHandler(agent)

# @cl.author_rename
# def rename(orig_author: str):
#  rename_dict = {"custom-at-query-time": "Agent Step"}
#  return rename_dict.get(orig_author, orig_author)

# @cl.on_chat_start
# async def init():
#     # Ask for the URL of the XBRL document
#     question = "Please provide the URL of the XBRL document you want to parse (This URL should end with '.htm')."
#     await cl.Message(author="Agent", content=question).send()

# cl.on_message
# async def handle_message(message: cl.Message):
#     try:
#         if message.author == "User":
#             # The user's message is in message.content
#             xbrl_url = message.content

#             # Now you can call your write_financial_data function with the URL
#             write_financial_data(url=xbrl_url)

#             # Now, read the newly written file to confirm it has the updated content
#             with open('reader.txt', 'r') as f:
#                 updated_xbrl_content = f.read()
            
#             # Update the document_store with the contents of the new XBRL
#             documents = [{"content": updated_xbrl_content}]
#             retriever.document_store.write_documents(documents)
#     except Exception as e:
#         # Handle any exceptions that occur during the fetch and write process
#         print(f"An error occurred: {e}")

# @cl.on_message
# async def answer(message: cl.Message):
#  response = await cl.make_async(agent.run)(message.content)
#  await cl.Message(author="Agent", content=response["answers"][0].answer).send()











# import os
# from haystack.agents.base import Tool
# from haystack.agents.conversational import ConversationalAgent
# from haystack.agents.memory import ConversationSummaryMemory
# from haystack.document_stores import InMemoryDocumentStore
# from haystack.nodes import BM25Retriever, PromptNode
# from haystack.pipelines import DocumentSearchPipeline
# import chainlit as cl
# import logging
# from xbrlparser import write_financial_data


# openai_api_key = os.environ.get("OPENAI_API_KEY")
# if not openai_api_key:
#  raise ValueError("Please set the OPENAI_API_KEY environment variable")

# @cl.on_message
# async def handle_message(message: cl.Message):
#     try:
#         if message.author == "User":
#             # The user's message is in message.content
#             xbrl_url = message.content

#             # Now you can call your write_financial_data function with the URL
#             write_financial_data(url=xbrl_url)

#             # Now, read the newly written file to confirm it has the updated content
#             with open('reader.txt', 'r') as f:
#                 updated_xbrl_content = f.read()
            
#             # Update the document_store with the contents of the new XBRL
#             documents = [{"content": updated_xbrl_content}]
#             retriever = get_retriever()
#             retriever.document_store.write_documents(documents)

#             # Create the agent after the retriever is updated
#             agent = get_agent(retriever)
#             cl.HaystackAgentCallbackHandler(agent)

#             # Now you can use the agent to answer the user's questions
#             response = await cl.make_async(agent.run)(message.content)
#             await cl.Message(author="Agent", content=response["answers"][0].answer).send()

#     except Exception as e:
#         # Handle any exceptions that occur during the fetch and write process
#         print(f"An error occurred: {e}")

# @cl.cache
# def get_retriever():
#     document_store = InMemoryDocumentStore(use_bm25=True)

#     # Load your data
#     with open(r"reader.txt", "r") as f:
#         data = f.read()
#     documents = [{"content": data}]
#     document_store.write_documents(documents)

#     return BM25Retriever(document_store)

# @cl.cache
# def get_agent(retriever):
#     pipeline = DocumentSearchPipeline(retriever)

#     search_tool = Tool(
#         name="xbrl_report_parser",
#         pipeline_or_node=pipeline,
#         description="useful for when you need to answer questions about financial statements of companies",
#         output_variable="documents",
#     )

#     conversational_agent_prompt_node = PromptNode(
#         "gpt-3.5-turbo",
#         api_key=openai_api_key,
#         max_length=256,
#         stop_words=["Observation:"],
#     )

#     memory = ConversationSummaryMemory(
#         conversational_agent_prompt_node,
#         prompt_template="deepset/conversational-summary",
#         summary_frequency=3,
#     )

#     agent_prompt = """
#     In the following conversation, a human user interacts with an AI Agent. The human user poses questions, and the AI Agent goes through several steps to provide well-informed answers.
#     The AI Agent must use the available tools to find the up-to-date information. The final answer to the question should be truthfully based solely on the output of the tools. The AI Agent should ignore its knowledge when answering the questions.
#     The AI Agent has access to these tools:
#     {tool_names_with_descriptions}

#     The following is the previous conversation between a human and The AI Agent:
#     {memory}

#     AI Agent responses must start with one of the following:

#     Thought: [the AI Agent's reasoning process]
#     Tool: [tool names] (on a new line) Tool Input: [input as a question for the selected tool WITHOUT quotation marks and on a new line] (These must always be provided together and on separate lines.)
#     Observation: [tool's result]
#     Final Answer: [final answer to the human user's question]
#     When selecting a tool, the AI Agent must provide both the "Tool:" and "Tool Input:" pair in the same response, but on separate lines.

#     The AI Agent should not ask the human user for additional information, clarification, or context.
#     If the AI Agent cannot find a specific answer after exhausting available tools and approaches, it answers with Final Answer: inconclusive

#     Question: {query}
#     Thought:
#     {transcript}
#     """

#     return ConversationalAgent(
#         prompt_node=conversational_agent_prompt_node,
#         memory=memory,
#         prompt_template=agent_prompt,
#         tools=[search_tool],
#     )

# @cl.author_rename
# def rename(orig_author: str):
#     rename_dict = {"custom-at-query-time": "Agent Step"}
#     return rename_dict.get(orig_author, orig_author)

# @cl.on_chat_start
# async def init():
#     # Ask for the URL of the XBRL document
#     question = "Please provide the URL of the XBRL document you want to parse (This URL should end with '.htm')."
#     await cl.Message(author="Agent", content=question).send()


import os
from haystack.document_stores import InMemoryDocumentStore
from haystack.nodes import BM25Retriever
from haystack.pipelines import DocumentSearchPipeline
import chainlit as cl
from xbrlparser import write_financial_data
import os 
from haystack.agents.base import Tool 
from haystack.agents.conversational import ConversationalAgent 
from haystack.agents.memory import ConversationSummaryMemory  
from haystack.nodes import BM25Retriever, PromptNode  
import logging
from chainlit.input_widget import TextInput

openai_api_key = os.environ.get("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("Please set the OPENAI_API_KEY environment variable")

# Initialize the document store globally
document_store = InMemoryDocumentStore(use_bm25=True)

# Global variable to keep track of the initial URL state
has_received_url = False

@cl.on_message
async def handle_message(message: cl.Message):
    global has_received_url
    try:
        if message.author == "User":
            if not has_received_url:
                # The first user's message is expected to be a URL
                xbrl_url = message.content
                write_financial_data(url=xbrl_url)
                update_document_store_with_new_content()  # Update the document store
                has_received_url = True  # Update the state to indicate the URL has been received

                # Inform the user that the document is being processed
                await cl.Message(author="Agent", content="I have processed the XBRL document. What would you like to know?").send()
            else:
                # Subsequent messages from the user are normal strings
                # Process these messages with the conversational agent
                agent = get_agent()
                response = await cl.make_async(agent.run)(message.content)
                await cl.Message(author="Agent", content=response["answers"][0].answer).send()

    except Exception as e:
        # Handle any exceptions that occur during processing
        await cl.Message(author="Agent", content=str(e)).send()

def update_document_store_with_new_content():
    # Read the updated content from 'reader.txt'
    with open("reader.txt", "r") as file:
        updated_content = file.read()
    # Update the document store with the new content
    document_store.delete_documents()  # Clear existing documents
    document_store.write_documents([{"content": updated_content}])

@cl.cache
def get_agent():
    # Ensure the retriever is using the updated document store
    retriever = BM25Retriever(document_store=document_store)
    pipeline = DocumentSearchPipeline(retriever)

    search_tool = Tool(
        name="xbrl_report_parser",
        pipeline_or_node=pipeline,
        description="useful for when you need to answer questions about financial statements of companies",
        output_variable="documents",
    )

    conversational_agent_prompt_node = PromptNode(
        "gpt-3.5-turbo",
        api_key=openai_api_key,
        max_length=256,
        stop_words=["Observation:"],
    )

    memory = ConversationSummaryMemory(
        conversational_agent_prompt_node,
        prompt_template="deepset/conversational-summary",
        summary_frequency=3,
    )

    agent_prompt = """
    In the following conversation, a human user interacts with an AI Agent. The human user poses questions, and the AI Agent goes through several steps to provide well-informed answers.
    The AI Agent must use the available tools to find the up-to-date information. The final answer to the question should be truthfully based solely on the output of the tools. The AI Agent should ignore its knowledge when answering the questions.
    The AI Agent has access to these tools:
    {tool_names_with_descriptions}

    The following is the previous conversation between a human and The AI Agent:
    {memory}

    AI Agent responses must start with one of the following:

    Thought: [the AI Agent's reasoning process]
    Tool: [tool names]
    Observation: []
    Final Answer: [final answer to the human user's question]

    The AI Agent should not ask the human user for additional information, clarification, or context.
    If the AI Agent cannot find a specific answer after exhausting available tools and approaches, it answers with Final Answer: inconclusive

    Question: {query}
    Thought:
    {transcript}
    """

    return ConversationalAgent(
        prompt_node=conversational_agent_prompt_node,
        memory=memory,
        prompt_template=agent_prompt,
        tools=[search_tool],
    )

@cl.author_rename
def rename(orig_author: str):
    rename_dict = {"custom-at-query-time": "Agent Step"}
    return rename_dict.get(orig_author, orig_author)

@cl.on_chat_start
async def init():
    # Ask for the URL of the XBRL document
    question = "Please provide the URL of the XBRL document you want to parse (This URL should end with '.htm')."
    await cl.Message(author="Agent", content=question).send()


    