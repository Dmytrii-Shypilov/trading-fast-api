import asyncio

class AsyncManager:
    def __init__(self, limit: int = 400):
        self.tasks = []
        self.semaphore = asyncio.Semaphore(limit)

    async def add_async_operation(self, coro):
        # wrap the coroutine with the semaphore guard
        async def wrapper():
            async with self.semaphore:
                return await coro
        self.tasks.append(asyncio.create_task(wrapper()))

    async def get_results(self):
     
            results = await asyncio.gather(*self.tasks)
            self.tasks.clear()
            return results
     
