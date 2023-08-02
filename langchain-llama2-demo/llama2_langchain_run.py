import os

from dotenv import load_dotenv
from llama2_model_impl import Llama2

load_dotenv()  # 读取 .env 文件
LLAMA2_PATH = os.getenv("LLAMA2_PATH")

llm = Llama2(model_name_or_path=LLAMA2_PATH,bit4=False)
text = "Please tell a joke"
print("chat:"+llm(text))

