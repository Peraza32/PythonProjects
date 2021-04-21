"""
A kv file has been created, it has to have the same name as the widget, to handle
all the propierties of the application
https://kivy.org/doc/stable/tutorials/pong.html


"""


from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock

class PongGame(Widget): #root widget
    ball = ObjectProperty(None) #Allows to refer and bind an object created in the  kv file

    def update(self,dt):
       self.ball.move()
    #Bounce off top and bottom
        if(self.ball.y < 0) or (self.ball.top > self.height):
            self.ball.velocity_y *= -1

        #Bounce off left and right
        if(self.ball.x < 0) or (self.ball.right > self.width):
            self.ball.velocity_x *= -1

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


class PongApp(App): #app root, control the main frame, just return the class that handle all the actions
    def build(self):
        game = PongGame()
        Clock.schedule_interval(game.update, 1.0/60.0 ) #This function executes the func that is passed the amount of times
        #the interval ask for, in this case is one each second or 60 times per minute
        return game


if __name__ == '__main__':
    PongApp().run()

