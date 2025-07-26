from logica_sistema.logica_sistema import *
from database_connector import *


def adicionar_valores_livros(entrada_titulo,entrada_autor, entrada_editora, ano_publicacao, qtd_total, qtd_disponivel, master=None):
    titulo = entrada_titulo.get()
    autor = entrada_autor.get()
    editora = entrada_editora.get()
    ano = ano_publicacao.get()
    quant_tot = qtd_total.get()
    quant_disp = qtd_disponivel.get()

    if not all([titulo, autor, editora, ano, quant_tot, quant_disp]):
        print('Preencha todos os campos!.')
        mostrar_mensagem('Preencha todos os campos!.', 'orange', master)
        return

    try:
        executar_comando(
         "INSERT INTO livros (titulo, autor, editora, ano_publicacao, quantidade_total, quantidade_disponivel) VALUES (%s, %s, %s, %s, %s, %s)",
         (titulo,
          autor,
          editora,
          ano,
          quant_tot,
          quant_disp)
        )
        print('Livro Adicionado!.')
        mostrar_mensagem('Livro adicionado com sucesso!.', 'green', master)
        entrada_titulo.delete(0, 'end'),
        entrada_autor.delete(0, 'end'),
        entrada_editora.delete(0, 'end'),
        ano_publicacao.delete(0, 'end'),
        qtd_total.delete(0, 'end'),
        qtd_disponivel.delete(0, 'end')

    except Error as erro:
        print(f'ERRO ao Adicionar Livro:{erro}')
        mostrar_mensagem('Erro ao adicionar livro!.', 'red', master)


def visualizar_livros(caixa_de_texto):
    livros = executar_consulta("SELECT id_livro, titulo, autor, editora, ano_publicacao, quantidade_total, quantidade_disponivel FROM livros")
    if caixa_de_texto is None:
        print('Caixa de texto não foi passada!.')
        return
    caixa_de_texto.delete('1.0', 'end')
    for livro in livros:
        texto = (f'ID: {livro['id_livro']}\n'
                 f'TITULO: {livro['titulo']}\n'
                 f'AUTOR: {livro['autor']}\n'
                 f'EDITORA: {livro['editora']}\n'
                 f'ANO PUBLICAÇÃO: {livro['ano_publicacao']}\n'
                 f'QUANTIDADE TOTAL: {livro['quantidade_total']} |'f'  QUANTIDADE DISPONIVEL: {livro['quantidade_disponivel']}\n'
                 f'{'-' * 120}\n')

        caixa_de_texto.insert('end', texto)


def pesquisar_livro(entrada_pesquisar, caixa_texto2):
    titulo_entrada = entrada_pesquisar.get().strip()
    caixa_texto2.delete('1.0', 'end')
    if not titulo_entrada:
        caixa_texto2.insert('end', 'Digite o titulo do livro\n')
        return
    parametro = (f"%{titulo_entrada}%",)
    livros = executar_consulta("SELECT id_livro, titulo, autor, editora, ano_publicacao, quantidade_total, quantidade_disponivel FROM livros WHERE titulo LIKE %s",
                               parametro)
    if livros:
        for l in livros:
            texto = (f'ID: {l['id_livro']}\n'
                 f'TITULO: {l['titulo']}\n'
                 f'AUTOR: {l['autor']}\n'
                 f'EDITORA: {l['editora']}\n'
                 f'ANO PUBLICAÇÃO: {l['ano_publicacao']}\n'
                 f'QUANTIDADE TOTAL: {l['quantidade_total']} |'f'  QUANTIDADE DISPONIVEL: {l['quantidade_disponivel']}\n'
                 f'{'-' * 120}\n')

            caixa_texto2.insert('end', texto)
    else:
        caixa_texto2.insert('end', 'Nenhum livro encontrado com esse titulo!.')


def remover_livro(id_livro, nome_remove_livro, master):
    idlivro = id_livro.get()
    titulo = nome_remove_livro.get()

    try:
        executar_comando('DELETE FROM livros WHERE id_livro = %s AND titulo = %s',
                         (idlivro,
                         titulo))

        print('Removido com sucesso!')
        mostrar_mensagem('Removido com sucesso!', 'green', master)
        id_livro.delete(0, 'end')
        nome_remove_livro.delete(0, 'end')

    except Error as erro:
        print(f'Erro ao remover livro: {erro}')
        mostrar_mensagem(f'Erro ao remover livro: {erro}', 'orange', master)
        id_livro.delete(0, 'end')
        nome_remove_livro.delete(0, 'end')


def obter_estatisticas_livros():
    try:
        total_cadastrados = 0
        soma_total = 0

        # Obter a contagem de livros cadastrados
        livros_resultado = executar_consulta('SELECT COUNT(*) AS total_cadastrados FROM livros')
        if livros_resultado and livros_resultado[0]:
            total_cadastrados = livros_resultado[0]['total_cadastrados']

        # Obter a soma total de livros
        total_resultado = executar_consulta('SELECT SUM(quantidade_total) AS total FROM livros')
        if total_resultado and total_resultado[0] and total_resultado[0]['total'] is not None:
            soma_total = total_resultado[0]['total']

        mensagem = f'Foram cadastrados: {total_cadastrados} Livros.\n'
        mensagem += f'O total de livros é: {soma_total}'
        return mensagem

    except Error as erro:
        return f'ERRO ao obter estatísticas: {erro}'

