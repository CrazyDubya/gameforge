from ball import Ball
from paddle import Paddle


class Game:
    def __init__(self, window_width, window_height):
        self.window_width = window_width
        self.window_height = window_height
        self.player_paddle = Paddle(20, window_height // 2, 10, 80)
        self.ball = Ball(window_width // 2, window_height // 2, 10, 10)
        self.score = 0

    def update(self):
        self.player_paddle.update()
        self.ball.update()
        # Check collision with paddle
        if self.ball.rect.colliderect(self.player_paddle.rect):
            self.ball.bounce()
        # Check collision with window edges
        if self.ball.rect.left <= 0 or self.ball.rect.right >= self.window_width:
            self.ball.reverse_x()
        if self.ball.rect.top <= 0 or self.ball.rect.bottom >= self.window_height:
            self.ball.reverse_y()

    def render(self, window):
        self.player_paddle.render(window)
        self.ball.render(window)
