from kivy import *


from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput

class MyApp(App):

    def build(self):
        label_widget = Label( markup = True ) #Initialization like an object
        #this one works as a property
        label_widget.text= "[color=#ffa62b]This is [/color][color=#fcf876]Text[/color]"#Adding color by markup using [color] [/color] like in html
        label2 = Label(text="This is more text")
        #Everything works here as a class
        layout = GridLayout(cols=2)
        #bind -> bind a callback/function  to a widget, so it performs when something happened
        #Adding components to the layout
        layout.add_widget(label_widget)
        layout.add_widget(TextInput(multiline=False))
        layout.add_widget(label2)
        layout.add_widget(TextInput(multiline=False))
        return layout


if __name__ == '__main__':
    MyApp().run()