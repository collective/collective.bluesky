from prettyconf import config


IMAGE_WIDTH = config("BLUESKY_IMAGE_WIDTH", cast=int, default=1920)
POST_CHAR_LIMIT = config("BLUESKY_POST_CHAR_LIMIT", cast=int, default=300)


def get_bluesky_apps():
    return config("BLUESKY_APPS", cast=config.json, default="[]")
