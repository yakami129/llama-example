from oobabooga_model_impl import Oobabooga

llm = Oobabooga()
#text = "Please tell a joke"
text = ''' 你是谁？
'''
print("chat:"+llm(text))

