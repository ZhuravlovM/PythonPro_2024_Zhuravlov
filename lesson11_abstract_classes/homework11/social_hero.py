from abc import ABC, abstractmethod
from datetime import datetime
from typing import List


class SocialChannel(ABC):
    def __init__(self, channel_type: str, followers: int):
        self.type = channel_type
        self.followers = followers

    @abstractmethod
    def post(self, message: str) -> None:
        pass


class YoutubeChannel(SocialChannel):
    def post(self, message: str) -> None:
        print(f"Posting to YouTube: {message}")


class FacebookChannel(SocialChannel):
    def post(self, message: str) -> None:
        print(f"Posting to Facebook: {message}")


class TwitterChannel(SocialChannel):
    def post(self, message: str) -> None:
        print(f"Posting to Twitter: {message}")


class Post:
    def __init__(self, message: str, timestamp: datetime):
        self.message = message
        self.timestamp = timestamp


def post_a_message(channel: SocialChannel, message: str) -> None:
    channel.post(message)


def process_schedule(posts: List[Post], channels: List[SocialChannel]) -> None:
    current_time = datetime.now()
    for post in posts:
        if post.timestamp <= current_time:
            for channel in channels:
                post_a_message(channel, post.message)


youtube_channel = YoutubeChannel("youtube", 90)
facebook_channel = FacebookChannel("facebook", 70)
twitter_channel = TwitterChannel("twitter", 150)

posts = [
    Post("This is a 1st post!", datetime(2024, 2, 21, 12, 0)),
    Post("This is a 2nd post!", datetime(2024, 2, 22, 12, 0)),
    Post("This is a 3rd post!", datetime(2024, 2, 23, 12, 0)),
]

process_schedule(posts, [youtube_channel, facebook_channel, twitter_channel])
