"""
A kv file has been created, it has to have the same name as the widget, to handle
all the propierties of the application
https://kivy.org/doc/stable/tutorials/pong.html


"""


from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty
)
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.core.window import Window #Allows to manipulate or attach things to the window
#and also allows to import the keybinding method




class PongBall(Widget):
    #velocity of the ball in the x and y axis
    velocity_x = NumericProperty(0) #NumericPropertu is something that belongs to Kivy
    velocity_y = NumericProperty(0)

    #ReferenceListPrperty allow to use ball.velocitu as a shorthand, chaining the properties
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    #This function moves the ball one step
    #This will be called in regular intervales to animate the ball
    def move(self):
        self.pos = Vector(*self.velocity)+self.pos #using * we unpack the arguments

class PongPaddle(Widget):
    score = NumericProperty(0)

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height/2)
            bounced = Vector(-1 * vx, vy)
            vel = bounced * 1.1
            ball.velocity = vel.x, vel.y + offset


class PongGame(Widget): #root widget
    ball = ObjectProperty(None) #Allows to refer and bind an object created in the  kv file
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)

    #With this modification, the game can be used without the touch function
    #THis will allow to play with the kewboard
    def __init__(self, **kwargs):
        super(PongGame, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self.__keyboard_closed, self)#giving access to the keyboard
        self._keyboard.bind(on_key_down=self._on_keyboard_down)#binds the keyboard to make it accesible to the pressed

    def __keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down) #The selected keys get liberated from their hold
        self._keyboard = None #Clear the keyboard request

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == "w": #Toma el elemetno presionado y verifica cual tecla y accion corresponde
            self.player1.center_y += 25
        elif keycode[1] == "s":
            self.player1.center_y -= 25
        elif keycode[1] == "up":
            self.player2.center_y += 25
        elif keycode[1] == "down":
            self.player2.center_y -= 25


    def serve_ball(self, vel=(4,0)):
        self.ball.center = self.center
        self.ball.velocity = vel #assings a random position to the ball and resets it's for serving


    def update(self,dt):
        self.ball.move()

        #Bounce off paddles
        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)
        # Bounce off top and bottom
        if(self.ball.y < 0) or (self.ball.top > self.height):
            self.ball.velocity_y *= -1
        #Bounce off left and right
        # if(self.ball.x < 0) or (self.ball.right > self.width):
        #    self.ball.velocity_x *= -1
        #adding points
        if self.ball.x < self.x:
            self.player2.score += 1
            self.serve_ball(vel=(4,0))
        elif self.ball.x > self.width:
            self.player1.score += 1
            self.serve_ball(vel=(-4,0))

    #this is a inherited method
    def on_touch_move(self, touch):
        if touch.x < self.width / 3:
            self.player1.center_y = touch.y
        if touch.x > self.width - self.width / 3:
            self.player2.center_y = touch.y


class PongApp(App): #app root, control the main frame, just return the class that handle all the actions
    def build(self):
        game = PongGame()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1.0/60.0 ) #This function executes the func that is passed the amount of times
        #the interval ask for, in this case is one each second or 60 times per minute
        return game


if __name__ == '__main__':
    PongApp().run()
