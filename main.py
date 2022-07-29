import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api import VkUpload
from vkkey import token
import datetime
from PIL import Image, ImageFont, ImageDraw
import sqlite3
import re
import traceback
from random import randint
from time import sleep

vktoken = vk_api.VkApi(token=token)
image = 'png\\pictosend.png'
longpoll = VkBotLongPoll(vktoken, group_id=214697327)
upload = VkUpload(vktoken)
upload_image = upload.photo_messages(photos=image)[0]



def sendmsg():
    vktoken.method('messages.send', {'chat_id': 4, 'message': 'вы тоже все пошли нахуй', 'random_id': 0})
    # chat_id 2- беседа с полей, 3- тест со мной, 4-будет следующая

def sendpic(lastrec):
    with sqlite3.connect('halatnaya.db') as db:
        cursor = db.cursor()
        cursor.execute('SELECT date, description FROM halaty')
        halat = cursor.fetchall()[-1]
        print(halat)
    days = datetime.date.today() - datetime.date(int(halat[0].split('-')[2]), int(halat[0].split('-')[1]),
                                                 int(halat[0].split('-')[0]))
    days = re.findall(r"\d+", str(days))[0]
    oldint = int(days)-1
    imege = Image.open('png\\baza.png')
    if oldint > 9:
        fofont = ImageFont.truetype('png\\17900.ttf', 75)
    else:
        fofont = ImageFont.truetype('png\\17900.ttf', 120)
    immage = ImageDraw.Draw(imege)
    immage.text((1143, 270), str(lastrec), font=fofont, fill=(0, 0, 0, 255), anchor='mm')
    immage.text((1110, 460), str(oldint), font=fofont, fill=(0, 0, 0, 255), anchor='mm')
    imege.save('png\\pictosend.png')
    vktoken.method('messages.send',
                   {'chat_id': 3,
                    'message': f'Ура, теперь дней без проёбов целых:{oldint}\nПоследним проёбом было: "{halat[1]}".',
                    'random_id': 0, 'attachment': ','.join(attachments)})



with sqlite3.connect('halatnaya.db') as db:
    cursor = db.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS halaty(
    description TEXT,
    date TEXT
    )""")
    db.commit()


print('вкл')
for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW:
        print(event.message)
        print(event.message.get('text'))
        attachments = []
        attachments.append('photo{}_{}'.format(upload_image['owner_id'], upload_image['id']))
        if event.message.get('from_id') == 156367896 and event.message.get('text') == 'S g d': # если сообщение от полины 188166794
            print('Я затригерился')
            sleep(randint(60, 600))
            with sqlite3.connect('halatnaya.db') as db:
                cursor = db.cursor()
                cursor.execute('SELECT lastmsgdate FROM important')
                lastdate = cursor.fetchone()[0].split('-')
                cursor.execute('SELECT lastrec FROM important')
                lastrec = cursor.fetchone()[0]
            raznica = datetime.date.today() - datetime.date(int(lastdate[2]), int(lastdate[1]), int(lastdate[0]))
            if raznica != 0 and datetime.datetime.now().time()>datetime.time(9,00,00,0):
                sendpic(lastrec)

if __name__ == '__main__':
    print('чето работает')
    input('Нажмите Enter для выхода\n')
