import os
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from dotenv import load_dotenv
from llama2_model_impl import Llama2

## 初始化操作
load_dotenv()  # 读取 .env 文件
LLAMA2_PATH = os.getenv("LLAMA2_PATH")

## 初始化llm模型和工具
llm = Llama2(model_name_or_path=LLAMA2_PATH,bit4=False)
tools = load_tools(["serpapi","llm-math"],llm=llm)

## 初始化Agent
agent = initialize_agent(tools=tools,llm=llm,agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,verbose=True)

## 执行Agent
agent.run("How is the current development of big language models? Which company is doing well?")
#agent.run("目前大语言模型的发展情况如何？哪家公司做得好？用中文回复")

