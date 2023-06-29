import datetime
from typing import Optional, Union

from redis_om import HashModel, Field

class Game(HashModel):
    chat_id: int = Field(index=True)
    join_date: datetime.date
    first_player: int = None
    first_player_name: str = None
    second_player: int = None
    second_player_name: str = None
    first_player_move: Optional[str] = None
    second_player_move: Optional[str] = None
    first_player_score: Optional[int] = 0
    second_player_score: Optional[int] = 0