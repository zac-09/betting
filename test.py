import asyncio
from nats.aio.client import Client as NATS
from stan.aio.client import Client as STAN
import json
   
class CreatOddsPublisher:
    def __init__(self) -> None:   
        self.nc = ""
        self.sc = ""

    async def run(self,loop,message):
        # Use borrowed connection for NATS then mount NATS Streaming
        # client on top.
        self.nc = NATS()
        await self.nc.connect(io_loop=loop)

        # Start session with NATS Streaming cluster.
        self.sc = STAN()
        await self.sc.connect("test-cluster", "client-123-2", nats=self.nc)

        
        await self.sc.publish("create-odds",json.dumps(message).encode())
    
        await self.sc.close()

        # We are using a NATS borrowed connection so we need to close manually.
        await self.nc.close()
    def publish(self,message):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self.run(loop,message))
            loop.close()