import random
import time

from sqlalchemy import select
from telethon.errors import RPCError
from telethon.sync import TelegramClient,events
import asyncio
from datetime import datetime
from telethon.tl.types import User
from telethon.tl.types import UserStatusOnline, UserStatusOffline
from engine import create_db, session_maker
from models import Like
import pytz
import requests
from time import  sleep

async def on_sturtup():
    await create_db()
    print("bot online")
from telethon.tl.functions.account import UpdateStatusRequest

api_id = ""
api_hash = ''
my_id=""
my_id2=""

client = TelegramClient('session_name', api_id, api_hash)

auto_reply_message = "aaaaaa"

@client.on(events.NewMessage)
async def handler(event):

    if event.sender_id == my_id2:
        if not event.text.startswith(".likeme ") and event.text!=".showlike":

            user = await client.get_entity(my_id)
            if isinstance(user.status, UserStatusOnline):
                print(f"{user.username or user.id} 1")
            elif isinstance(user.status, UserStatusOffline):
                # print(f"{user.username or user.id} 0")

                ev=await event.reply(f"🖖Привет,я походу не в сети ❌🛜, но думаю скоро зайду.\nEсли срочно звони 📞.\n"
                                     f"\nМожешь оценить меня как собеседника(или друга) ❤️ если введешь команду <b>'.likeme (1-10)'.</b>\n"
                                     f"Или можешь посмотреть кто уже меня оценил 😊 если введешь команду <b>'.showlike'</b>.")
                # print(f"H{int(nh) - int(lh)}:M{int(nm) - int(lm)}")
                perc = 10

                while perc > 0:

                    try:
                        text = f"{ev.text}\nСообщение удалится через <b>{perc}</b> секунд"
                        await ev.edit(text,parse_mode='html')

                        perc -= 1


                        await asyncio.sleep(1)

                    except Exception as e:
                        print(f"An error occurred: {e}")
                        break
                await ev.delete()

            else:
                print(f"{user.username or user.id} NONE")
@client.on(events.NewMessage)
async def likeme(event):
    user = await client.get_entity(my_id)
    # if isinstance(user.status, UserStatusOffline):
    if ".likeme " in event.text:
        sender_id = event.sender_id
        sender = await client.get_entity(sender_id)
        username = sender.first_name
        print(username)
        try:
            like = int(event.text.split(".likeme ", maxsplit=1)[1])

            if like > 10:
                like = 10
            elif like<1:
                like=1
            print(like)
            async with session_maker() as session:
                stmt = select(Like).where(Like.username == username)
                result = await session.execute(stmt)
                data=result.scalars().all()
                # print(data)
                if data:
                    for i in data:
                        m=await event.reply(f"Ты уже оценил(а) меня на {i.value}")
                        sleep(1)
                        await m.delete()

                else:
                    print("false")
                    session.add(Like(username=username, value=like))
                    await session.commit()
                    m = await client.send_message(event.chat_id, "Спасибо 🤗")
                    await asyncio.sleep(0.5)
                    await m.delete()
        except ValueError:
            m=await client.send_message(event.chat_id,"Странное число у тебя 🤣,попробуй еще раз")
            sleep(3)
            await m.delete()

@client.on(events.NewMessage)
async def showlike(event):
    try:
        user = await client.get_entity(my_id)
        # if isinstance(user.status, UserStatusOnline):
        if ".showlike" in event.text:
            async with session_maker() as session:
                stmt = select(Like)
                result = await session.execute(stmt)
                data = result.scalars()
                masl=["💔","💔","🤎","🤎","💛","🧡","💙","💜","🩷","❤️"]
                en=""
                for i in data:
                    en+=f"👤 {i.username} {masl[i.value-1]} {i.value}\n"
                m=await client.send_message(event.chat_id,f"{en}")
                sleep(3)
                await m.delete()
                    # print(i)
                print(en)


    except Exception:
        print("oops")
        m = await client.send_message(event.chat_id, "Хмм...Никого нет,но ты можешь стать первым 🤗 <b>'.likeme (1-10)'</b>")
        sleep(3)
        await m.delete()

async def main():
    await on_sturtup()
    await client.start()
    await client.run_until_disconnected()
if __name__ == "__main__":

    asyncio.run(main())