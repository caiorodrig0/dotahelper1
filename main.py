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


# MEDUSA
carry = 12
# SILENCER
mid = 76
# PUDGE
off = 36
# SK
sup4 = 0
# DISRUPTOR
sup5 = 0

start_overlay_config(138, [345001363, 293052390, 95825708, 280511288, 196931374, 1060164724, 247751328, 877402200, 316501737,
                          886742476, 97658618, 375507918, 321580662, 102458922],
                     [carry, mid, off, sup4, sup5])
