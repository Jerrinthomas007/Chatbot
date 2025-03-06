from flask import Flask, request, jsonify, render_template
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import trim_messages
from typing import Sequence, Annotated, TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Set OpenAI API key
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# Initialize the chat model
model = ChatOpenAI(model="gpt-3.5-turbo")



class State(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    language: str

# Define the prompt template
prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are a helpful ai assistant for Zk techo. only answer questions about zk techo, for other question you can reply i dont have that infromation
            about zk techo :
            ZKTeco, established in March 1998, is a global leader in biometric verification technologies, specializing in fingerprint, face, finger vein, and iris recognition. The company's extensive product portfolio includes solutions for time attendance, access control, video surveillance, entrance control, and smart locks. 
ZKTECO

With a strong emphasis on research and development, ZKTeco boasts a team of nearly 1,000 R&D engineers. The company operates manufacturing facilities in Dongguan and maintains a significant presence in the United States, focusing on biometric verification and business operations. 
ZKTECO
 ZKTeco's global footprint extends to over 40 countries and territories, including Europe, the USA, Brazil, the Middle East, Indonesia, Mexico, Thailand, India, South Africa, and Argentina, employing more than 4,100 individuals worldwide. 
ZKTECO.EU

The company's mission is to share its advanced biometric technology to benefit businesses and individuals alike. ZKTeco's solutions cater to various sectors, such as public services, enterprise-level organizations, and personal users, aiming to enhance security and operational efficiency. 
ZKTECO.EU
 Notably, ZKTeco was ranked 14th globally in the "Top 50 Global Security Companies 2020" by a&s Magazine, reflecting its commitment to excellence and innovation in the security industry
            """,
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

# Define the trimmer for conversation history
trimmer = trim_messages(
    max_tokens=100,
    strategy="last",
    token_counter=model,
    include_system=True,
    allow_partial=False,
    start_on="human",
)

# Define the workflow
workflow = StateGraph(state_schema=State)

def call_model(state: State):
    trimmed_messages = trimmer.invoke(state["messages"])
    prompt = prompt_template.invoke(
        {"messages": trimmed_messages, "language": state["language"]}
    )
    response = model.invoke(prompt)
    return {"messages": [response]}

# Add the node to the workflow
workflow.add_node("model", call_model)

# Define the START node and connect it to the model node
workflow.set_entry_point("model")

# Define the END node and connect the model node to it
workflow.set_finish_point("model")

# Add memory management
memory = MemorySaver()
app_workflow = workflow.compile(checkpointer=memory)

# Initialize Flask app
app = Flask(__name__)

# Serve the frontend
@app.route("/")
def home():
    return render_template("index.html")

# Chatbot API endpoint
@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_input = data.get("message")
    thread_id = data.get("thread_id", "default_thread")  # Use a default thread ID if not provided
    language = data.get("language", "English")  # Default to English if not provided

    # Prepare input messages
    input_messages = [HumanMessage(content=user_input)]

    # Invoke the chatbot
    config = {"configurable": {"thread_id": thread_id}}
    output = app_workflow.invoke(
        {"messages": input_messages, "language": language},
        config,
    )

    # Return the chatbot's response
    return jsonify({"response": output["messages"][-1].content})

if __name__ == "__main__":
    app.run(debug=True)