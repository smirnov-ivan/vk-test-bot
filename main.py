import datetime
from dotenv import load_dotenv
import os
from vkbottle import BaseStateGroup
from vkbottle.bot import Bot, Message
import pygsheets

load_dotenv()
client = pygsheets.authorize(os.environ['google_key_path'])
sheet = client.open("Bot_data")
list1 = sheet[0]
bot = Bot(os.environ['vk_api_key'])


class HAYState(BaseStateGroup):
    ANSWERING = 0


@bot.on.private_message(lev="/askme")
async def askme_handle(message: Message):
    await bot.state_dispenser.set(message.peer_id, HAYState.ANSWERING)
    return "ну давай пожалуйся мне"


@bot.on.private_message(state=HAYState.ANSWERING)
async def askme_continue_handler(message: Message):
    user = await message.get_user()
    try:
        list1.append_table((
            message.from_id,
            user.first_name + " " + user.last_name,
            datetime.datetime.now().strftime("%I:%M%p %b %d, %Y"),
            message.text
        ))
    except Exception as e:
        print(e)

    await bot.state_dispenser.delete(message.peer_id)
    return 'я тебя услышал и мне похуй.'


@bot.on.private_message()
async def any_message(message: Message):
    return "Введи команду блять. Например: /askme"

bot.run_forever()
