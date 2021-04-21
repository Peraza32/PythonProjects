
from collections import deque

#This will determine with sign has greater precedence, and return a bolean
#True if the sign in the stack has lower precedence, False otherwise
def prioridadDeSigno(actual_sign, queued_sign):
    val_ac = 0 #Let's suppose that the basic sign is + or -
    val_q = 0
    if actual_sign == "*" or actual_sign == "/":
        val_ac = 1
    if queued_sign == "*" or queued_sign == "/":
        val_q = 1

    #Then, let's check preference
    if val_ac  < val_q:
        return True
    else:
        return False

#hate weak types
def numberConversion(numero):
    if "." in numero:
        return float(numero)
    else:
        return int(numero)


def operaciones(num_right, num_left, operand):
    if operand == "+":
        return num_left + num_right
    elif operand == "-":
        return num_left - num_right
    elif operand == "*":
        return num_left * num_right
    elif operand == "/":
        if num_right == 0 or num_right == 0.0:
            raise Exception("Division between zero")
        return num_left / num_right

#this funtion will allow to check that the parenthesis in the expression are well used
#it tolerates one orpham (
def checkingParenthesis(cadena):
    cstack = deque()
    for c in cadena:
        if c == "(":
            cstack.append(c)
        elif c == ")":
            if cstack:
                cstack.pop()
            else:
                return False

    if  not cstack:
        return True
    elif cstack[-1] == "(":
        return True
    else:
        return False


def isOperator(value):
    if value == "+" or value == "-" or value == "*" or value == "/":
        return True
    else:
        return False


def isUnary(last_val):
    if str.isdigit(last_val):
        return False
    else:
        return True