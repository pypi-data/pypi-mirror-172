from instagrapi import Client
from instagrapi.types import Media

class LikesUtility:
    def __init__(self, session: Client):
        self.session = session

        self.enabled = False
        self.percentage = 0

    def set_enabled(self, enabled: bool):
        self.enabled = enabled

    def set_percentage(self, percentage: int):
        self.percentage = percentage

    def like(self, media: Media) -> bool:
        try:
            liked = self.session.media_like(media_id=media.id)
            print(f'[INFO]: Successfully liked media: {media.code}.' if liked else f'[ERROR]: Failed to like media.')
            return liked
        except Exception as error:
            print(f'[ERROR]: {error}.')
            return False