def converter_para_segundos(tempo):
    if tempo == None:
        return 0
    dias, horas, minutos = tempo
    total_segundos = dias * 86400 + horas * 3600 + minutos * 60
    return total_segundos

def converter_de_segundos(segundos):
    if segundos == None:
        return [0, 0, 0]
    dias = segundos // 86400
    segundos_restantes = segundos % 86400
    horas = segundos_restantes // 3600
    segundos_restantes %= 3600
    minutos = segundos_restantes // 60
    return dias, horas, minutos