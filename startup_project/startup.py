import mysql.connector
# getpass eh um modulo para mascarar a senha
import getpass
from datetime import date

# inserir no sistema as credencicias do banco de dados
user_host = input('iforme o host')
user_user = input('informe o usuario')
user_password = getpass.getpass('informe a senha')
user_db = input('Informe o banco de dados')


conexao = mysql.connector.connect(
    host = user_host,
    user = user_user,
    password = user_password,
    database = user_db
)

cursor = conexao.cursor()

def mostrar_tabela(startup):
    print(f'tabela {startup}')
    cursor.execute(f'select * from {startup}')
    # para coletar os resultados
    resultados = cursor.fetchall()
    
    colunas = [desc[0] for desc in cursor.description]
    
    print(' | '.join(colunas))
    
    print('-'*50)
    
    for linha in resultados:
        print(" | ".join(str(item) for item in linha))