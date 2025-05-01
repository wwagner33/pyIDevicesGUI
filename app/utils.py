def bytes_para_gb(bytes_val):
    """Converte bytes para gigabytes com 2 casas decimais."""
    return round(bytes_val / (1024 ** 3), 2)

def formatar_titulo(titulo):
    """Retorna um título capitalizado e centralizado."""
    return f"--- {titulo.strip().title()} ---"

def limpar_texto(texto):
    """Remove espaços extras e quebras de linha"""
    return " ".join(texto.strip().split())
