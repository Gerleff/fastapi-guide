from asyncio import Queue


class AsyncFanoutQueue:
    def __init__(self) -> None:
        self.subscribers: set[Queue] = set()

    def register(self, queque: Queue | None = None) -> Queue:
        queue = queque or Queue()
        self.subscribers.add(queue)
        return queue

    async def unregister(self, subscriber: Queue) -> None:
        self.subscribers.remove(subscriber)
        await subscriber.put({"type": "finish"})

    async def multicast(self, message: dict) -> None:
        for subscriber in self.subscribers:
            await subscriber.put(message)

