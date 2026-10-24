import pygame


class Button:
    def __init__(self, x, y, image, image2, scale):
        width = image.get_width()
        height = image.get_height()
        size = (int(width * scale), int(height * scale))
        self.image = pygame.transform.scale(image, size)
        self.image2 = pygame.transform.scale(image2, size)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.clicked = False
        self.pressed_until = 0
        self.pressed_image_active = False

    def res(self):
        self.clicked = False
        self.pressed_until = 0
        self.pressed_image_active = False

    def draw(self, surface, events=()):
        action = False
        now = pygame.time.get_ticks()
        mouse_down = bool(pygame.mouse.get_pressed()[0])
        over_button = self.rect.collidepoint(pygame.mouse.get_pos())

        # Use queued click events so a quick click is not missed between frames.
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.rect.collidepoint(event.pos):
                    self.clicked = True
                    self.pressed_until = now + 120
                    action = True
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.clicked = False

        # Also recover if a release event was missed.
        if not mouse_down:
            self.clicked = False

        self.pressed_image_active = (
            (self.clicked and mouse_down and over_button)
            or now < self.pressed_until
        )
        image = self.image2 if self.pressed_image_active else self.image
        surface.blit(image, self.rect)
        return action
