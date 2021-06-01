def numero_mixto(num, den):
    '''
    Convierte división en número mixto
    Input: 
        num: número entero
        den: número entero
    Ouput: 
        retorna: lista con 3 números
    '''
    Emtero=num//den
    fracción=(num%den)
    
    lst_result= [Emtero, fracción, den]
    

    return lst_result