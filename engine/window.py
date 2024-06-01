import pygame


class Window():
    def __init__(self, res: tuple[int,int] = (1280,800)):
        pygame.init()
        self.res = res
        self.surface = pygame.display.set_mode(self.res)
        self.surface.fill((0,0,0))
        self.clock = pygame.time.Clock()
        self.frame_rate = 60

    def update(self):
        pygame.display.flip()
        self.clock.tick(self.frame_rate)

    def close(self):
        pygame.quit()


