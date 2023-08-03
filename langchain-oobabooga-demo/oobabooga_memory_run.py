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

outputA = llm_chain.predict(human_input="你好")
print(outputA)

outputB = llm_chain.predict(human_input="现在美国总统是谁？")
print(outputB)

outputC = llm_chain.predict(human_input="AI产品的发展前景怎么样？")
print(outputC)