"""
MIT License

Copyright (c) 2022 Omkaar

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


from __future__ import annotations

from time import sleep
from typing import Callable, Optional
from threading import Thread

from requests import Session

from .endpoints import BASE_URL
from .exceptions import UncallableError
from .models import Battlelog, BrawlStarsObject, BrawlerList, ClubMemberList, EventList, Player, PlayerRanking, ClubRanking, PowerPlaySeasonList
from .utils import _fetch, _difference


class Client:

    """
    A class that represents a client.

    :param token: The Brawl Stars API token.
    :type token: :class:`str`
    :param session: The session to use.
    :type session: Optional[:class:`requests.Session`]
    """

    def __init__(self, token: str, *, session: Optional[Session] = None) -> None:
        self.session = session if session else Session()
        self.session.headers = {"Authorization": f"Bearer {token}"}

    def get_player_battlelog(self, tag: str) -> Battlelog:
        """
        Gets a list of recent battle results for a player.

        .. note::

            It may take up to 30 minutes for a new battle to appear in the battlelog.

        :param tag: The tag of the player.
        :type tag: :class:`str`
        """
        data = _fetch(f"{BASE_URL}players/{tag}/battlelog", self)
        return Battlelog(data)

    def get_player(self, tag: str) -> Player:
        """
        Gets information about a single player.

        :param tag: The tag of the player.
        :type tag: :class:`str`
        """
        data = _fetch(f"{BASE_URL}players/{tag}", self)
        return Player(data)

    def get_club_members(self, tag: str, *, before: Optional[str] = None, after: Optional[str] = None, limit: Optional[int] = None) -> ClubMemberList:
        """
        Gets a list of club members.

        :param tag: The tag of the club.
        :type tag: :class:`str`
        :param before: The marker to return items before.
        :type before: Optional[:class:`str`]
        :param after: The marker to return items after.
        :type after: Optional[:class:`str`]
        :param limit: The maximum number of items to be returned.
        :type limit: Optional[:class:`int`]

        .. note::

            If both ``before`` and ``after`` are provided, a ``ValueError`` is raised.
        """
        if before and after:
            raise ValueError("both 'before' and 'after' cannot be provided.")
        data = _fetch(f"{BASE_URL}clubs/{tag}/members", self, {"before": before, "after": after, "limit": limit})
        return ClubMemberList(data)

    def get_club(self, tag: str) -> BrawlStarsObject:
        """
        Gets information about a single club.

        :param tag: The tag of the club.
        :type tag: :class:`str`
        """
        data = _fetch(f"{BASE_URL}clubs/{tag}", self)
        return BrawlStarsObject(data)

    def get_player_rankings(self, country: str, *, before: Optional[str] = None, after: Optional[str] = None, limit: Optional[int] = None) -> PlayerRanking:
        """
        Gets global player rankings or those for a specific country.

        :param country: The two-letter country code, or 'global' for global rankings.
        :type country: :class:`str`
        :param before: The marker to return items before.
        :type before: Optional[:class:`str`]
        :param after: The marker to return items after.
        :type after: Optional[:class:`str`]
        :param limit: The maximum number of items to be returned.
        :type limit: Optional[:class:`int`]

        .. note::

            If both ``before`` and ``after`` are provided, a ``ValueError`` is raised.
        """
        if before and after:
            raise ValueError("both 'before' and 'after' cannot be provided.")
        data = _fetch(f"{BASE_URL}rankings/{country}", self, {"before": before, "after": after, "limit": limit})
        return PlayerRanking(data)

    def get_brawler_rankings(self, country: str, brawler_id: int, *, before: Optional[str] = None, after: Optional[str] = None, limit: Optional[int] = None) -> PlayerRanking:
        """
        Gets global brawler rankings or those for a specific country.

        :param country: The two-letter country code, or 'global' for global rankings.
        :type country: :class:`str`
        :param before: The marker to return items before.
        :type before: Optional[:class:`str`]
        :param after: The marker to return items after.
        :type after: Optional[:class:`str`]
        :param limit: The maximum number of items to be returned.
        :type limit: Optional[:class:`int`]

        .. note::

            If both ``before`` and ``after`` are provided, a ``ValueError`` is raised.
        """
        if before and after:
            raise ValueError("both 'before' and 'after' cannot be provided.")
        data = _fetch(f"{BASE_URL}rankings/{country}/brawlers/{brawler_id}", self, {"before": before, "after": after, "limit": limit})
        return PlayerRanking(data)

    def get_club_rankings(self, country: str, *, before: Optional[str] = None, after: Optional[str] = None, limit: Optional[int] = None) -> ClubRanking:
        """
        Gets global club rankings or those for a specific country.

        :param country: The two-letter country code, or 'global' for global rankings.
        :type country: :class:`str`
        :param before: The marker to return items before.
        :type before: Optional[:class:`str`]
        :param after: The marker to return items after.
        :type after: Optional[:class:`str`]
        :param limit: The maximum number of items to be returned.
        :type limit: Optional[:class:`int`]

        .. note::

            If both ``before`` and ``after`` are provided, a ``ValueError`` is raised.
        """
        if before and after:
            raise ValueError("both 'before' and 'after' cannot be provided.")
        data = _fetch(f"{BASE_URL}rankings/{country}/clubs", self, {"before": before, "after": after, "limit": limit})
        return ClubRanking(data)

    def get_powerplay_seasons(self, country: str, *, before: Optional[str] = None, after: Optional[str] = None, limit: Optional[int] = None) -> PowerPlaySeasonList:
        """
        Gets a list of Power Play seasons.

        :param country: The two-letter country code, or 'global' for global rankings.
        :type country: :class:`str`
        :param before: The marker to return items before.
        :type before: Optional[:class:`str`]
        :param after: The marker to return items after.
        :type after: Optional[:class:`str`]
        :param limit: The maximum number of items to be returned.
        :type limit: Optional[:class:`int`]

        .. note::

            If both ``before`` and ``after`` are provided, a ``ValueError`` is raised.
        """

        if before and after:
            raise ValueError("both 'before' and 'after' cannot be provided.")
        data = _fetch(f"{BASE_URL}rankings/{country}/powerplay/seasons", self, {"before": before, "after": after, "limit": limit})
        return PowerPlaySeasonList(data)

    def get_powerplay_rankings(self, country: str, season_id: str, *, before: Optional[str] = None, after: Optional[str] = None, limit: Optional[int] = None) -> PlayerRanking:
        """
        Gets global Power Play rankings or those for a specific country.

        :param country: The two-letter country code, or 'global' for global rankings.
        :type country: :class:`str`
        :param season_id: The identifier of the season, or 'latest' for the latest season.
        :type season_id: :class:`str`
        :param before: The marker to return items before.
        :type before: Optional[:class:`str`]
        :param after: The marker to return items after.
        :type after: Optional[:class:`str`]
        :param limit: The maximum number of items to be returned.
        :type limit: Optional[:class:`int`]

        .. note::

            If both ``before`` and ``after`` are provided, a ``ValueError`` is raised.
        """

        if before and after:
            raise ValueError("both 'before' and 'after' cannot be provided.")
        data = _fetch(f"{BASE_URL}rankings/{country}/powerplay/seasons/{season_id}", self, {"before": before, "after": after, "limit": limit})
        return PlayerRanking(data)

    def get_brawlers(self, *, before: Optional[str] = None, after: Optional[str] = None, limit: Optional[int] = None) -> PlayerRanking:
        """
        Gets a list of brawlers.

        :param before: The marker to return items before.
        :type before: Optional[:class:`str`]
        :param after: The marker to return items after.
        :type after: Optional[:class:`str`]
        :param limit: The maximum number of items to be returned.
        :type limit: Optional[:class:`int`]

        .. note::

            If both ``before`` and ``after`` are provided, a ``ValueError`` is raised.
        """
        if before and after:
            raise ValueError("both 'before' and 'after' cannot be provided.")
        data = _fetch(f"{BASE_URL}brawlers", self, {"before": before, "after": after, "limit": limit})
        return BrawlerList(data)

    def get_brawler(self, brawler_id: str) -> BrawlStarsObject:
        """
        Gets a list of brawlers.

        :param before: The marker to return items before.
        :type before: Optional[:class:`str`]
        :param after: The marker to return items after.
        :type after: Optional[:class:`str`]
        """
        data = _fetch(f"{BASE_URL}brawlers/{brawler_id}", self)
        return BrawlStarsObject(data)

    def get_event_rotation(self) -> EventList:
        """
        Gets the event rotation.
        """
        data = _fetch(f"{BASE_URL}events/rotation", self)
        return EventList(data)

    def on_member_join(self, tag: str, *, repeat_duration: Optional[float] = 60):
        """
        Event that is called when a member joins a club.

        :param tag: The tag of the club.
        :type tag: :class:`str`
        :param repeat_duration: The time to sleep for between every check.
        :type repeat_duration: Optional[:class:`float`]
        """
        def decorator(function: Callable):

            def process():
                while True:
                    cache = list(self.get_club_members(tag))
                    sleep(repeat_duration)
                    current = list(self.get_club_members(tag))
                    difference = _difference(current, cache)
                    if len(difference) >= 1:
                        function(members = difference)

            thread = Thread(target = process)
            thread.start()

            def error():
                raise UncallableError("functions used for events are not callable.")

            return error

        return decorator

    def on_member_leave(self, tag: str, repeat_duration: Optional[float] = 60):
        """
        Event that is called when a member leaves a club.

        :param tag: The tag of the club.
        :type tag: :class:`str`
        :param repeat_duration: The time to sleep for between every check.
        :type repeat_duration: Optional[:class:`float`]
        """
        def decorator(function: Callable):

            def process():
                while True:
                    cache = list(self.get_club_members(tag))
                    sleep(repeat_duration)
                    current = list(self.get_club_members(tag))
                    difference = _difference(cache, current)
                    if len(difference) >= 1:
                        function(members = difference)

            thread = Thread(target = process)
            thread.start()

            def error():
                raise UncallableError("functions used for events are not callable.")

            return error

        return decorator

    def on_battlelog_update(self, tag: str, repeat_duration: Optional[float] = 60):
        """
        Event that is called when a player's battlelog is updated.

        :param tag: The tag of the player.
        :type tag: :class:`str`
        :param repeat_duration: The time to sleep for between every check.
        :type repeat_duration: Optional[:class:`float`]
        """
        def decorator(function: Callable):

            def process():
                while True:
                    cache = list(self.get_player_battlelog(tag))
                    sleep(repeat_duration)
                    current = list(self.get_player_battlelog(tag))
                    difference = _difference(current, cache)
                    if len(difference) >= 1:
                        function(battles = difference)

            thread = Thread(target = process)
            thread.start()

            def error():
                raise UncallableError("functions used for events are not callable.")

            return error

        return decorator
