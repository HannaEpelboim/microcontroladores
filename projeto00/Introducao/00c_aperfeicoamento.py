from json import load
from turtle import *


# Copie as funções que você fez na Implementação aqui embaixo


def desenha_retangulo(x, y, comprimento, altura, cor):
    penup()
    goto(x,y)
    pendown()
    # retangulo
    fillcolor(cor) 
    begin_fill()
    for i in range(2):
        forward(comprimento)
        right(90)
        forward(altura)
        right(90)
    end_fill()
    setheading(0)
    return
    
    
def desenha_circulo(x, y, raio, cor):
    penup()
    goto(x,y-raio)
    setheading(0)
    pendown()
    fillcolor(cor) 
    begin_fill()
    # circulo
    circle(raio)
    end_fill()
    setheading(0)
    return
    
    
def desenha_poligono(lista_pontos, cor):
    penup()
    goto(lista_pontos[0]["x"],lista_pontos[0]["y"])
    pendown()
    # retangulo
    fillcolor(cor) 
    begin_fill()
    for ponto in lista_pontos:
        goto(ponto["x"], ponto["y"])
        right(90)
    goto(lista_pontos[0]["x"],lista_pontos[0]["y"])
    end_fill()
    setheading(0)
    return
    
    


# Faça a primeira parte do Aperfeiçoamento aqui

def desenha_todos(dicionario_do_pais):
    for pais in lista_de_paises:
        for elemento in pais["elementos"]:
            #print(elemento)
            #print(elemento["tipo"])
                if elemento["tipo"] == "retângulo":
                    desenha_retangulo(elemento["x"],elemento["y"],elemento["comprimento"], elemento["altura"], elemento["cor"])
                elif elemento["tipo"] == "polígono":
                    desenha_poligono(elemento["pontos"],elemento["cor"])
                else:
                    desenha_circulo(elemento["x"],elemento["y"],elemento["raio"],elemento["cor"])

    return

def desenha_bandeira(dicionario_do_pais):
    for elemento in dicionario_do_pais["elementos"]:
        if elemento["tipo"] == "retângulo":
            desenha_retangulo(elemento["x"],elemento["y"],elemento["comprimento"], elemento["altura"], elemento["cor"])
        elif elemento["tipo"] == "polígono":
            desenha_poligono(elemento["pontos"],elemento["cor"])
        else:
            desenha_circulo(elemento["x"],elemento["y"],elemento["raio"],elemento["cor"])

                
    return


lista_de_paises = load(open('paises.json', encoding="UTF-8"))
#desenha_bandeira(lista_de_paises[0])


# Faça a segunda parte do Aperfeiçoamento aqui

def desenhaPais(x,y):
    entrada = textinput("País", "Digite o nome do país")
    for pais in lista_de_paises:
        if pais["nome"] == entrada:
            desenha_bandeira(pais)

onscreenclick(desenhaPais)

#desenhaPais("Brasil")

# O desafio deve ser feito diretamente no JSON, não aqui!



# Mantém a janela do Turtle aberta
mainloop()