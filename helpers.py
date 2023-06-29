import functools
from models import Game
from redis_om import NotFoundError
from telebot import types

from enum import Enum


class Player(Enum):
    FIRST = 1
    SECOND = 2


class Move(Enum):
    ROCK = 'rock'
    SCISSORS = 'scissors'
    PAPER = 'paper'


def in_game_middleware(func):
    @functools.wraps(func)
    def wrapper_type(event, *args, **kwargs):
        chat_id = event.message.chat.id if isinstance(event, types.CallbackQuery) else event.chat.id
        try:
            game = Game.find(Game.chat_id == chat_id).first()
        except NotFoundError:
            game = None
        return func(event, game, *args, **kwargs)
    return wrapper_type

def get_player_by_id(game, user_id):
    if game.first_player != user_id and \
            game.second_player != user_id:
        return (None, user_id)
    player = (Player.FIRST if game.first_player == user_id else Player.SECOND)

    return (player, user_id)