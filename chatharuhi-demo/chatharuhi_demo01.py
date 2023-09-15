from chatharuhi import ChatHaruhi
from dotenv import load_dotenv

load_dotenv();

db_folder = 'characters/yuqian/content/yuqian'
system_prompt = 'characters/yuqian/content/system_prompt.txt'

chatbot = ChatHaruhi( system_prompt = system_prompt,\
                      llm = 'openai' ,\
                      story_db = db_folder)

response = chatbot.chat(role='yakami', text = '于老师, 我好累啊')
print(response)

response = chatbot.chat(role='yakami', text = '于老师, 我什么都不想做')
print(response)

response = chatbot.chat(role='yakami', text = '于老师, 你知道我谁吗？')
print(response)