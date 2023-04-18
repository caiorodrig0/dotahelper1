import os

diretorio_pai = "C:\\Users\\caio.rodrigo.santos\\IdeaProjects\\c6-novo\\auto.adm.renegotiation.app\\src" # Substitua pelo caminho do diretório pai

for diretorio_atual, subdiretorios, arquivos in os.walk(diretorio_pai):
    for nome_arquivo in arquivos:
        if nome_arquivo.endswith(".java"):
            novo_nome = nome_arquivo.replace(".java", ".txt")
            caminho_original = os.path.join(diretorio_atual, nome_arquivo)
            caminho_novo = os.path.join(diretorio_atual, novo_nome)
            os.rename(caminho_original, caminho_novo)
