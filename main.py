import datetime
from dotenv import load_dotenv
import os
from vkbottle.bot import Bot, Message
import pygsheets

load_dotenv()
client = pygsheets.authorize(os.environ['google_key_path'])
sheet = client.open("Bot_data")
list1 = sheet[0]
bot = Bot(os.environ['vk_api_key'])


@bot.on.private_message()
async def any_message(message: Message):
    if message.text.lower() in ('привет', 'хай', 'ку', 'хеллоу', 'hi', 'hello'):
        await message.answer("Даров, как дела?")
        return
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
    await message.answer("Ясно, а щас как дела?")

bot.run_forever()
