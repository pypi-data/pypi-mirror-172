def armazenar(dados):
    with open("dados_usuario.txt", "a") as arq:
        arq.writelines(dados)
        arq.writelines("\n")
        arq.close()
