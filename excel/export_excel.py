import pandas as pd
from datetime import date
from database_connector import *
import os
import subprocess

from logica_sistema.logica_sistema import mostrar_mensagem

data_atual = date.today()


def export_livro(master):
    documentos = os.path.join(os.path.expanduser("~"), "Documents")
    nome_arquivo = f"Livros_Export_{data_atual}.xlsx"
    caminho_completo = os.path.join(documentos, nome_arquivo)

    exporta_livro = executar_consulta('SELECT * FROM livros')
    exporta_livro = pd.DataFrame(exporta_livro, columns=['id_livro', 'titulo', 'autor', 'editora', 'ano_publicacao', 'quantidade_total', 'quantidade_disponivel'])
    exporta_livro.to_excel(caminho_completo, index=False)
    mostrar_mensagem('Livros exportados com sucesso!', 'green', master)
    # Abre o arquivo e também a pasta
    os.startfile(caminho_completo)
    subprocess.run(['explorer', documentos])


def export_aluno(master):
    documentos = os.path.join(os.path.expanduser("~"), "Documents")
    nome_arquivo = f"Alunos_Export_{data_atual}.xlsx"
    caminho_completo = os.path.join(documentos, nome_arquivo)

    dados = executar_consulta("SELECT * FROM alunos")
    df = pd.DataFrame(dados, columns=['id_aluno', 'nome_completo', 'matricula', 'email', 'telefone'])
    df.to_excel(caminho_completo, index=False)
    print("Alunos exportados com sucesso!")
    mostrar_mensagem("Alunos exportados com sucesso!", 'green', master)
    os.startfile(caminho_completo)
    subprocess.run(['explorer', documentos])


def exportar_emprestimos(master):
    documentos = os.path.join(os.path.expanduser("~"), "Documents")
    nome_arquivo = f"Empréstimos_Export_{data_atual}.xlsx"
    caminho_completo = os.path.join(documentos, nome_arquivo)

    query = """
    SELECT 
        e.id_emprestimo,
        a.nome_completo AS aluno,
        l.titulo AS livro,
        e.data_emprestimo,
        e.data_devolucao_prevista,
        e.data_devolucao_real
    FROM emprestimo e
    JOIN alunos a ON e.id_aluno = a.id_aluno
    JOIN livros l ON e.id_livro = l.id_livro
    """
    dados = executar_consulta(query)
    df = pd.DataFrame(dados, columns=['id_emprestimo', 'aluno', 'livro', 'data_emprestimo', 'data_devolucao_prevista', 'data_devolucao_real'])
    df.to_excel(caminho_completo, index=False)
    print("Empréstimos exportados com sucesso!")
    mostrar_mensagem("Empréstimos exportados com sucesso!", 'green', master)

    # Abre o arquivo e também a pasta
    os.startfile(caminho_completo)
    subprocess.run(['explorer', documentos])