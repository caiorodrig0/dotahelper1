import tkinter as tk
import pyautogui
import time

imagem_path = '5.png'
# Criar uma janela sem borda com background transparente
root = tk.Tk()
root.overrideredirect(True)
root.wait_visibility(root)
root.attributes('-alpha', 0.7)

# Criar um label com o texto "Olá, mundo!"
label = tk.Label(root, text="Aguardando jogo iniciar...", font=("Arial", 9), bg='white')
label.pack()

# Exibir a janela sempre no topo
root.lift()
root.attributes("-topmost", True)
root.geometry("+%d+%d" % (0, 0))


def printrelogio():
    tempo_inicial = time.time()

    # espera 1 segundo
    time.sleep(1)

    # obtém o tempo atual
    tempo_atual = time.time()

    # calcula o tempo que passou
    tempo_decorrido = tempo_atual - tempo_inicial
    print(tempo_decorrido)


def atualizar_contador():
    regiao_busca = (586, 207, 76, 33)

    posicao = pyautogui.locateOnScreen(imagem_path, region=regiao_busca)
    print(posicao)
    if posicao:
        tempo_inicial = time.time()
        # label.configure(text="Posição: " + str(posicao))
        label['text'] = 'BUCETA!!!'
        # printrelogio()
        tempo_atual = time.time()
        print(tempo_atual - tempo_inicial)
    else:
        tempo_inicial = time.time()
        # label.configure(text="Aguardando nova ação...")
        label['text'] = 'CU!!!'
        tempo_atual = time.time()
        print(tempo_atual - tempo_inicial)
    root.after(10, atualizar_contador)


root.after(10, atualizar_contador)

# Iniciar o loop da janela
root.mainloop()
