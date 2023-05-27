import asyncio

class AsyncioStack:
    def __init__(self):
        self.stack = []
        self.lock = asyncio.Lock()

    async def push(self, item):
        async with self.lock:
            self.stack.append(item)

    async def pop(self):
        async with self.lock:
            if not self.stack:
                return None
            return self.stack.pop()
        
    async def clear(self):
        async with self.lock:
            self.stack.clear()

    def len(self):
        return len(self.stack)
        # async with self.lock: