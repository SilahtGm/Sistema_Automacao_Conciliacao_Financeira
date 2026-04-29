from datetime import datetime


def validar_data_especifica(data_str):
    try:
        # CONVERTENDO A DATA RECEBIDA EM DATA NO FORMATO YYYY-MM-DD
        data_obj = datetime.strptime(data_str, "%d-%m-%Y")

        # IMPEDE QUE A DATA SELECIONADA SEJA UMA DATA FUTURA
        if data_obj.date() > datetime.now().date():
            raise ValueError("Data não pode ser futura.")

        # RETORNANDO O OBJETO EM UMA STRINF
        return data_obj.strftime("%d-%m-%Y")
    # EM CASO DE ERRO (VALUEERROR - VALOR NO FORMATO ERRADO)
    except ValueError:
        raise ValueError("Data inválida. Use o formato DD-MM-YYYY.")