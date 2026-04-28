from repositories.nota_fiscal_repository import NotaFiscalRepository
from views.nota_fiscal_view import view_exibir_por_id, view_exibir_todos


def exibir_nota (id_nf):
    try:
        # INSTANCIANDO SERVICES
        service = NotaFiscalRepository
        dados = service.exibir_nota(id_nf)
        view_exibir_por_id(dados)
    except Exception as e:
        print(f"Erro inesperado: {e}")

def listar_notas():
    try:
        # INSTANCIANDO SERVICE
        service = NotaFiscalRepository
        dados = service.listar_todas()

        view_exibir_todos(dados)
    except Exception as e:
        print(f"Erro inesperado: {e}")