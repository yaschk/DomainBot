from aiogram.types import Message
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.utils.helper import Helper, HelperMode, ListItem
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.redis import RedisJobStore
import requests
import config

scheduler = AsyncIOScheduler()

ADMINS = config.admins
ADMIN_CHANNEL = config.admin_channel


bot = Bot(token=config.bot_token, parse_mode="HTML")
storage = RedisStorage2('localhost', 6379, db=3)
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())


class BotStates(Helper):
    mode = HelperMode.snake_case
    ENTER_DOMAIN = ListItem()
    ENTER_PROXY = ListItem()


async def proxy_checker():
    data = await storage.get_data(chat=0, user=0)

    try:
        sess = requests.Session()

        proxies = {
            'http': data['proxy-url'],
        }

        sess.get('google.com', proxies=proxies).status_code
    except Exception as e:
        await bot.send_message(chat_id=ADMIN_CHANNEL, text="Proxy down, please update {}".format(str(e)))


# async def domain_checker():
#     data = await storage.get_data(chat=0, user=0)
#     try:
#         sess = requests.Session()
#
#         proxies = {
#             'http': data['proxy-url'],
#         }
#
#         ans = sess.get(data['url'], proxies=proxies).status_code
#         if ans != 200:
#             await bot.send_animation(chat_id=ADMIN_CHANNEL, caption="Oh No!", animation=open('false.gif', 'rb'))
#     except:
#         await bot.send_animation(chat_id=ADMIN_CHANNEL, caption="Oh No!", animation=open('false.gif', 'rb'))


@dp.message_handler(chat_id=ADMINS, commands=['start'], state="*", chat_type='private')
async def start_cmd(message: Message):
    if message.chat.id in ADMINS:
        state = dp.current_state(chat=message.chat.id, user=message.chat.id)
        await state.set_state(None)
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(text="Add New Website#1 Link", callback_data="add#1"))
        markup.add(types.InlineKeyboardButton(text="Add New Website#2 Link", callback_data="add#2"))
        markup.add(types.InlineKeyboardButton(text="Add New Website#3 Link", callback_data="add#3"))
        markup.add(types.InlineKeyboardButton(text="Add New Proxy Link", callback_data="add-proxy#"))

        data = await storage.get_data(chat=0, user=0)
        url1 = data['url1'] if 'url1' in data.keys() else '-'
        url2 = data['url2'] if 'url2' in data.keys() else '-'
        url3 = data['url3'] if 'url3' in data.keys() else '-'
        proxy_url = data['proxy-url'] if 'proxy-url' in data.keys() else '-'
        await message.answer("Website#1 URL: {}\nWebsite#2 URL: {}\nWebsite#2 URL: {}\nProxy URL: {}\n".format(url1,
                             url2, url3, proxy_url), reply_markup=markup)


@dp.callback_query_handler(lambda c: c.data == 'add#', state="*", chat_type='private')
async def add_link_callback(call: types.CallbackQuery):
    state = dp.current_state(chat=call.message.chat.id, user=call.message.chat.id)
    await state.set_state(BotStates.ENTER_DOMAIN[0])
    await call.message.answer("Please enter new link:")
    markup = types.InlineKeyboardMarkup()
    await call.message.edit_reply_markup(reply_markup=markup)


@dp.callback_query_handler(lambda c: c.data == 'add-proxy#', state="*", chat_type='private')
async def add_proxy_link_callback(call: types.CallbackQuery):
    state = dp.current_state(chat=call.message.chat.id, user=call.message.chat.id)
    await state.set_state(BotStates.ENTER_PROXY[0])
    await call.message.answer("Please enter new proxy link:")
    markup = types.InlineKeyboardMarkup()
    await call.message.edit_reply_markup(reply_markup=markup)


@dp.message_handler(chat_id=ADMINS, state=BotStates.ENTER_PROXY[0], chat_type='private')
async def proxy_message_checker(message: Message):
    await storage.update_data(chat=0, user=0, data={"proxy-url": message.text})
    data = await storage.get_data(chat=0, user=0)
    proxies = {
        'http': data['proxy-url'],
    }
    try:
        sess = requests.Session()
        sess.get(data['url'], proxies=proxies).status_code
        await message.answer("Saved")
    except Exception as e:
        await message.answer("Wrong proxy url please try again: {}".format(str(e)))


@dp.message_handler(chat_id=ADMINS, state=BotStates.ENTER_DOMAIN[0], chat_type='private')
async def message_checker(message: Message):
    await storage.update_data(chat=0, user=0, data={"url": message.text})
    state = dp.current_state(chat=message.chat.id, user=message.chat.id)
    await state.set_state(None)
    data = await storage.get_data(chat=0, user=0)

    proxies = {
        'http': data['proxy-url'],
    }

    try:

        sess = requests.Session()

        ans = sess.get(message.text, proxies=proxies).status_code
        if ans != 200:
            await bot.send_animation(chat_id=message.chat.id, caption="Oh No!", animation=open('false.gif', 'rb'))
        else:
            await bot.send_animation(chat_id=message.chat.id, caption="Oh Yes!", animation=open('true.gif', 'rb'))
    except:
        await bot.send_animation(chat_id=ADMIN_CHANNEL, caption="Oh No!", animation=open('false.gif', 'rb'))


async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


if __name__ == '__main__':
    scheduler.start()
    jobstore = RedisJobStore(jobs_key='r-payments.jobs', run_times_key='r-prod.run_times')
    scheduler.add_jobstore(jobstore, alias='redis')
    scheduler.remove_all_jobs()
    #scheduler.add_job(domain_checker, "interval", seconds=30, jobstore='redis')
    scheduler.add_job(proxy_checker, "interval", seconds=30, jobstore='redis')
    executor.start_polling(dp, on_shutdown=shutdown)
