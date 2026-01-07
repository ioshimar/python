def calcula(lat):
    grados = int(lat)
    minutos = int((lat - grados) * 60)
    segundos = round((((lat - grados) * 60) - minutos) * 60 * 100000)
    if segundos == 600000:
            segundos = 0
            minutos += 1
    elif segundos >= 1000000:
            segundos -= 1000000
            minutos += 1
    if minutos >= 60:
            minutos = 0
            grados += 1
    return "{:0>3}{:0>2}{:0>6}".format(grados, minutos, segundos)

latit = 102.34704930340318

media = calcula(latit)
print(f"grados {media}")
print("Programa terminado")