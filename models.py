import datetime
from typing import Optional, Union

from redis_om import HashModel, Field

class Game(HashModel):
    chat_id: int = Field(index=True)
    game_message_id: int
    is_started: int = 0
    join_date: datetime.date

    moves_message_id: Optional[int] = 0
    first_player: Optional[int] = 0
    first_player_name: Optional[str] = ''
    second_player: Optional[int] = 0
    second_player_name: Optional[str] = ''
    first_player_move: Optional[str] = ''
    second_player_move: Optional[str] = ''
    first_player_score: Optional[int] = 0
    second_player_score: Optional[int] = 0