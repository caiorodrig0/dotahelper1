import tkinter as tk
import pyautogui
import time
from playsound import playsound

imagem_path = '0.png'
# Criar uma janela sem borda com background transparente
root = tk.Tk()
root.overrideredirect(True)
root.wait_visibility(root)
root.attributes('-alpha', 0.7)

# Criar um label com o texto "Olá, mundo!"
label = tk.Label(root, text="Aguardando jogo iniciar...", font=("Arial", 8), bg='white')
label.pack()

# Exibir a janela sempre no topo
root.lift()
root.attributes("-topmost", True)
root.geometry("+%d+%d" % (0, 300))


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


printrelogio()

#Box(left=1229, top=156, width=78, height=5)
def atualizar_contador():
    regiao_busca = (1340, 1038, 28, 25)
    posicao = pyautogui.locateOnScreen(imagem_path)

    if posicao:
        print(posicao)
        label['text'] = '1 - Agrar creeps na lane (treinar esse conceito & last hit)\n2 - Farmar o little camp sempre ' \
                        'que possível e ir farmando a jungle na side lane\n3- Caso a lane esteja dificil e tenha o item ' \
                        'de farm, farmar ancient + lane do top\n4- Caso a primeira torre do top tiver caído, ' \
                        'farmar jungle do time inimigo, caso não, cogitar farmar propria jungle\n5- Wardar a jungle ' \
                        'inimiga'
        printrelogio()
    else:
        label['text'] = 'Aguardando inicio do jogo...'
        root.after(10, atualizar_contador)


root.after(10, atualizar_contador)

# Iniciar o loop da janela
root.mainloop()
