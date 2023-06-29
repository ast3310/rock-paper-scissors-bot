import handlers
from bot import bot

from redis_om import (
    get_redis_connection,
    Migrator
)

if __name__ == '__main__':
    print('Bot was started')

    redis = get_redis_connection()
    Migrator().run()

    bot.enable_save_next_step_handlers(delay=2)
    bot.load_next_step_handlers()
    bot.infinity_polling()