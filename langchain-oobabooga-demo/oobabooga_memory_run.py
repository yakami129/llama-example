from langchain import LLMChain, PromptTemplate
from langchain.prompts import(
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate
)
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from oobabooga_model_impl import Oobabooga

template = """
Human: {human_input}
"""

prompt = PromptTemplate(
    input_variables=["human_input"], template=template
)
memory = ConversationBufferMemory(memory_key="chat_history")
llm = Oobabooga()
llm_chain = LLMChain(
    llm=llm,
    prompt=prompt,
    verbose=True,
    memory=memory,
)

outputA = llm_chain.predict(human_input="上海位于哪个位置？")
print(outputA)

outputB = llm_chain.predict(human_input="它有什么旅游景点？")
print(outputB)