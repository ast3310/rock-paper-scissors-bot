from bot import bot, template_env
import datetime
from models import Game
from telebot import types

from helpers import in_game_middleware, Player, get_player_by_id, Move


def first_is_winner(first_player_move, second_player_move):
    if first_player_move == second_player_move:
        return False
    
    FIRST_COND = [
        first_player_move == Move.ROCK.value and \
        second_player_move == Move.SCISSORS.value,

        first_player_move == Move.SCISSORS.value and \
        second_player_move == Move.PAPER.value,

        first_player_move == Move.PAPER.value and \
        second_player_move == Move.ROCK.value,
    ]

    return any(FIRST_COND)


@bot.callback_query_handler(func=lambda call: call.data in ['rock', 'scissors', 'paper'])
@in_game_middleware
def player_move(event, game):
    if game is not None:
        player, user_id = get_player_by_id(game, event.from_user.id)
        if player is None:
            bot.answer_callback_query(callback_query_id=event.id, show_alert=False,
                text="Вы не тот человек")
        else:
            bot.answer_callback_query(callback_query_id=event.id, show_alert=False,
                text="Ваш ход принят")
            
            template = template_env.get_template('move_notify_ru.html')
            
            bot.send_message(chat_id=event.message.chat.id,
                text=template.render(
                    user_name=event.from_user.first_name,
                ), parse_mode='HTML')

        if player == Player.FIRST and (not game.first_player_move):
            game.first_player_move = event.data
        elif player == Player.SECOND and (not game.second_player_move):
            game.second_player_move = event.data

        if game.first_player_move and game.second_player_move:
            template = template_env.get_template('winner_notify_ru.html')
        
            if first_is_winner(game.first_player_move, game.second_player_move):
                bot.send_message(chat_id=event.message.chat.id,
                    text=template.render(
                        is_draw=False,
                        winner_name=game.first_player_name,
                    ), parse_mode='HTML')
                
                game.first_player_score += 1
            
            elif first_is_winner(game.second_player_move, game.first_player_move):
                bot.send_message(chat_id=event.message.chat.id,
                    text=template.render(
                        is_draw=False,
                        winner_name=game.second_player_name,
                    ), parse_mode='HTML')
                
                game.second_player_score += 1
            else:
                bot.send_message(chat_id=event.message.chat.id,
                    text=template.render(
                        is_draw=True,
                    ), parse_mode='HTML')
                
                game.first_player_score += 1
                game.second_player_score += 1
            
            game.first_player_move = None
            game.second_player_move = None
        
        game.save()


@bot.callback_query_handler(func=lambda call: call.data == 'cancel_game')
@in_game_middleware
def end_game(event, game):
    if game is not None:
        player, user_id = get_player_by_id(game, event.from_user.id)
        if player is None:
            bot.answer_callback_query(callback_query_id=event.id, show_alert=False,
                text="Вы не тот человек")
            return
        
        bot.answer_callback_query(callback_query_id=event.id, show_alert=False,
                text="Все ок")
        
        template = template_env.get_template('end_game_ru.html')

        bot.edit_message_text(chat_id=event.message.chat.id, message_id=event.message.id,
            text=template.render(
                first_player_score=game.first_player_score,
                first_player_name=game.first_player_name,
                second_player_score=game.second_player_score,
                second_player_name=game.second_player_name,
            ), parse_mode='HTML')

        game.delete(pk=game.pk)