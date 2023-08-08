from pygmalionai_chat_robot import PygmalionAIService

if __name__ == "__main__":
    chat_service = PygmalionAIService()
    resultA = chat_service.chat(role_name="Allie", you_name="alan", query="hi")
    print(resultA)

    resultB = chat_service.chat(role_name="Allie", you_name="alan", query="Who are you?")
    print(resultB)
