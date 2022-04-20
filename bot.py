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
import bs4 as bs
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.proxy import *
from selenium.webdriver.firefox.options import Options
from pyvirtualdisplay import Display

scheduler = AsyncIOScheduler()

ADMINS = config.admins
ADMIN_CHANNEL = config.admin_channel


bot = Bot(token=config.bot_token, parse_mode="HTML")
storage = RedisStorage2('localhost', 6379, db=3)
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())


class BotStates(Helper):
    mode = HelperMode.snake_case
    ENTER_DOMAIN1 = ListItem()
    ENTER_DOMAIN2 = ListItem()
    ENTER_DOMAIN3 = ListItem()
    ENTER_PROXY = ListItem()


async def save_domain(message):
    state = dp.current_state(chat=message.chat.id, user=message.chat.id)
    await state.set_state(None)
    data = await storage.get_data(chat=0, user=0)

    proxy = Proxy({
        'proxyType': ProxyType.MANUAL,
        'httpProxy': data['proxy-url'],
        'sslProxy': data['proxy-url'],
        'noProxy': ''})

    try:
        options = Options()
        options.proxy = proxy

        display = Display(visible=0, size=(800, 800))
        display.start()

        browser = webdriver.Chrome(ChromeDriverManager().install())
        browser.get(message.text)
        sauce = browser.page_source
        browser.quit()
        soup = bs.BeautifulSoup(sauce, 'lxml')

        if soup.find("body", {"id": "trader-win24"}) is None and soup.find("body", {"id": "trader-winbir"}) is None:
            await bot.send_animation(chat_id=message.chat.id, caption="Oh No! ", animation=open('false.gif', 'rb'))
        else:
            await bot.send_animation(chat_id=message.chat.id, caption="Oh Yes!", animation=open('true.gif', 'rb'))
    except Exception as e:
        await bot.send_animation(chat_id=message.chat.id, caption="Oh No!", animation=open('false.gif', 'rb'))
        await bot.send_message(chat_id=config.admins[0], text="save domain error - {}".format(str(e)))
    await start_cmd(message)


async def proxy_checker():
    data = await storage.get_data(chat=0, user=0)

    try:
        sess = requests.Session()

        proxies = {
            'http': data['proxy-url'],
        }

        a = sess.get('http://google.com', proxies=proxies).status_code
    except Exception as e:
        await bot.send_message(chat_id=ADMIN_CHANNEL, text="Proxy down, please update")
        await bot.send_message(config.admins[0], "proxy checker error - {}".format(str(e)))


async def domain_checker():
    try:
        data = await storage.get_data(chat=0, user=0)

        proxy = Proxy({
            'proxyType': ProxyType.MANUAL,
            'httpProxy': data['proxy-url'],
            'sslProxy': data['proxy-url'],
            'noProxy': ''})

        options = Options()
        options.proxy = proxy

        display = Display(visible=0, size=(800, 800))
        display.start()

        browser = webdriver.Chrome(ChromeDriverManager().install())

        if 'url1' in data.keys():
            try:
                # proxy = Proxy({
                #     'proxyType': ProxyType.MANUAL,
                #     'httpProxy': data['proxy-url'],
                #     'sslProxy': data['proxy-url'],
                #     'noProxy': ''})
                #
                # options = Options()
                # options.proxy = proxy
                #
                # display = Display(visible=0, size=(800, 800))
                # display.start()
                #
                # browser = webdriver.Chrome(ChromeDriverManager().install())
                browser.get(data['url1'])
                sauce = browser.page_source
                # browser.quit()
                soup = bs.BeautifulSoup(sauce, 'lxml')

                if soup.find("body", {"id": "trader-win24"}) is None and soup.find("body", {"id": "trader-winbir"}) is None:
                    await bot.send_animation(chat_id=ADMIN_CHANNEL, caption="Oh No! {}".format(data['url1']),
                                             animation=open('false.gif', 'rb'))
                else:
                    await bot.send_message(config.admins[0], "url1 works")
            except Exception as e:
                with open('logs.txt' 'a') as f:
                    f.write(str(e) + "\n\n")
                await bot.send_animation(chat_id=ADMIN_CHANNEL, caption="Oh No! {}".format(data['url1']),
                                         animation=open('false.gif', 'rb'))
                await bot.send_message(config.admins[0], "url1 error - {}".format(str(e)))
        if 'url2' in data.keys():
            try:
                # proxy = Proxy({
                #     'proxyType': ProxyType.MANUAL,
                #     'httpProxy': data['proxy-url'],
                #     'sslProxy': data['proxy-url'],
                #     'noProxy': ''})
                #
                # options = Options()
                # options.proxy = proxy
                #
                # display = Display(visible=0, size=(800, 800))
                # display.start()
                #
                # browser = webdriver.Chrome(ChromeDriverManager().install())
                browser.get(data['url2'])
                sauce = browser.page_source
                # browser.quit()
                soup = bs.BeautifulSoup(sauce, 'lxml')

                if soup.find("body", {"id": "trader-win24"}) is None and soup.find("body", {"id": "trader-winbir"}) is None:
                    await bot.send_animation(chat_id=ADMIN_CHANNEL, caption="Oh No! {}".format(data['url2']),
                                             animation=open('false.gif', 'rb'))
                else:
                    await bot.send_message(config.admins[0], "url2 works")
            except Exception as e:
                with open('logs.txt' 'a') as f:
                    f.write(str(e) + "\n\n")
                await bot.send_animation(chat_id=ADMIN_CHANNEL, caption="Oh No! {}".format(data['url2']),
                                         animation=open('false.gif', 'rb'))
                await bot.send_message(config.admins[0], "url2 error - {}".format(str(e)))
        if 'url3' in data.keys():
            try:
                # proxy = Proxy({
                #     'proxyType': ProxyType.MANUAL,
                #     'httpProxy': data['proxy-url'],
                #     'sslProxy': data['proxy-url'],
                #     'noProxy': ''})
                #
                # options = Options()
                # options.proxy = proxy
                #
                # display = Display(visible=0, size=(800, 800))
                # display.start()
                #
                # browser = webdriver.Chrome(ChromeDriverManager().install())
                browser.get(data['url3'])
                sauce = browser.page_source
                # browser.quit()
                soup = bs.BeautifulSoup(sauce, 'lxml')

                if soup.find("body", {"id": "trader-win24"}) is None and soup.find("body", {"id": "trader-winbir"}) is None:
                    await bot.send_animation(chat_id=ADMIN_CHANNEL, caption="Oh No! {}".format(data['url3']),
                                             animation=open('false.gif', 'rb'))
                else:
                    await bot.send_message(config.admins[0], "url3 works")

            except Exception as e:
                with open('logs.txt' 'a') as f:
                    f.write(str(e) + "\n\n")
                await bot.send_animation(chat_id=ADMIN_CHANNEL, caption="Oh No! {}".format(data['url3']),
                                         animation=open('false.gif', 'rb'))
                await bot.send_message(config.admins[0], "url3 error - {}".format(str(e)))
        browser.quit()
    except Exception as e:
        with open('logs.txt' 'a') as f:
            f.write(str(e) + "main\n\n")


