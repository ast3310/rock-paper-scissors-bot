from bot import bot, template_env
import datetime
from models import Game
from telebot import types
import re

from helpers import in_game_middleware


@bot.message_handler(commands=['game'])
@in_game_middleware
def welcome_player(message, game):
    template = template_env.get_template('welcome_ru.html')
    if game is None:
        msg = bot.send_message(message.chat.id, template.render(
                    new_game=True,
                    user_name=message.from_user.first_name,
                ), parse_mode='HTML',)
        
        bot.register_next_step_handler(msg, set_second_player, message.from_user.id)
    else:
        bot.send_message(message.chat.id, template.render(
                    new_game=False,
                    user_name=message.from_user.first_name,
                ), parse_mode='HTML',)


def set_second_player(message, user_id):
    has_mention = False
    username = None
    user = None

    if message.from_user.id != user_id:
        bot.register_next_step_handler(message, set_second_player, user_id)
        return

    if message.entities is not None:
        for entity in message.entities:
            if entity.type == 'mention':
                has_mention = True
                username = re.findall(r'^@[A-Za-z0-9]+|.+ @[A-Za-z0-9]+', message.text)[0][1:]
                break
            elif entity.type == 'text_mention':
                has_mention = True
                user = entity.user
                break
    
    template = template_env.get_template('set_mention_player_ru.html')
    
    if has_mention:
        markup = types.InlineKeyboardMarkup()

        user_ = user.id if username is None else username
        
        markup.add(
            types.InlineKeyboardButton("Я готов", 
                                       callback_data=f'imready_{user_id}_{message.from_user.first_name}_{user_}')
        )

        bot.send_message(chat_id=message.chat.id,
            text=template.render(
                sucsess=True,
                user_name=message.from_user.first_name,
            ), parse_mode='HTML', reply_markup=markup)
    else:
        msg = bot.send_message(chat_id=message.chat.id,
            text=template.render(
                sucsess=False,
                user_name=message.from_user.first_name,
            ), parse_mode='HTML')
        bot.register_next_step_handler(msg, set_second_player, user_id)


@bot.callback_query_handler(func=lambda call: call.data.startswith('imready'))
def find_player(event):
    first_player = int(event.data.split('_')[1])
    first_player_name = event.data.split('_')[2]
    username = event.data.split('_')[3]

    if event.from_user.username == username \
        or str(event.from_user.id) == username:
        start_game(event, first_player, first_player_name)
    else:
        bot.answer_callback_query(callback_query_id=event.id, show_alert=False,
                text="Вы не тот человек")


@in_game_middleware
def start_game(event, game, first_player, first_player_name):
    template = template_env.get_template('start_game_ru.html')

    if game is None:
        new_game = Game(chat_id=event.message.chat.id, 
                        first_player=first_player,
                        first_player_name=first_player_name,
                        second_player=event.from_user.id,
                        second_player_name=event.from_user.first_name,
                        join_date=datetime.date.today())
        new_game.save()

        markup = types.InlineKeyboardMarkup()
        item1 = types.InlineKeyboardButton("Камень", callback_data='rock')
        item2 = types.InlineKeyboardButton("Ножницы", callback_data='scissors')
        item3 = types.InlineKeyboardButton("Бумага", callback_data='paper')
        item4 = types.InlineKeyboardButton("Закончить игру", callback_data='cancel_game')
 
        markup.add(item1, item2, item3)
        markup.add(item4)

        bot.send_message(chat_id=event.message.chat.id,
            text=template.render(
                new_game=True,
                user_name=event.from_user.first_name,
            ), parse_mode='HTML', reply_markup=markup)
