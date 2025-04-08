import pandas as pd
from models import Cliente, Endereco
from typing import List, Dict
from pydantic import ValidationError

def validate_dataframe(df: pd.DataFrame, model_class) -> List[Dict]:
    """
    Valida cada linha do dataframe usando o modelo Pydantic especificado.
    Retorna uma lista de dicionários com os erros encontrados.
    """
    errors = []
    
    for idx, row in df.iterrows():
        try:
            # Converte a linha do dataframe para dicionário e valida
            model_class(**row.to_dict())
        except ValidationError as e:
            errors.append({
                'linha': idx + 1,  # +1 porque o índice começa em 0
                'erros': e.errors()
            })
    
    return errors

def print_validation_errors(errors: List[Dict]):
    """
    Imprime os erros de validação de forma legível
    """
    if not errors:
        print("Nenhum erro de validação encontrado!")
        return
    
    print("\nErros de validação encontrados:")
    for error in errors:
        print(f"\nLinha {error['linha']}:")
        for err in error['erros']:
            campo = err['loc'][0]
            msg = err['msg']
            print(f"  - Campo '{campo}': {msg}")

# Carregar os dataframes
df_clientes = pd.read_csv('output/clientes_com_erros.csv')
df_enderecos = pd.read_csv('output/enderecos_com_erros.csv')

# Validar dados dos clientes
print("Validando dados dos clientes...")
erros_clientes = validate_dataframe(df_clientes, Cliente)
print_validation_errors(erros_clientes)

# Validar dados dos endereços
print("\nValidando dados dos endereços...")
erros_enderecos = validate_dataframe(df_enderecos, Endereco)
print_validation_errors(erros_enderecos) 