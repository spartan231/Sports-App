import pygame
import asyncio


async def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()
    running = True

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill("white")


        pygame.display.flip()

        clock.tick(60)
        await asyncio.sleep(0)

asyncio.run(main())
