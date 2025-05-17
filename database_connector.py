import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error

load_dotenv()
def obter_conexao():
    try:
        conexao = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        )
        return conexao
    except Error as error:
        print(f'Erro ao conectar ao banco de dados: {error}')
        return None


def executar_consulta(query, parametros=None):
#executa uma consulta SELECT e retorna os resultados

    conexao = obter_conexao()
    if not conexao:
        return []

    try:
        with conexao.cursor(dictionary=True) as cursor:
            cursor.execute(query, parametros or ())
            resultado = cursor.fetchall()
            return resultado

    except Error as erro:
        print(f'Erro falha na execução da consulta: {erro}')
        return []

    finally:
        conexao.close()


def executar_comando(query, parametros=None):
#executar comandos INSERT, UPDATE ou DELETE
    conexao = obter_conexao()
    if not conexao:
        return False

    try:
        with conexao.cursor() as cursor:
            cursor.execute(query, parametros or ())
            conexao.commit()
            return True

    except Error as erro:
        print(f'Falha na execução do comando: {erro}')
        return False
    finally:
        conexao.close()

