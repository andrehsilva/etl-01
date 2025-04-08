import streamlit as st
import pandas as pd
from models import Cliente, Endereco
from typing import List, Dict, Set
from pydantic import ValidationError
import io

st.set_page_config(page_title="Validador de Dados", layout="wide")

def get_required_fields(model_class) -> Set[str]:
    """
    Retorna o conjunto de campos obrigatórios do modelo Pydantic
    """
    return {name for name, field in model_class.model_fields.items() if field.is_required}

def validate_columns(df: pd.DataFrame, model_class) -> List[str]:
    """
    Valida se todas as colunas obrigatórias existem no dataframe
    Retorna lista de erros encontrados
    """
    required_fields = get_required_fields(model_class)
    df_columns = set(df.columns)
    missing_columns = required_fields - df_columns
    
    errors = []
    if missing_columns:
        errors.append(f"Colunas obrigatórias faltando: {', '.join(missing_columns)}")
    
    return errors

def validate_dataframe(df: pd.DataFrame, model_class) -> List[Dict]:
    """
    Valida cada linha do dataframe usando o modelo Pydantic especificado.
    Retorna uma lista de dicionários com os erros encontrados.
    """
    errors = []
    
    # Primeiro valida as colunas
    column_errors = validate_columns(df, model_class)
    if column_errors:
        return [{'linha': 0, 'erros': [{'loc': ('colunas',), 'msg': error}]} for error in column_errors]
    
    # Depois valida os dados
    for idx, row in df.iterrows():
        try:
            model_class(**row.to_dict())
        except ValidationError as e:
            errors.append({
                'linha': idx + 1,  # Índice começa em 0, mas mostramos começando em 1
                'erros': e.errors()
            })
    
    return errors

def display_dataframe_with_index(df: pd.DataFrame):
    """
    Exibe o dataframe com uma coluna de índice começando em 1
    """
    df_display = df.copy()
    df_display.insert(0, 'Nº Linha', range(1, len(df) + 1))
    return df_display

def main():
    st.title("Validador de Dados de Clientes e Endereços")
    
    # Upload de arquivos
    st.header("Upload de Arquivos")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Arquivo de Clientes")
        clientes_file = st.file_uploader("Selecione o arquivo CSV de clientes", type=['csv'])
    
    with col2:
        st.subheader("Arquivo de Endereços")
        enderecos_file = st.file_uploader("Selecione o arquivo CSV de endereços", type=['csv'])
    
    if clientes_file is not None or enderecos_file is not None:
        # Processar arquivo de clientes
        if clientes_file is not None:
            try:
                df_clientes = pd.read_csv(clientes_file)
                st.session_state['df_clientes'] = df_clientes
            except Exception as e:
                st.error(f"Erro ao ler arquivo de clientes: {str(e)}")
        
        # Processar arquivo de endereços
        if enderecos_file is not None:
            try:
                df_enderecos = pd.read_csv(enderecos_file)
                st.session_state['df_enderecos'] = df_enderecos
            except Exception as e:
                st.error(f"Erro ao ler arquivo de endereços: {str(e)}")
        
        # Criar abas para visualização e validação
        if 'df_clientes' in st.session_state or 'df_enderecos' in st.session_state:
            tab1, tab2 = st.tabs(["Clientes", "Endereços"])
            
            with tab1:
                if 'df_clientes' in st.session_state:
                    st.header("Dados dos Clientes")
                    
                    # Mostrar dataframe com índice
                    st.subheader("Dados Brutos")
                    df_clientes_display = display_dataframe_with_index(st.session_state['df_clientes'])
                    st.dataframe(df_clientes_display, hide_index=True)
                    
                    # Mostrar colunas do arquivo
                    st.subheader("Colunas do Arquivo")
                    st.write("Colunas encontradas:", ", ".join(df_clientes.columns))
                    
                    # Botão para validar
                    if st.button("Validar Dados dos Clientes"):
                        erros_clientes = validate_dataframe(st.session_state['df_clientes'], Cliente)
                        
                        # Mostrar estatísticas
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Total de Registros", len(st.session_state['df_clientes']))
                        with col2:
                            st.metric("Registros com Erros", len(erros_clientes))
                        with col3:
                            st.metric("Taxa de Erros", f"{(len(erros_clientes)/len(st.session_state['df_clientes'])*100):.1f}%")
                        
                        # Mostrar erros
                        if erros_clientes:
                            st.subheader("Erros Encontrados")
                            for error in erros_clientes:
                                with st.expander(f"Erros na Linha {error['linha']}"):
                                    if error['linha'] == 0:
                                        # Erro de colunas
                                        for err in error['erros']:
                                            st.error(err['msg'])
                                    else:
                                        # Mostrar a linha completa com os dados
                                        linha_data = df_clientes_display[df_clientes_display['Nº Linha'] == error['linha']].iloc[0]
                                        st.write("Dados da linha:")
                                        st.dataframe(linha_data.to_frame().T, hide_index=True)
                                        
                                        # Mostrar os erros
                                        st.write("Erros encontrados:")
                                        for err in error['erros']:
                                            campo = err['loc'][0]
                                            msg = err['msg']
                                            st.error(f"Campo '{campo}': {msg}")
                        else:
                            st.success("Nenhum erro encontrado nos dados dos clientes!")
            
            with tab2:
                if 'df_enderecos' in st.session_state:
                    st.header("Dados dos Endereços")
                    
                    # Mostrar dataframe com índice
                    st.subheader("Dados Brutos")
                    df_enderecos_display = display_dataframe_with_index(st.session_state['df_enderecos'])
                    st.dataframe(df_enderecos_display, hide_index=True)
                    
                    # Mostrar colunas do arquivo
                    st.subheader("Colunas do Arquivo")
                    st.write("Colunas encontradas:", ", ".join(df_enderecos.columns))
                    
                    # Botão para validar
                    if st.button("Validar Dados dos Endereços"):
                        erros_enderecos = validate_dataframe(st.session_state['df_enderecos'], Endereco)
                        
                        # Mostrar estatísticas
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Total de Registros", len(st.session_state['df_enderecos']))
                        with col2:
                            st.metric("Registros com Erros", len(erros_enderecos))
                        with col3:
                            st.metric("Taxa de Erros", f"{(len(erros_enderecos)/len(st.session_state['df_enderecos'])*100):.1f}%")
                        
                        # Mostrar erros
                        if erros_enderecos:
                            st.subheader("Erros Encontrados")
                            for error in erros_enderecos:
                                with st.expander(f"Erros na Linha {error['linha']}"):
                                    if error['linha'] == 0:
                                        # Erro de colunas
                                        for err in error['erros']:
                                            st.error(err['msg'])
                                    else:
                                        # Mostrar a linha completa com os dados
                                        linha_data = df_enderecos_display[df_enderecos_display['Nº Linha'] == error['linha']].iloc[0]
                                        st.write("Dados da linha:")
                                        st.dataframe(linha_data.to_frame().T, hide_index=True)
                                        
                                        # Mostrar os erros
                                        st.write("Erros encontrados:")
                                        for err in error['erros']:
                                            campo = err['loc'][0]
                                            msg = err['msg']
                                            st.error(f"Campo '{campo}': {msg}")
                        else:
                            st.success("Nenhum erro encontrado nos dados dos endereços!")

if __name__ == "__main__":
    main() 