from pacotebanco import Armazenamento, Consulta, Interacao

from time import sleep

usuarios = []
run = True

print("---" * 20)
print("Bem-Vindo ao \033[35mBANCO DE USUARIOS\033[m"
      "\nO que deseja fazer?\n"
      "\033[32m[1]-Cadastrar novo Usuario.\033[m\n"
      "\033[34m[2]-Consultar CPF.\033[m\n"
      "\033[31m[3]-Sair\033[m")
print("---" * 20)

while run:
    escolha = int(input(""))

    if escolha == 1:
        dados = Interacao.interagir()
        usuarios.append(dados)
        usuarios.append("\n")
        Armazenamento.armazenar(dados)
        print("Processando...")
        sleep(2)
        print("-" * 14, "Cadastro realizado com sucesso!", "-" * 13)
        sleep(1.5)
    elif escolha == 2:
        print("CPF - NOME - ENDERECO:")
        Consulta.consultar()
        print("-" * 21, "Fim da Consulta", "-" * 22)
        sleep(1.5)
    elif escolha == 3:
        print("Finalizando...")
        sleep(2)
        print("FIM!")
        run = False
        break
    else:
        print("Escolha invalida!")
        sleep(1.5)

    print("---" * 20)
    print("O que deseja fazer?\n"
          "\033[32m[1]-Cadastrar novo Usuario.\033[m\n"
          "\033[34m[2]-Consultar CPF.\033[m\n"
          "\033[31m[3]-Sair\033[m")
    print("---" * 20)
