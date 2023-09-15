
import openai
import os
from dotenv import load_dotenv

load_dotenv()  # 读取 .env 文件

# 设置您的 OpenAI API 密钥
openai.api_key = os.environ.get("OPENAI_API_KEY")


class UserEntityExtraction():

    input_prompt = """
    You are now a professional NLP engineer, you need to extract important entities and relationships from the conversations I provided, here are the entities and relationships I defined, please think step by step
    ```
    ## user_node: Extract user information from conversations
    - name: The username you extracted,
    - tags: Extracted user attribute name, user numeric value
    This is my conversation
    ```
    {input}
    ```
    """

    output_prompt = """
    Please do not output the inference process, just output the result.
    Please output the result in Chinese and json format,Format as follows :
    ```
    {
        "user_node": [{
            "name": "The username you extracted",
            "tags": [{"User property name":"User property value"}]
        }]
    }
    ```
    """

    def extraction(self, text: str) -> str:
        prompt = self.input_prompt.format(input=text) + self.output_prompt
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[
                {'role': 'user', 'content': prompt}
            ],
            temperature=0,
        )
        return response["choices"][0]["message"]["content"]


class EventEntityExtraction():

    input_prompt = """
    You are now a professional NLP engineer, you need to extract important entities and relationships from the conversations I provided, here are the entities and relationships I defined, please think step by step
    ```
    ## event_node: Extract ideas, trivia, questions, and key information from the conversation
    - "name": "The event name you extracted,
    - "time": "The time when the event you extracted occurred, if not set to empty string",
    - "location": "You extract where the event occurred, if no empty string is used",
    - "description": "The text description of the event you extracted, if not set to the null character"
    This is my conversation
    ```
    {input}
    ```
    """

    output_prompt = """
    Please do not output the inference process, just output the result.
    Please output the result in Chinese and json format,Format as follows :
    ```
    {
        "event_node": []
    }
    ```
    """

    def extraction(self, text: str) -> str:
        prompt = self.input_prompt.format(input=text) + self.output_prompt
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[
                {'role': 'user', 'content': prompt}
            ],
            temperature=0,
        )
        return response["choices"][0]["message"]["content"]


class InterestEntityExtraction():

    input_prompt = """
    You are now a professional NLP engineer, you need to extract important entities and relationships from the conversations I provided, here are the entities and relationships I defined, please think step by step
    ```
    ## interest_node: Extract hobbies from the conversation
    - "name": "Name of interest you extracted",
    - "type": "The type of interest you extract, such as entertainment, sports, etc",
    This is my conversation
    ```
    {input}
    ```
    """

    output_prompt = """
    Please do not output the inference process, just output the result.
    Please output the result in Chinese and json format,Format as follows :
    ```
    {
        "interest_node": []
    }
    ```
    """

    def extraction(self, text: str) -> str:
        prompt = self.input_prompt.format(input=text) + self.output_prompt
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[
                {'role': 'user', 'content': prompt}
            ],
            temperature=0,
        )
        return response["choices"][0]["message"]["content"]


class EntityRelationshipAnalysis():

    input_prompt = """
    You are now a professional NLP engineer, you need to reason about the relationship between entities based on the dialogue and entities I provided, please think step by step
    Here are some important relationship notes:
    ```
    # participate_events: Identify customer engagement events
    # interested_interest: Identify what users are interested in
    # unInterested_interest: Determine what users are not interested in
    ```
    This is my conversation:
    ```
    {chat_histroy}
    ```
    This is my Entity:
    ```
    {entity_json}
    ```
    """

    output_prompt = """
    Please do not output the inference process, just output the result.
    Please output the result in Chinese and json format,Format as follows :
    ```
    {
        "participate_events": [{
            "user_name": "",
            "event_name": ""
        }],
        "interested_interest": [{
            "user_name": "",
            "interest_name": ""
        }],
        "un_interested_interest": [{
            "user_name": "",
            "interest_name": ""
        }]
    }
    """

    def extraction(self, chat_histroy: str, entity_json: str) -> str:
        prompt = self.input_prompt.format(chat_histroy=chat_histroy,entity_json=entity_json) + self.output_prompt
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[
                {'role': 'user', 'content': prompt}
            ],
            temperature=0,
        )
        return response["choices"][0]["message"]["content"]


if __name__ == "__main__":

    chat_histroy = """
    阿虚:「今天在计算机课上老师教了我写Python!」
    ---
    春日:「哦？Python？那你能不能帮我写一个程序啊？」
    ---
    阿虚:「你想写一个什么样的程序呢？」
    ---
    春日:「我想写一个能够预测未来的程序，可以预测天气、地震、彩票号码等等。」
    ---
    阿虚:「如果有一个能预测彩票的程序，我们岂不是能赚很多钱？」
    ---
    春日:「没错！这就是我的计划！我们可以用赚来的钱来支持SOS团的活动，甚至可以扩大我们的影响力！」
    ---
    阿虚:「我不太喜欢看电影」
    ---
    春日:「我也是，我不喜欢出门，喜欢宅在家里」
    ---
    阿虚:「我快过生日了，我的是生日是1月29日」
    ---
    春日:「哈哈，我的生日是1月20日呢」
    """

    user_entity_extraction = UserEntityExtraction()
    user_result = user_entity_extraction.extraction(text=chat_histroy)
    event_entity_extraction = EventEntityExtraction()
    event_result = event_entity_extraction.extraction(text=chat_histroy)
    interest_entity_extraction = InterestEntityExtraction()
    interest_result = interest_entity_extraction.extraction(text=chat_histroy)
    print("user_result:", user_result)
    print("event_result:", event_result)
    print("interest_result:", interest_result)
    erpa = EntityRelationshipAnalysis();
    result = erpa.extraction(chat_histroy=chat_histroy,entity_json=user_result+event_result+interest_result)
    print("result:", result)

