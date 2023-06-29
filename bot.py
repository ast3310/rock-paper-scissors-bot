import telebot
from telebot import types
from jinja2 import Environment, PackageLoader, select_autoescape

from config import TelegramConfig

bot=telebot.TeleBot(TelegramConfig.TOKEN)

template_env = Environment(
    loader=PackageLoader("bot", "templates"),
    autoescape=select_autoescape()
)
