import os

from dotenv import load_dotenv
from langchain import LLMChain, PromptTemplate
from llama2_model_impl import Llama2

load_dotenv();
LLAMA2_PATH = os.getenv("LLAMA2_PATH")

## 初始化Llama2模型和prompt的模板
llm = Llama2(model_name_or_path=LLAMA2_PATH,bit4=False)
prompt = PromptTemplate(
    input_variables=["product"],
    template="What is a good name for a company that makes {product}?"
)

## 创建一个langchain链
chain = LLMChain(llm=llm,prompt=prompt)

## 执行langchain链
str = chain.run("AI software company")
print(str)
