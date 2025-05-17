import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error

load_dotenv()

try:
    conexao = mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME')
    )

    if conexao.is_connected():
        print('conexão com mysql realizada com sucesso')


except Error as erro:
    print(f'erro ao conectar: {erro}')

finally:
    if 'conexao'in locals() and conexao.is_connected():
        conexao.close()
        print('Conexão encerrada')
