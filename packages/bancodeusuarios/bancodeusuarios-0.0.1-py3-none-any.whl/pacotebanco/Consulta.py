def consultar():
    with open("dados_usuario.txt", "r") as arq:
        usuarios = arq.readlines()
        cpfC = str(input("Digite seu CPF: "))

        for i in usuarios:
            if cpfC in i:
                print(i)

        arq.close()
