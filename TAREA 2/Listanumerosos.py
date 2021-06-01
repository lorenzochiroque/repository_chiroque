def suma_lista(lista_numeros):
    '''
    Suma una lista de numeros y retorna un resultado condicional:

    Input: 
        lista_numeros: lista de números
    Ouput: 
        - Si es menor a 100: nada, solo un print
        - Si es mayor a 100: un número
    '''
    
    W = sum(lista_numeros)

    assert W >= 0

    if  W<= 100:
        x= 100 - W
        print("Monto faltante para 100:", x)
    
    elif W>100:
        print(W)

    return W