import tkinter as tk

# Criar uma janela sem borda com background transparente
root = tk.Tk()
root.overrideredirect(True)
root.wait_visibility(root)
root.attributes('-alpha', 0.7)

# cria um widget de texto
texto = tk.Text(root, wrap=tk.WORD, state='disabled')

# adiciona o texto ao widget de texto
texto.insert(tk.END,
             "Este é um exemplo de texto longo que será quebrado em várias linhas caso ele ultrapasse o tamanho do widget.")


# posiciona o widget de texto na janela
texto.pack()

# Exibir a janela sempre no topo
root.lift()
root.attributes("-topmost", True)
root.geometry("+%d+%d" % (0, 0))
root.maxsize(width=220, height=550)

# Função para alternar o tamanho do overlay
def toggle_overlay(event):
    if root.winfo_height() == 30:  # Se o overlay estiver retraído
        root.geometry("220x550")  # Expandir o overlay
    else:  # Se o overlay estiver expandido
        root.geometry("200x30")
        # Retrair o overlay


root.bind("<f>", toggle_overlay)

# Iniciar o loop da janela
root.mainloop()
