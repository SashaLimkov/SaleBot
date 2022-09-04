from bot.config.loader import dp
from bot.middleware.album import AlbumMiddleware

if __name__ == "__main__":
    dp.middleware.setup(AlbumMiddleware())
