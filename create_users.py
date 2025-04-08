from faker import Faker
import pandas as pd
import uuid
import random
import numpy as np

# Initialize Faker with Brazilian locale
fake = Faker('pt_BR')

def introduce_errors(value, error_type):
    if random.random() < 0.1:  # 10% chance of error
        if error_type == 'null':
            return np.nan
        elif error_type == 'duplicate':
            return value
        elif error_type == 'format':
            return str(value).upper()  # Inconsistent formatting
        elif error_type == 'invalid':
            return 'INVALIDO'
    return value

# Function to generate customer data with errors
def generate_customer_data(num_customers=250):
    customers = []
    
    for _ in range(num_customers):
        customer_id = str(uuid.uuid4())
        nome = fake.name()
        email = fake.email()
        data_nascimento = fake.date_of_birth(minimum_age=18, maximum_age=80).strftime('%Y-%m-%d')
        cpf = fake.cpf()
        telefone = fake.phone_number()
        
        # Introduce errors
        nome = introduce_errors(nome, 'format')
        email = introduce_errors(email, 'null')
        data_nascimento = introduce_errors(data_nascimento, 'invalid')
        cpf = introduce_errors(cpf, 'format')
        telefone = introduce_errors(telefone, 'null')
        
        customer = {
            'id_cliente': customer_id,
            'nome': nome,
            'email': email,
            'data_nascimento': data_nascimento,
            'cpf': cpf,
            'telefone': telefone
        }
        customers.append(customer)
    
    # Add some duplicate customers
    for _ in range(5):
        duplicate = random.choice(customers).copy()
        duplicate['id_cliente'] = str(uuid.uuid4())  # New ID for duplicate
        customers.append(duplicate)
    
    return pd.DataFrame(customers)

# Function to generate address data with errors
def generate_address_data(customer_df):
    addresses = []
    
    for _, customer in customer_df.iterrows():
        # 80% chance of having an address
        if random.random() < 0.8:
            address = {
                'id_cliente': customer['id_cliente'],
                'tipo_endereco': introduce_errors(fake.random_element(elements=('Residencial', 'Comercial')), 'format'),
                'endereco': introduce_errors(fake.street_address(), 'null'),
                'numero': introduce_errors(fake.building_number(), 'invalid'),
                'complemento': introduce_errors(fake.random_element(elements=('', 'Apto 101', 'Casa 2', 'Sala 3')), 'null'),
                'bairro': introduce_errors(fake.bairro(), 'format'),
                'cidade': introduce_errors(fake.city(), 'format'),
                'estado': introduce_errors(fake.estado_nome(), 'invalid'),
                'cep': introduce_errors(fake.postcode(), 'format'),
                'ponto_referencia': introduce_errors(fake.random_element(elements=('Próximo ao shopping', 'Em frente à praça', 'Ao lado da escola', '')), 'null')
            }
            addresses.append(address)
    
    # Add some addresses without corresponding customers
    for _ in range(10):
        fake_address = {
            'id_cliente': str(uuid.uuid4()),  # Random ID that doesn't exist in customers
            'tipo_endereco': fake.random_element(elements=('Residencial', 'Comercial')),
            'endereco': fake.street_address(),
            'numero': fake.building_number(),
            'complemento': fake.random_element(elements=('', 'Apto 101', 'Casa 2', 'Sala 3')),
            'bairro': fake.bairro(),
            'cidade': fake.city(),
            'estado': fake.estado_nome(),
            'cep': fake.postcode(),
            'ponto_referencia': fake.random_element(elements=('Próximo ao shopping', 'Em frente à praça', 'Ao lado da escola', ''))
        }
        addresses.append(fake_address)
    
    return pd.DataFrame(addresses)

# Generate customer data with errors
df_customers = generate_customer_data(100)

# Generate address data with errors
df_addresses = generate_address_data(df_customers)

# Save to CSV files
df_customers.to_csv('output/clientes_com_erros.csv', index=False, encoding='utf-8')
df_addresses.to_csv('output/enderecos_com_erros.csv', index=False, encoding='utf-8')

print("Arquivos gerados com sucesso!")  
print("- 'clientes_com_erros.csv': Contém informações dos clientes com erros e inconsistências")
print("- 'enderecos_com_erros.csv': Contém informações dos endereços com erros e inconsistências")
print("\nTipos de erros introduzidos:")
print("1. Dados faltantes (null/NaN)")
print("2. Formatação inconsistente (maiúsculas/minúsculas)")
print("3. Dados duplicados")
print("4. Valores inválidos")
print("5. Endereços sem clientes correspondentes")
print("6. Clientes sem endereços")