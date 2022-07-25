import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vkkey import token
vktoken = vk_api.VkApi(token=token)
longpoll = VkBotLongPoll(vktoken, group_id=214697327)

def sendmsg():
    vktoken.method('messages.send', {'chat_id': 3, 'message': 'могу нахуй послать','random_id': 0})
    # chat_id 2- беседа с полей, 3- тест со мной, 4-будет следующая

print('вкл')
for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW:
        print(event.message.get('text'))
        print(event.chat_id)
        sendmsg()