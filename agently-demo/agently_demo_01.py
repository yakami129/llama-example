import Agently
worker = Agently.create_worker()
worker\
.set_llm_name("GPT")\
.set_llm_auth("GPT", "sk-JSZQ")\
.set_proxy("http://127.0.0.1:23457")
result = worker\
.input("Give me 5 words and 1 sentence.")\
    .output({
        "words": ("Array",),
        "sentence": ("String",),
    })\
    .start()
print(result)
print(result["words"][2])