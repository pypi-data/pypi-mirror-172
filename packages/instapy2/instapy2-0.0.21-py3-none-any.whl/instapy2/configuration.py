from . import comments, follows, interactions, likes, location, media, people

from instagrapi import Client

class Configuration:
    def __init__(self, session: Client):
        self.comments = comments.CommentsUtility()
        self.follows = follows.FollowUtility(session=session)
        self.interactions = interactions.InteractionsUtility()
        self.likes = likes.LikesUtility(session=session)
        self.media = media.MediaUtil()

        self.location = location.LocationHelper(session=session)
        self.people = people.PeopleHelper(session=session)