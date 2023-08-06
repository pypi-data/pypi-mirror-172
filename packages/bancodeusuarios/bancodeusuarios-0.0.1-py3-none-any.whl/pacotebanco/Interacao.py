def interagir() -> list:
    cpf = str(input("Digite seu CPF: "))
    nome = str(input("Digite seu nome: "))
    endereco = str(input("Digite seu endereco: "))

    info = [cpf, "-", nome, "-", endereco]
    return info
