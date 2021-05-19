import asyncio
from nats.aio.client import Client as NATS
from stan.aio.client import Client as STAN
import os
async def run(loop):
    # Use borrowed connection for NATS then mount NATS Streaming
    # client on top.
    nats_cluster_ip = os.environ.get("NATS_CLUSTER_ID")
    nats_url =  os.environ.get("NATS_URL")
    nats_client_id =  os.environ.get("NATS_CLIENT_ID")
    nc = NATS()
    print("from cluster env",nats_cluster_ip,nats_client_id,nats_url)
    print("url from NAts",nc)
    await nc.connect(io_loop=loop)

    # Start session with NATS Streaming cluster.
    sc = STAN()
    await sc.connect("test-cluster", "client-123", nats=nc)

    # Synchronous Publisher, does not return until an ack
    # has been received from NATS Streaming.
    await sc.publish("hi", b'hello')
    await sc.publish("hi", b'world')

    total_messages = 0
    future = asyncio.Future(loop=loop)
    async def cb(msg):
        nonlocal future
        nonlocal total_messages
        print("Received a message (seq={}): {}".format(msg.seq, msg.data))
        total_messages += 1
        if total_messages >= 2:
            future.set_result(None)

    # Subscribe to get all messages since beginning.
    sub = await sc.subscribe("hi", start_at='first', cb=cb)
    await asyncio.wait_for(future, 1, loop=loop)

    # Stop receiving messages
    # await sub.unsubscribe()

    # Close NATS Streaming session
    # await sc.close()

    # We are using a NATS borrowed connection so we need to close manually.
    await nc.close()


