from repositories.conciliacao_repository import ConciliacaoRepository
from views.conciliacoes_view import view_divergencias, view_conformidades, view_pesquisa_por_data, \
    view_pesquisa_a_partir_data, view_conciliacao_por_id, view_listar_conciliacoes


def mostrar_divergencias ():
    try:
        # INSTANCIANDO METODO DO SERVICE
        services = ConciliacaoRepository
        dados = services.listar_divergencias()

        view_divergencias(dados)
    except Exception as e:
        print(f"Erro inesperado: {e}")


def mostrar_conformidade():
    try:
        # INSTANCIANDO METODO DO SERVICE
        services = ConciliacaoRepository
        dados = services.listar_conformidadades()

        view_conformidades(dados)
    except Exception as e:
        print(f"Erro inesperado: {e}")


def pesquisar_por_data (data):
    try:
        # INSTANCIANDO METODO DO SERVICE
        services = ConciliacaoRepository
        dados = services.listar_conciliacao_por_data(data)

        view_pesquisa_por_data(dados)
    except Exception as e:
        print(f"Erro inesperado: {e}")



def pesquisar_a_partir_data (data):
    try:
        # INSTANCIANDO METODO DO SERVICE
        services = ConciliacaoRepository
        dados = services.listar_conciliacao_pos_data(data)

        view_pesquisa_a_partir_data(dados)
    except Exception as e:
        print(f"Erro inesperado: {e}")


def exibir_conciliacao_por_id (id_conciliacao):
    try:
        # INSTANCIANDO SERVICE
        service = ConciliacaoRepository
        dados = service.buscar_por_id(id_conciliacao)
        view_conciliacao_por_id(dados)
    except Exception as e:
        print(f"Erro inesperado: {e}")

def listar_conciliacoes():
    try:
        # INSTANCIANDO SERVICE
        service = ConciliacaoRepository
        dados = service.listar_todas()

        view_listar_conciliacoes(dados)
    except Exception as e:
        print(f"Erro inesperado: {e}")  