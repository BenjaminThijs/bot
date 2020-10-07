from base_client import BaseClient

class Client(BaseClient):
    async def stop(self, message, *args):
        await self.say(message.channel, "Bye bye")
        await self.close()
