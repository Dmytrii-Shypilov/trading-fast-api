import asyncio

class AsyncManager:
    tasks = []
    
    async def add_async_operation(self, operation):
        self.tasks.append(asyncio.create_task(operation))
    async def get_results(self):
        results = await asyncio.gather(*self.tasks)
        self.tasks.clear()
        return results