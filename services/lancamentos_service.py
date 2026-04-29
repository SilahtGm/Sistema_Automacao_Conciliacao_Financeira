from repositories.lancamento_repository import LancamentoContabilRepository
from views.lancamentos_view import view_exibir_lancamento, view_listar_lancamento


def exibir_lancamento(id_lc):
    try:
        # INSTANCIANDO SERVICES
        service = LancamentoContabilRepository()
        dados = service.buscar_por_id(id_lc)
        view_exibir_lancamento(dados)
    except Exception as e:
        print(f"Erro inesperado: {e}")

def listar_lancamentos():
    try:
        # INSTANCIANDO SERVICE
        service = LancamentoContabilRepository()
        dados = service.listar_todas()

        view_listar_lancamento(dados)
    except Exception as e:
        print(f"Erro inesperado: {e}")