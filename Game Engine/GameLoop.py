import asyncio
from Time import Time
class GameLoop:
    def __init__(self):
        self.timer = Time()
        self.start()

    def start(self):
        pass

    async def update(self):
        while True:       
            await asyncio.sleep(self.timer.deltaTime)

    async def main(self):
        await asyncio.gather(
            # Add concurrent Tasks here
            self.update()
        )

    asyncio.run(main())