@dp.message_handler(chat_id=ADMINS, commands=['start'], state="*", chat_type='private')
async def start_cmd(message: Message):
    if message.chat.id in ADMINS:
        state = dp.current_state(chat=message.chat.id, user=message.chat.id)
        await state.set_state(None)
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(text="Add New 24Win Link", callback_data="add#1"))
        markup.add(types.InlineKeyboardButton(text="Add New Winb1r Link", callback_data="add#2"))
        # markup.add(types.InlineKeyboardButton(text="Add New Website#3 Link", callback_data="add#3"))
        markup.add(types.InlineKeyboardButton(text="Add New Proxy Link", callback_data="add-proxy#"))

        data = await storage.get_data(chat=0, user=0)
        url1 = data['url1'] if 'url1' in data.keys() else '-'
        url2 = data['url2'] if 'url2' in data.keys() else '-'
        url3 = data['url3'] if 'url3' in data.keys() else '-'
        proxy_url = data['proxy-url'] if 'proxy-url' in data.keys() else '-'
        await message.answer("24Win URL: {}\nWinb1r URL: {}\nProxy URL: {}\n".format(url1,
                             url2, proxy_url), reply_markup=markup)


@dp.callback_query_handler(lambda c: c.data.startswith('add#'), state="*", chat_type='private')
async def add_link_callback(call: types.CallbackQuery):
    state = dp.current_state(chat=call.message.chat.id, user=call.message.chat.id)

    url_nmb = int(call.data.replace('add#', ''))
    text = "Please enter new link for the website#{}:".format(url_nmb)

    if url_nmb == 1:
        await state.set_state(BotStates.ENTER_DOMAIN1[0])
    elif url_nmb == 2:
        await state.set_state(BotStates.ENTER_DOMAIN2[0])
    else:
        await state.set_state(BotStates.ENTER_DOMAIN3[0])
    await call.message.answer(text)
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
        sess.get('http://google.com', proxies=proxies).status_code
        await message.answer("Saved")
        await start_cmd(message)
    except Exception as e:
        await message.answer("Wrong proxy url please try again:")


@dp.message_handler(chat_id=ADMINS, state=BotStates.ENTER_DOMAIN1[0], chat_type='private')
async def message_checker1(message: Message):
    await storage.update_data(chat=0, user=0, data={"url1": message.text})
    await save_domain(message)


@dp.message_handler(chat_id=ADMINS, state=BotStates.ENTER_DOMAIN2[0], chat_type='private')
async def message_checker2(message: Message):
    await storage.update_data(chat=0, user=0, data={"url2": message.text})
    await save_domain(message)


@dp.message_handler(chat_id=ADMINS, state=BotStates.ENTER_DOMAIN3[0], chat_type='private')
async def message_checker3(message: Message):
    await storage.update_data(chat=0, user=0, data={"url3": message.text})
    await save_domain(message)


async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


if __name__ == '__main__':
    scheduler.start()
    jobstore = RedisJobStore(jobs_key='r-payments.jobs', run_times_key='r-prod.run_times')
    scheduler.add_jobstore(jobstore, alias='redis')
    scheduler.remove_all_jobs()
    scheduler.add_job(domain_checker, "interval", minutes=2, jobstore='redis')
    # scheduler.add_job(proxy_checker, "interval", minutes=2, jobstore='redis')
    executor.start_polling(dp, on_shutdown=shutdown)
