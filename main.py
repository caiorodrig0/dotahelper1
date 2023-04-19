import time
from playsound import playsound
from overlay.configoverlay import start_overlay_config


def printrelogio():
    tempo_inicial = time.time()

    # espera 1 segundo
    time.sleep(1)

    # obtém o tempo atual
    tempo_atual = time.time()

    # calcula o tempo que passou
    tempo_decorrido = tempo_atual - tempo_inicial

    if 50 < tempo_decorrido <= 59:
        playsound('count.mp3.mp3')
    elif tempo_decorrido == 60:
        tempo_decorrido = 0


start_overlay_config(67, 345001363)
