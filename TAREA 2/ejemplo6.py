def celsius_a_fahrenheit(temp_c): #donde "temp_c" temperatura en grados celcius y "temp_f", en grados fahrenheit
    '''
    transforma temperatura de celsius a fahrenheit.
    Input: 
        temp_c:número float
    Ouput: 
        retorna: número float
    '''
    temp_f = 1.8*temp_c + 32
    return temp_f
    
    
    
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
    
def cambiar_hora(hora_lima,país):
    
    assert hora_lima <= 24
    
    
    hora_total= hora_lima + dic_horas[país]
   

    if  hora_total < 0:
        x= (12-hora_total)
        print("El día anterior a las", x, "horas")
    
    elif hora_total <= 24:
        y=hora_total
        print("Son las:", y)
        
    elif hora_total > 24:
        Z=hora_total-24
        print("Son la o las:", Z, "del día de mañana")
        
    return hora_total