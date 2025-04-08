import streamlit as st
import pandas as pd
from models import Cliente, Endereco
from typing import List, Dict
from pydantic import ValidationError

st.set_page_config(page_title="Validação de Dados", layout="wide")

def validate_dataframe(df: pd.DataFrame, model_class) -> List[Dict]:
    """
    Valida cada linha do dataframe usando o modelo Pydantic especificado.
    Retorna uma lista de dicionários com os erros encontrados.
    """
    errors = []
    
    for idx, row in df.iterrows():
        try:
            model_class(**row.to_dict())
        except ValidationError as e:
            errors.append({
                'linha': idx + 1,
                'erros': e.errors()
            })
    
    return errors

def main():
    st.title("Validação de Dados de Clientes e Endereços")
    
    # Carregar os dataframes
    try:
        df_clientes = pd.read_csv('clientes_com_erros.csv')
        df_enderecos = pd.read_csv('enderecos_com_erros.csv')
    except FileNotFoundError:
        st.error("Arquivos CSV não encontrados. Por favor, execute primeiro o script de geração de dados.")
        return

    # Criar abas para separar as visualizações
    tab1, tab2 = st.tabs(["Clientes", "Endereços"])

    with tab1:
        st.header("Dados dos Clientes")
        
        # Mostrar dataframe
        st.subheader("Dados Brutos")
        st.dataframe(df_clientes)
        
        # Validar dados
        erros_clientes = validate_dataframe(df_clientes, Cliente)
        
        # Mostrar estatísticas
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total de Registros", len(df_clientes))
        with col2:
            st.metric("Registros com Erros", len(erros_clientes))
        with col3:
            st.metric("Taxa de Erros", f"{(len(erros_clientes)/len(df_clientes)*100):.1f}%")
        
        # Mostrar erros
        if erros_clientes:
            st.subheader("Erros Encontrados")
            for error in erros_clientes:
                with st.expander(f"Erros na Linha {error['linha']}"):
                    for err in error['erros']:
                        campo = err['loc'][0]
                        msg = err['msg']
                        st.error(f"Campo '{campo}': {msg}")
        else:
            st.success("Nenhum erro encontrado nos dados dos clientes!")

    with tab2:
        st.header("Dados dos Endereços")
        
        # Mostrar dataframe
        st.subheader("Dados Brutos")
        st.dataframe(df_enderecos)
        
        # Validar dados
        erros_enderecos = validate_dataframe(df_enderecos, Endereco)
        
        # Mostrar estatísticas
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total de Registros", len(df_enderecos))
        with col2:
            st.metric("Registros com Erros", len(erros_enderecos))
        with col3:
            st.metric("Taxa de Erros", f"{(len(erros_enderecos)/len(df_enderecos)*100):.1f}%")
        
        # Mostrar erros
        if erros_enderecos:
            st.subheader("Erros Encontrados")
            for error in erros_enderecos:
                with st.expander(f"Erros na Linha {error['linha']}"):
                    for err in error['erros']:
                        campo = err['loc'][0]
                        msg = err['msg']
                        st.error(f"Campo '{campo}': {msg}")
        else:
            st.success("Nenhum erro encontrado nos dados dos endereços!")

if __name__ == "__main__":
    main() 