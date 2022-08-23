from admin_bot.config.loader import dp
from admin_bot.middleware.album import AlbumMiddleware

if __name__ == '__main__':
    dp.middleware.setup(AlbumMiddleware())
