from db.init_db import inicializar_banco
from services.conciliacao_service import listar_conciliacoes, mostrar_divergencias, mostrar_conformidade, \
    pesquisar_por_data, pesquisar_a_partir_data, exibir_conciliacao_por_id
from services.csv_service import gerar_dados
from services.lancamentos_service import listar_lancamentos, exibir_lancamento
from services.nota_fiscal_service import listar_notas, exibir_nota
from interfaces.utils_interface import pausar

def menu_inicial():
    while True:
        print("===========================================================")
        print("     SACF - Sistema de Automação de Conciliação Financeira")
        print("===========================================================")
        print("1 - ACESSAR")
        print("0 - ENCERRAR")
        print("===========================================================")
        op = input("Digite a opção desejada: ")
        match op:
            case "1":
                inicializar_banco()
                menu_principal()
            case "0":
                print("\nEncerrando sistema...")
                break
            case _:
                print("\nOpção inválida!")
                pausar()


def menu_principal():
    while True:
        print("===========================================================")
        print("     SACF - Sistema de Automação de Conciliação Financeira")
        print("===========================================================")
        print("1 - Área Operacional")
        print("2 - Área Administrativa")
        print("0 - Voltar")
        print("===========================================================")

        opcao = input("Digite a opção desejada: ")

        match opcao:
            case "1":
                menu_operacional()
            case "2":
                menu_administrativo()
            case "0":
                print("\nEncerrando sistema...")
                break
            case _:
                print("\nOpção inválida!")
                pausar()




def menu_administrativo():
    while True:
        print("===========================================================")
        print("                ÁREA ADMINISTRATIVA - SACF")
        print("===========================================================")
        print("1 - Carregar Dados dos CSVs")
        print("2 - Listar Todas as Notas Fiscais")
        print("3 - Listar Todos os Lançamentos")
        print("4 - Listar Todas as Conciliações")
        print("0 - Voltar")
        print("===========================================================")

        opcao = input("Digite a opção desejada: ")

        match opcao:
            case "1":
                gerar_dados()
                pausar()
            case "2":
                listar_notas()
                pausar()
            case "3":
                listar_lancamentos()
                pausar()
            case "4":
                listar_conciliacoes()
                pausar()
            case "0":
                break
            case _:
                print("\nOpção inválida!")
                pausar()


def menu_operacional():
    while True:
        print("===========================================================")
        print("                  ÁREA OPERACIONAL - SACF")
        print("===========================================================")
        print("1 - Mostrar Divergências")
        print("2 - Mostrar Conformidades")
        print("3 - Pesquisar Conciliações por Data")
        print("4 - Pesquisar Conciliações a partir de Data")
        print("5 - Exibir Nota Fiscal")
        print("6 - Exibir Lançamento Contábil")
        print("7 - Exibir Conciliação")
        print("0 - Voltar")
        print("===========================================================")

        opcao = input("Digite a opção desejada: ")

        match opcao:
            case "1":
                mostrar_divergencias()
                pausar()
            case "2":
                mostrar_conformidade()
                pausar()
            case "3":
                data = input("Digite a data (DD-MM-YYYY): ")
                pesquisar_por_data(data)
                pausar()
            case "4":
                data = input("Digite a data inicial (DD-MM-YYYY): ")
                pesquisar_a_partir_data(data)
                pausar()
            case "5":
                id_nf = input("Digite o ID da Nota Fiscal: ")
                exibir_nota(id_nf)
                pausar()
            case "6":
                id_lc = input("Digite o ID do Lançamento: ")
                exibir_lancamento(id_lc)
                pausar()
            case "7":
                id_conc = input("Digite o ID da Conciliação: ")
                exibir_conciliacao_por_id(id_conc)
                pausar()
            case "0":
                break
            case _:
                print("\nOpção inválida!")
                pausar()