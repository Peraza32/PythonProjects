#Creacion de una calculadora basica, como primero mini proyecto

from kivy import *
from PostFixMethods import *
from collections import deque


from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout


class Calculator(App):
    def build(self):

        #This is the queue that will store the infix expression
        queue = deque()
        stack = deque()
        #Containers for the calculator
        main_box = BoxLayout(orientation = "vertical")
        grid = GridLayout(cols=4)

        result= Label(size_hint_y = None, text="")

        #Creating all the Button
        signs = ("1","2","3", "+","4","5","6","-", "7","8","9","*", ".","0","/","(", ")", "=")

        for i in range(len(signs)):
            grid.add_widget(Button(text=str(signs[i])))
        #There are 2 ways to add the text in the calculator results
        #first lets define the long way with a function for the callback
        def print_button_text(instance): #Instance is the object that is using it
            result.text+=instance.text
        #we go over all the childs inside the gridlayout
        for button in grid.children[1:]: #The ``children` property is available on any Widget, and holds a list of all the widgets added to it, in reverse order.
            button.bind(on_press=print_button_text)


        # This function add to the queue the number and the respective symbol

        def parsingtoqueue(instance):
            value = result.text
            last_input = ""
            try:
                # Sanity check for parenthesis
                good_exp = checkingParenthesis(value)
                if good_exp == True:
                    # This code adds the numbers to the queue and the signs to the stack
                    temp = ""
                    unary = False #This is a flag that indicates if a value is a unary
                    for v in value:
                        if str.isdigit(v) or v == ".":
                            if unary == True:
                                temp += "-"+v
                                last_input = v
                                unary = False
                            else:
                                temp += v
                                last_input = v
                        else:
                            if v == "(" and temp == "":  # Caso donde se empiece con un (
                                stack.append(v)
                                last_input = v
                            elif temp != "":  # Cualquier caso que no sea "(" al inicio
                                # addng to the queue the number and the sign
                                queue.append(numberConversion(temp))
                                if stack and v == ")":
                                    p = stack.pop()
                                    while p != "(":
                                        queue.append(p)
                                        if stack:
                                            p = stack.pop()
                                        else:
                                            break
                                elif stack and v != "(":  # if the stack is not empty, then the priority is check
                                    res = prioridadDeSigno(v, stack[-1])
                                    if res:
                                        queue.append(stack.pop())
                                        stack.append(v)
                                    else:
                                        stack.append(v)
                                else:
                                    stack.append(v)

                                temp = ""
                                if (last_input == ")" or str.isdigit(last_input)) and v == "(":
                                    queue.append("*")
                                last_input = v
                            elif temp == "" and isOperator(v):
                                if isUnary(last_input):
                                    unary = True
                                else:
                                    stack.append(v)
                            else:
                                print("The input is empty")
                    # with the previous method, the last digit didn't get added so it's added here
                    # Hope it's works
                    if temp != "":
                        queue.append(numberConversion(temp))
                    temp = ""  # I'm emptying thw variable just cause
                    while stack:
                        queue.append(stack.pop())  # All the signs are added to the queue to create the ppostfix expression

                    # ------------------------------------------------------#
                    # In this section I'm  going to calculate the result of the expression

                    while queue:
                        actual_v = queue.popleft()
                        if type(actual_v) == float or type(actual_v) == int:
                            stack.append(actual_v)
                        else:
                            # we take teo numbers at a time
                            right_n = stack.pop()
                            left_n = stack.pop()
                            # the result of the operations are return to the stack
                            stack.append(operaciones(right_n, left_n, actual_v))
                    # the result is shown
                    result.text = str(stack.pop())
                else:
                    result.text = "SYNTAX ERROR"
                    raise Exception("Bad Input")

            except Exception as e:
                print(e)



        #Implementing the function in the = value
        grid.children[0].bind(on_press = parsingtoqueue)
        


        #Clearing method
        def clear(instance): #always pass instance, since this tell who is performing the action
            result.text=""


        #Adding widgets to the boxlayout
        main_box.add_widget(result)
        main_box.add_widget(grid)
        main_box.add_widget(Button(text="Clear", size_hint_y = None))

        main_box.children[0].bind(on_press = clear)

        return main_box


if __name__ == '__main__':
    Calculator().run()