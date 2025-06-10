from turtle import *


# Desenhe o que foi solicitado no enunciado do PDF aqui embaixo

def escreveCoordenadas(x,y):
    penup()
    goto(x,y)
    pendown()
    write("x = " + str(x) + "y = " + str(y))
penup()
goto(-100,200)
pendown()
# retangulo
for i in range(2):
    forward(100)
    right(90)
    forward(50)
    right(90)

penup()
goto(202,60)
setheading(0)
pendown()

# triangulo
for i in range(3):
    forward(50)
    left(120)
    
penup()
goto(-100,-150)
setheading(0)
pendown()

# circulo
circle(50)

penup()
goto(-300,-50)
setheading(0)
pendown()

# espiral

for i in range(25):
    circle(10+(i*4),30)

onscreenclick(escreveCoordenadas)


# Mantém a janela do Turtle aberta
mainloop()