"""
Text input box in pygame
Source code taken from
https://stackoverflow.com/questions/46390231/how-can-i-create-a-text-input-box-with-pygame
"""
import pygame


class TextInputBox(pygame.sprite.Sprite):
    def __init__(self, x, y, w, font, comment="", text=""):
        super().__init__()
        self.color = (255, 255, 255)
        self.backcolor = None
        self.pos = (x, y)
        self.width = w
        self.font = font
        # self.active = False
        self.active = True
        self.text = text
        self.comment = comment
        self.render_text()

    def render_text(self):
        box_text = self.font.render(self.text, True, self.color, self.backcolor)
        box_comment = []
        box_width = max(self.width, 5 + 5 + box_text.get_width() + 5)
        box_height = 5 + box_text.get_height() + 5
        if isinstance(self.comment, tuple) or isinstance(self.comment, list):
            for comment in self.comment:
                box_comment.append(self.font.render(comment, True, self.color, self.backcolor))
                box_width = max(box_width, 5 + box_comment[-1].get_width() + 5)
                box_height += 5 + box_comment[-1].get_height() + 5
        else:
            box_comment.append(self.font.render(self.comment, True, self.color, self.backcolor))
            box_width = max(box_width, 5 + box_comment[-1].get_width() + 5)
            box_height += 5 + box_comment[-1].get_height() + 5
        self.image = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
        if self.backcolor:
            self.image.fill(self.backcolor)
        height = 5
        for comment in box_comment:
            self.image.blit(comment, (5 + (box_width - comment.get_width())/2, height))
            height += comment.get_height() + 5
        self.image.blit(box_text, (5 + (box_width - box_text.get_width())/2, height + 5))
        pygame.draw.rect(self.image, self.color, (5 + (box_width - box_text.get_width())/2 - 4,
                                                  height + 5 - 4,
                                                  box_text.get_width() + 8,
                                                  box_text.get_height() + 8), 2)
        # self.rect = self.image.get_rect(topleft=self.pos)
        self.rect = self.image.get_rect(center=self.pos)

    def update(self, event_list):
        for event in event_list:
            # if event.type == pygame.MOUSEBUTTONDOWN and not self.active:
            #     self.active = self.rect.collidepoint(event.pos)
            # if event.type == pygame.KEYDOWN and self.active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.active = False
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.render_text()