from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Optional
from datetime import date
import re

class Cliente(BaseModel):
    id_cliente: str = Field(..., description="Identificador único do cliente")
    nome: str = Field(..., min_length=3, max_length=100, description="Nome completo do cliente")
    email: Optional[EmailStr] = Field(None, description="Email do cliente")
    data_nascimento: Optional[str] = Field(None, description="Data de nascimento no formato YYYY-MM-DD")
    cpf: Optional[str] = Field(None, description="CPF do cliente")
    telefone: Optional[str] = Field(None, description="Telefone do cliente")

    @field_validator('cpf')
    @classmethod
    def validate_cpf(cls, v):
        if v is None:
            return v
        # Remove caracteres não numéricos
        cpf = re.sub(r'[^\d]', '', v)
        if len(cpf) != 11:
            raise ValueError('CPF deve conter 11 dígitos')
        return cpf

    @field_validator('data_nascimento')
    @classmethod
    def validate_data_nascimento(cls, v):
        if v is None:
            return v
        try:
            # Tenta converter para date para validar o formato
            date.fromisoformat(v)
            return v
        except ValueError:
            raise ValueError('Data de nascimento deve estar no formato YYYY-MM-DD')

class Endereco(BaseModel):
    id_cliente: str = Field(..., description="ID do cliente associado ao endereço")
    tipo_endereco: Optional[str] = Field(None, description="Tipo do endereço (Residencial/Comercial)")
    endereco: Optional[str] = Field(None, description="Logradouro do endereço")
    numero: Optional[str] = Field(None, description="Número do endereço")
    complemento: Optional[str] = Field(None, description="Complemento do endereço")
    bairro: Optional[str] = Field(None, description="Bairro")
    cidade: Optional[str] = Field(None, description="Cidade")
    estado: Optional[str] = Field(None, description="Estado")
    cep: Optional[str] = Field(None, description="CEP")
    ponto_referencia: Optional[str] = Field(None, description="Ponto de referência")

    @field_validator('cep')
    @classmethod
    def validate_cep(cls, v):
        if v is None:
            return v
        # Remove caracteres não numéricos
        cep = re.sub(r'[^\d]', '', v)
        if len(cep) != 8:
            raise ValueError('CEP deve conter 8 dígitos')
        return cep

    @field_validator('tipo_endereco')
    @classmethod
    def validate_tipo_endereco(cls, v):
        if v is None:
            return v
        tipos_validos = ['RESIDENCIAL', 'COMERCIAL']
        if v.upper() not in tipos_validos:
            raise ValueError(f'Tipo de endereço deve ser um dos seguintes: {", ".join(tipos_validos)}')
        return v.upper() 