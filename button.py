import pygame

# Button class
class Button():
    def __init__(self, x, y, image, image2, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.image2 = pygame.transform.scale(image2, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.pressed_image_active = False  # Track whether the pressed image is displayed
    def res(self):
        action = False
        self.clicked = False
        self.pressed_image_active = False
        
    def draw(self, surface):
        action = False
        pos = pygame.mouse.get_pos()
        
        # Check if the mouse is over the button
        if self.rect.collidepoint(pos):
            # Check if the button is being clicked
            if pygame.mouse.get_pressed()[0] and not self.clicked:
                self.clicked = True
                self.pressed_image_active = True
                action = True
            elif not pygame.mouse.get_pressed()[0]:  # Mouse is released
                self.clicked = False
                self.pressed_image_active = False

        # Display the pressed image if button is in clicked state
        if self.pressed_image_active:
            surface.blit(self.image2, (self.rect.x, self.rect.y))
        else:
            # Display the default image
            surface.blit(self.image, (self.rect.x, self.rect.y))
    
    
    
        
        return action