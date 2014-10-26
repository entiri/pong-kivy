from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty,\
     ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock


class PongBall(Widget):
    
    #velocity of the ball on x and y axis
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    
    #referencelistproperty lets us use the ball's
    #velocity as a variable to be used for later.
    velocity = ReferenceListProperty(velocity_x, velocity_y)
    
    #the move function moves  the ball one step.
    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class PongPaddle(Widget):
    ''' This class is used for each player's paddle
    '''
    
    # Keep the score for each player
    score = NumericProperty(0)
    
    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            #Offset -- bando bando! (Migos > Beatles)
            # In all seriousness, the offset concerns how far off
            # the ball is from the paddle upon impact
            # (I think -- will update later)
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            
            # Set the vector for the ball upon impact with the paddle
            # Then increase the velocity by 0.1, and send the ball on its way
            bounced = Vector(-1 * vx, vy)
            vel = bounced * 1.1
            
            ball.velocity = vel.x, vel.y + offset


class PongGame(Widget):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)

    def serve_ball(self, vel=(4,0)):
        self.ball.center = self.center
        self.ball.velocity = vel

    def update(self, dt):
        #call ball.move and all that here.
        self.ball.move()
        
        #bouncing ball off of paddles
        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)
        
        #bounce the ball off the top and bottom
        if (self.ball.y < 0) or (self.ball.top > self.height):
            self.ball.velocity_y *= -1
        
        #if the ball goes to a side -- point scored
        if self.ball.x < self.x:
            self.player2.score += 1
            self.serve_ball(vel=(4, 0))
        if self.ball.x > self.width:
            self.player1.score += 1
            self.serve_ball(vel=(-4, 0))

    def on_touch_move(self, touch):
        '''
        Move the paddle. The paddle moved is dependent on the
        side the user is touching.
        '''
        if touch.x < self.width / 3:
            self.player1.center_y = touch.y
        if touch.x > self.width - self.width / 3:
            self.player2.center_y = touch.y

class PongApp(App):
    def build(self):
        game = PongGame()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1.0/60.0)
        return game

if __name__ == '__main__':
    PongApp().run()