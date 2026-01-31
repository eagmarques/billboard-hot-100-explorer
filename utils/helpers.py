"""
Utilitários para validação e formatação de dados.
"""
from datetime import datetime
from typing import Tuple, Optional


def validate_date(year: int, month: int, max_year: int = 2021, max_month: int = 5) -> Tuple[bool, Optional[str]]:
    """
    Valida se a data fornecida é válida e está dentro do range do dataset.
    
    Args:
        year: Ano (ex: 2020)
        month: Mês (1-12)
        max_year: Ano máximo disponível no dataset
        max_month: Mês máximo do último ano
    
    Returns:
        Tuple[bool, Optional[str]]: (is_valid, error_message)
    """
    # Validação básica de range
    if not (1958 <= year <= max_year):
        return False, f"Ano deve estar entre 1958 e {max_year}"
    
    if not (1 <= month <= 12):
        return False, "Mês deve estar entre 1 e 12"
    
    # Validação especial para o último ano
    if year == max_year and month > max_month:
        return False, f"Para {max_year}, dados disponíveis apenas até Maio"
    
    # Valida se é uma data válida
    try:
        datetime(year, month, 1)
    except ValueError:
        return False, "Data inválida"
    
    return True, None


def format_chart_date(year: int, month: int) -> str:
    """
    Formata a data para o formato esperado pela Billboard API.
    
    Args:
        year: Ano
        month: Mês
    
    Returns:
        str: Data formatada (YYYY-MM-DD) do primeiro dia do mês
    """
    return f"{year}-{month:02d}-01"


def format_display_date(year: int, month: int) -> str:
    """
    Formata a data para exibição amigável ao usuário.
    
    Args:
        year: Ano
        month: Mês
    
    Returns:
        str: Data formatada (ex: "Janeiro de 2020")
    """
    meses = [
        "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
        "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
    ]
    return f"{meses[month - 1]} de {year}"