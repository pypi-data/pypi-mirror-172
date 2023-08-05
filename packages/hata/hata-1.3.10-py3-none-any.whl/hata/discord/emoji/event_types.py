__all__ = ('ReactionAddEvent', 'ReactionDeleteEvent', )

from scarletio import Task, copy_docs

from ..bases import EventBase
from ..core import KOKORO
from ..exceptions import DiscordException, ERROR_CODES
from ..permission.permission import PERMISSION_MASK_MANAGE_MESSAGES


async def _delete_reaction_with_task(reaction_add_event, client):
    """
    Removes the given reaction event's emoji from it's message if applicable. Expected error codes are silenced.
    
    Parameters
    ----------
    reaction_add_event : ``ReactionAddEvent``, ``ReactionDeleteEvent``
        The respective reaction event.
    client : ``Client``
        The client who should remove the reaction if applicable.
    """
    try:
        await client.reaction_delete(reaction_add_event.message, reaction_add_event.emoji, reaction_add_event.user)
    except GeneratorExit:
        raise
    
    except BaseException as err:
        
        if isinstance(err, ConnectionError):
            # no internet
            return
        
        if isinstance(err, DiscordException):
            if err.code in (
                ERROR_CODES.unknown_message, # message deleted
                ERROR_CODES.unknown_channel, # channel deleted
                ERROR_CODES.missing_access, # client removed
                ERROR_CODES.missing_permissions, # permissions changed meanwhile
            ):
                return
        
        await client.events.error(client, f'_delete_reaction_with_task called from {reaction_add_event!r}', err)
        return


class ReactionAddEvent(EventBase):
    """
    Represents a processed `MESSAGE_REACTION_ADD` dispatch event.
    
    Attributes
    ----------
    message : ``Message``
        The message on what the reaction is added.
    emoji : ``Emoji``
        The emoji used as reaction.
    user : ``ClientUserBase``
        The user who added the reaction.
    
    Class Attributes
    ----------------
    DELETE_REACTION_OK : `int` = `0`
        Returned by ``.delete_reaction_with`` when the client has permission to execute the reaction remove.
    DELETE_REACTION_PERM : `int` = `1`
        Returned by ``.delete_reaction_with`` when the client has no permission to execute the reaction remove.
    DELETE_REACTION_NOT_ADDED : `int` = `2`
        Returned by ``.delete_reaction_with`` when the client has permission to execute the reaction remove, but
        it cannot, because the reaction is not added on the respective message. Not applicable for
        ``ReactionAddEvent``.
    """
    __slots__ = ('message', 'emoji', 'user')
    
    def __new__(cls, message, emoji, user):
        """
        Creates a new ``ReactionAddEvent`` (or it's subclass's instance).
        
        Parameters
        ----------
        message : ``Message``
            The respective message.
        emoji : ``Emoji``
            The emoji used.
        user : ``ClientUserBase``
            The user who reacted.
        """
        self = object.__new__(cls)
        self.message = message
        self.emoji = emoji
        self.user = user
        return self
    
    
    @copy_docs(EventBase.__repr__)
    def __repr__(self):
        return (
            f'<{self.__class__.__name__} message={self.message!r}, emoji={self.emoji!r}, '
            f'user={self.user.full_name!r}>'
        )
    
    
    @copy_docs(EventBase.__len__)
    def __len__(self):
        return 3
    
    
    @copy_docs(EventBase.__iter__)
    def __iter__(self):
        yield self.message
        yield self.emoji
        yield self.user
    
    
    @copy_docs(EventBase.__eq__)
    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        # message type can be different, so check id instead of identity
        if self.message.id != other.message.id:
            return False
        
        if self.emoji is not other.emoji:
            return False
        
        if self.user is not other.user:
            return False
        
        return True
    
    
    @copy_docs(EventBase.__hash__)
    def __hash__(self):
        return self.message.id ^ self.emoji.id ^ self.user.id
    
    
    def delete_reaction_with(self, client):
        """
        Removes the added reaction.
        
        Parameters
        ----------
        client : ``Client``
            The client, who will execute the action.
        
        Returns
        -------
        result : `int`
            The identifier number of the action what will be executed.
            
            Can be one of the following:
            +-----------------------+-------+
            | Respective name       | Value |
            +=======================+=======+
            | DELETE_REACTION_OK    | 0     |
            +-----------------------+-------+
            | DELETE_REACTION_PERM  | 1     |
            +-----------------------+-------+
        """
        if self.message.channel.cached_permissions_for(client) & PERMISSION_MASK_MANAGE_MESSAGES:
            Task(_delete_reaction_with_task(self, client), KOKORO)
            result = self.DELETE_REACTION_OK
        else:
            result = self.DELETE_REACTION_PERM
        
        return result
    
    DELETE_REACTION_OK = 0
    DELETE_REACTION_PERM = 1
    DELETE_REACTION_NOT_ADDED = 2
    

class ReactionDeleteEvent(ReactionAddEvent):
    """
    Represents a processed `MESSAGE_REACTION_REMOVE` dispatch event.
    
    Attributes
    ----------
    message : ``Message``
        The message from what the reaction was removed.
    emoji : ``Emoji``
        The removed emoji.
    user : ``ClientUserBase``
        The user who's reaction was removed.
    
    Class Attributes
    ----------------
    DELETE_REACTION_OK : `int` = `0`
        Returned by ``.delete_reaction_with`` when the client has permission to execute the reaction remove. Not
        applicable on ``ReactionDeleteEvent``.
    DELETE_REACTION_PERM : `int` = `1`
        Returned by ``.delete_reaction_with`` when the client has no permission to execute the reaction remove.
    DELETE_REACTION_NOT_ADDED : `int` = `2`
        Returned by ``.delete_reaction_with`` when the client has permission to execute the reaction remove, but
        it cannot, because the reaction is not added on the respective message.
    """
    __slots__ = ()
    
    def delete_reaction_with(self, client):
        """
        Removes the added reaction. Because the event is ``ReactionDeleteEvent``, it will not remove any reaction, but
        only check the permissions.
        
        Parameters
        ----------
        client : ``Client``
            The client, who will execute the action.
        
        Returns
        -------
        result : `int`
            The identifier number of the action what will be executed.
            
            Can be one of the following:
            +---------------------------+-------+
            | Respective name           | Value |
            +===========================+=======+
            | DELETE_REACTION_PERM      | 1     |
            +---------------------------+-------+
            | DELETE_REACTION_NOT_ADDED | 2     |
            +---------------------------+-------+
        """
        if self.message.channel.cached_permissions_for(client) & PERMISSION_MASK_MANAGE_MESSAGES:
            result = self.DELETE_REACTION_NOT_ADDED
        else:
            result = self.DELETE_REACTION_PERM
        
        return result
