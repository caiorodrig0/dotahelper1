import tkinter as tk
from overlay.overlayfunctions import inicia_overlay

imagem_path = '5.png'
root = tk.Tk()


def start_overlay_config(hero_id, players, heroes_against):
    # Criar uma janela sem borda com background transparente

    root.overrideredirect(True)
    root.wait_visibility(root)
    root.attributes('-alpha', 0.7)
    root.maxsize(width=220, height=550)

    # Criar um label com o texto "Olá, mundo!"
    label = tk.Label(root, text="Aguardando jogo iniciar...", font=("Arial", 8), bg='white', width=220, anchor="w")
    label.config(wraplength=220)
    label.pack()

    # Exibir a janela sempre no topo
    root.lift()
    root.attributes("-topmost", True)
    root.geometry("+%d+%d" % (0, 0))

    root.bind("<f>", toggle_overlay)

    root.after(1, inicia_overlay(imagem_path=imagem_path, root=root, label=label, hero_id=hero_id, players=players,
                                 heroes_against=heroes_against))

    # Iniciar o loop da janela
    #root.mainloop()


def toggle_overlay(event):
    if root.winfo_height() == 30:  # Se o overlay estiver retraído
        root.geometry("220x550")  # Expandir o overlay
    else:  # Se o overlay estiver expandido
        root.geometry("200x30")  # Retrair o overlay
