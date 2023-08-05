__all__ = ('GuildPreview', )

from ..bases import DiscordEntity, IconSlot
from ..emoji import Emoji
from ..http import urls as module_urls
from ..sticker import Sticker
from ..utils import DATETIME_FORMAT_CODE

from .preinstanced import GuildFeature


class GuildPreview(DiscordEntity):
    """
    A preview of a public guild.
    
    Attributes
    ----------
    approximate_online_count : `int`
        Approximate amount of online users at the guild.
    approximate_user_count : `int`
        Approximate amount of users at the guild.
    description : `None`, `str`
        Description of the guild. The guild must have `PUBLIC` feature.
    discovery_splash_hash : `int`
        The guild's discovery splash's hash in `uint128`. The guild must have `DISCOVERABLE` feature to have
        discovery splash.
    discovery_splash_type : ``IconType``
        The guild discovery splash's type.
    emojis : `dict` of (`int`, ``Emoji``) items
        The emojis of the guild stored in `emoji_id` - `emoji` relation.
    features : `list` of ``GuildFeature``
        The guild's features.
    icon_hash : `int`
        The guild's icon's hash in `uint128`.
    icon_type : ``IconType``
        The guild's icon's type.
    invite_splash_hash : `int`
        The guild's invite splash's hash in `uint128`. The guild must have `INVITE_SPLASH` feature.
    invite_splash_type : ``IconType``
        the guild's invite splash's type.
    stickers : `dict` of (`int`, ``Sticker``) items
        The stickers of the guild stored in `sticker_id` - `sticker` relation.
    name : `str`
        The name of the guild.
    """
    __slots__ = (
        'approximate_online_count', 'approximate_user_count','description', 'emojis', 'features', 'name', 'stickers'
    )
    
    icon = IconSlot(
        'icon',
        'icon',
        module_urls.guild_icon_url,
        module_urls.guild_icon_url_as,
    )
    
    invite_splash = IconSlot(
        'invite_splash',
        'splash',
        module_urls.guild_invite_splash_url,
        module_urls.guild_invite_splash_url_as,
    )
    
    discovery_splash = IconSlot(
        'discovery_splash',
        'discovery_splash',
        module_urls.guild_discovery_splash_url,
        module_urls.guild_discovery_splash_url_as,
    )
    
    def __init__(self, data):
        """
        Creates a guild preview from the requested guild preview data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Received guild preview data.
        """
        guild_id = int(data['id'])
        
        self.description = data.get('description',None)
        
        self._set_discovery_splash(data)
        
        emojis = {}
        self.emojis = emojis
        try:
            emoji_datas = data['emojis']
        except KeyError:
            pass
        else:
            for emoji_data in emoji_datas:
                emoji = Emoji(emoji_data, guild_id)
                emojis[emoji.id] = emoji
        
        stickers = {}
        self.stickers = stickers
        try:
            sticker_datas = data['stickers']
        except KeyError:
            pass
        else:
            for sticker_data in sticker_datas:
                sticker = Sticker(sticker_data)
                stickers[sticker.id] = sticker
        
        features = []
        self.features = features
        try:
            feature_datas = data['features']
        except KeyError:
            pass
        else:
            for feature_data in feature_datas:
                feature = GuildFeature.get(feature_data)
                features.append(feature)
            
            features.sort()
        
        self._set_icon(data)
        
        self.id = guild_id
        
        self.name = data['name']
        
        self.approximate_online_count = data['approximate_presence_count']
        
        self._set_invite_splash(data)
        
        self.approximate_user_count = data['approximate_member_count']
    
    
    def __repr__(self):
        """Returns the guild preview's representation."""
        return f'<{self.__class__.__name__} id={self.id}, name={self.name!r}>'
    
    
    def __format__(self, code):
        """
        Formats the guild preview in a format string.
        
        Parameters
        ----------
        code : `str`
            The option on based the result will be formatted.
        
        Returns
        -------
        channel : `str`
        
        Raises
        ------
        ValueError
            Unknown format code.
        
        Examples
        --------
        ```py
        >>> from hata import Client, KOKORO
        >>> TOKEN = 'a token goes here'
        >>> client = Client(TOKEN)
        >>> guild_id = 302094807046684672
        >>> guild_preview = KOKORO.run(client.guild_preview_get(guild_id))
        >>> guild_preview
        <GuildPreview id=302094807046684672, name='MINECRAFT'>
        >>> # no code stands for `guild_preview.name`.
        >>> f'{guild_preview}'
        'MINECRAFT'
        >>> # 'c' stands for created at.
        >>> f'{guild_preview:c}'
        '2017.04.13-14:56:54'
        ```
        """
        if not code:
            return self.name
        
        if code == 'c':
            return format(self.created_at, DATETIME_FORMAT_CODE)
        
        raise ValueError(
            f'Unknown format code {code!r} for {self.__class__.__name__}; {self!r}. '
            f'Available format codes: {""!r}, {"c"!r}.'
        )
