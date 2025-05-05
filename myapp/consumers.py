# d:\Term-4\Advanced sw\Nan-Project-Phase-1\NU_advanced_SW_Nano_Project\myapp\consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
import logging

logger = logging.getLogger(__name__)

class ChatConsumer(AsyncWebsocketConsumer):
    # Keep track of users per room to know which rooms are active
    room_users = {}

    async def connect(self):
        # Get user from scope (populated by AuthMiddlewareStack)
        self.user = self.scope.get("user")

        # --- FIX: Add Authentication Check ---
        if not self.user or not self.user.is_authenticated:
            logger.warning(f"Unauthenticated WebSocket connection attempt rejected. User: {self.user}")
            await self.close() # Close the connection gracefully
            return # Stop further processing for this connection
        # --- End FIX ---

        # User is authenticated, proceed
        self.username = self.user.username # Now safe to access username
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        logger.info(f"User '{self.username}' connecting to room '{self.room_name}'")

        # Add this channel to the room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Add user to the room's user set
        if self.room_name not in ChatConsumer.room_users:
            ChatConsumer.room_users[self.room_name] = set()
        is_new_user = self.username not in ChatConsumer.room_users[self.room_name]
        ChatConsumer.room_users[self.room_name].add(self.username)

        # Accept the connection ONLY if authenticated
        await self.accept()

        # Broadcast user join message
        if is_new_user:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "user_join",
                    "username": self.username,
                }
            )
        logger.info(f"User '{self.username}' connected. Active users in '{self.room_name}': {list(ChatConsumer.room_users.get(self.room_name, set()))}")


    async def disconnect(self, close_code):
        # Use getattr for safety, in case connect failed before setting attributes
        username_to_log = getattr(self, 'username', 'Unknown user')
        room_name_to_log = getattr(self, 'room_name', 'Unknown room')

        logger.info(f"User '{username_to_log}' disconnecting from room '{room_name_to_log}' (Code: {close_code})")

        # Check if attributes were set (connection might fail before)
        # Also check if user was authenticated before proceeding with cleanup
        if hasattr(self, 'user') and self.user.is_authenticated and hasattr(self, 'room_name') and hasattr(self, 'username'):
            user_existed = False
            if self.room_name in ChatConsumer.room_users:
                if self.username in ChatConsumer.room_users[self.room_name]:
                    ChatConsumer.room_users[self.room_name].discard(self.username)
                    user_existed = True
                # Check if room is empty after discarding
                if not ChatConsumer.room_users[self.room_name]:
                    logger.info(f"Room '{self.room_name}' is now empty, removing from active list.")
                    del ChatConsumer.room_users[self.room_name] # Remove room if empty

            # Broadcast user leave message only if they were actually in the room
            if user_existed and hasattr(self, 'room_group_name'):
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        "type": "user_leave",
                        "username": self.username,
                    }
                )

        # Remove this channel from the room group if group name exists
        if hasattr(self, 'room_group_name'):
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )
        # Log remaining users (might be slightly delayed if disconnect is abrupt)
        logger.info(f"User '{username_to_log}' disconnected process finished. Active users in '{room_name_to_log}': {list(ChatConsumer.room_users.get(room_name_to_log, set()))}")


    async def receive(self, text_data):
        # This check is good, keep it.
        if not hasattr(self, 'user') or not self.user.is_authenticated:
             logger.warning("Received message from unauthenticated connection. Ignoring.")
             return

        try:
            data = json.loads(text_data)
            message_type = data.get("type")

            if message_type == 'chat_message':
                message = data.get("message")
                if not message:
                     logger.warning(f"Received incomplete chat message from {self.username}: {data}")
                     return
                logger.info(f"Received message from '{self.username}' in room '{self.room_name}': {message}")
                await self.channel_layer.group_send(
                    self.room_group_name,
                    { "type": "chat_message_broadcast", "username": self.username, "message": message, }
                )
            else:
                logger.warning(f"Received unknown message type '{message_type}' from {self.username} in {self.room_name}")
        except json.JSONDecodeError:
            logger.error(f"Failed to decode JSON from {self.username} in {self.room_name}: {text_data}")
        except Exception as e:
            # Log the specific exception
            logger.exception(f"Error processing received message in {self.room_name} from {self.username}: {e}")


    # --- Handler methods ---
    async def chat_message_broadcast(self, event):

        await self.send(text_data=json.dumps({
            "type": "chat_message",
            "username": event["username"],
            "message": event["message"],
        }))

    async def user_join(self, event):
        await self.send(text_data=json.dumps({
            "type": "user_join",
            "username": event["username"],
        }))

    async def user_leave(self, event):
        await self.send(text_data=json.dumps({
            "type": "user_leave",
            "username": event["username"],
        }))

    @classmethod
    def get_active_rooms(cls):
        # Return only room names
        # Cleanup: remove unused user_count calculation
        active_rooms_data = []
        for room_name in cls.room_users.keys(): # Iterate through keys directly
             # Check if the room still has users before adding (optional safety)
             if cls.room_users.get(room_name):
                active_rooms_data.append({ "name": room_name })
             else:
                 # Handle case where room might be empty but not yet deleted (shouldn't happen often with current logic)
                 logger.warning(f"Room '{room_name}' found in keys but empty during get_active_rooms.")
        return active_rooms_data

