from inspect import getmembers
from typing import Dict, List, Optional, Union

from lavalink import Client as LavalinkClient

from interactions import Client, Snowflake

from .models import VoiceState
from .player import Player
from .websocket import VoiceWebSocketClient

__all__ = ["VoiceClient", "listener"]


class VoiceClient(Client):
    def __init__(self, token: str, **kwargs):
        super().__init__(token, **kwargs)

        self._websocket = VoiceWebSocketClient(
            self, token, self._intents, shards=self._shards, presence=self._presence
        )
        self.lavalink_client: LavalinkClient = None

        self._websocket._dispatch.register(
            self.__raw_voice_state_update, "on_raw_voice_state_update"
        )
        self._websocket._dispatch.register(
            self.__raw_voice_server_update, "on_raw_voice_server_update"
        )

    async def _login(self) -> None:
        self._http._bot_var = self
        self.lavalink_client = LavalinkClient(int(self.me.id), player=Player)

        self.__register_lavalink_listeners()

        await super()._login()

    async def __raw_voice_state_update(self, data: dict):
        lavalink_data = {"t": "VOICE_STATE_UPDATE", "d": data}
        await self.lavalink_client.voice_update_handler(lavalink_data)

    async def __raw_voice_server_update(self, data: dict):
        lavalink_data = {"t": "VOICE_SERVER_UPDATE", "d": data}
        await self.lavalink_client.voice_update_handler(lavalink_data)

    async def connect(
        self,
        guild_id: Union[Snowflake, int, str],
        channel_id: Union[Snowflake, int, str],
        self_deaf: bool = False,
        self_mute: bool = False,
    ) -> Player:
        """
        Connects to voice channel and creates player.

        :param Union[Snowflake, int, str] guild_id: The guild id to connect.
        :param Union[Snowflake, int, str] channel_id: The channel id to connect.
        :param bool self_deaf: Whether bot is self deafened
        :param bool self_mute: Whether bot is self muted
        :return: Created guild player.
        :rtype: Player
        """
        if guild_id is None:
            raise TypeError("guild_id cannot be NoneType")
        if channel_id is None:
            raise TypeError("channel_id cannot be NoneType for connect method")

        await self._websocket.update_voice_state(guild_id, channel_id, self_deaf, self_mute)
        player = self.lavalink_client.player_manager.get(int(guild_id))
        if player is None:
            player = self.lavalink_client.player_manager.create(int(guild_id))
        return player

    async def disconnect(self, guild_id: Union[Snowflake, int]):
        if guild_id is None:
            raise TypeError("guild_id cannot be NoneType")

        await self._websocket.update_voice_state(int(guild_id))
        await self.lavalink_client.player_manager.destroy(int(guild_id))

    def get_player(self, guild_id: Union[Snowflake, int]) -> Player:
        """
        Returns current player in guild.

        :param Union[Snowflake, int] guild_id: The guild id
        :return: Guild player
        :rtype: Player
        """
        return self.lavalink_client.player_manager.get(int(guild_id))

    @property
    def voice_states(self) -> Dict[Snowflake, VoiceState]:
        """Returns dict of cached voice states"""
        return self._http.cache[VoiceState].values

    def get_user_voice_state(self, user_id: Union[Snowflake, int]) -> Optional[VoiceState]:
        """
        Returns user voice state.

        :param Union[Snowflake, int] user_id: The user id
        :return: Founded user voice state else nothing
        :rtype: Optional[VoiceState]
        """

        _user_id = Snowflake(user_id) if isinstance(user_id, int) else user_id
        return self._http.cache[VoiceState].get(_user_id)

    def get_guild_voice_states(self, guild_id: Union[Snowflake, int]) -> Optional[List[VoiceState]]:
        """
        Returns guild voice states.

        :param Union[Snowflake, int] guild_id: The channel id
        :return: Founded channel voice states else nothing
        :rtype: Optional[List[VoiceState]]
        """

        _guild_id = Snowflake(guild_id) if isinstance(guild_id, int) else guild_id
        return [
            voice_state
            for voice_state in self.voice_states.values()
            if voice_state.guild_id == _guild_id
        ]

    def get_channel_voice_states(
        self, channel_id: Union[Snowflake, int]
    ) -> Optional[List[VoiceState]]:
        """
        Returns channel voice states.

        :param Union[Snowflake, int] channel_id: The channel id
        :return: Founded channel voice states else nothing
        :rtype: Optional[List[VoiceState]]
        """

        _channel_id = Snowflake(channel_id) if isinstance(channel_id, int) else channel_id
        return [
            voice_state
            for voice_state in self.voice_states.values()
            if voice_state.channel_id == _channel_id
        ]

    def __register_lavalink_listeners(self):
        for extension in self._extensions.values():
            for name, func in getmembers(extension):
                if not hasattr(func, "__lavalink__"):
                    continue
                name = func.__lavalink__[3:]
                event_name = "".join(word.capitalize() for word in name.split("_")) + "Event"
                event_hooks = self.lavalink_client._event_hooks
                if event_name not in event_hooks:
                    event_hooks[event_name] = []
                event_hooks[event_name].append(func)


def listener(func=None, *, name: str = None):
    def wrapper(func):
        _name = name or func.__name__
        func.__lavalink__ = _name
        return func

    if func is not None:
        return wrapper(func)
    return wrapper
