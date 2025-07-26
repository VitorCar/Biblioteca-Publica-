from logica_sistema.logica_sistema import *
from database_connector import *


def realizar_emprestimo(nome_aluno, titulo_livro, data_emprestimo, data_prevista, master=None):
    #buscar ids
    aluno = executar_consulta("SELECT id_aluno FROM alunos WHERE nome_completo = %s", (nome_aluno,))
    livro = executar_consulta("SELECT id_livro , quantidade_disponivel FROM livros WHERE titulo = %s", (titulo_livro,))

    if not aluno:
        print('Aluno não encontrado!.')
        mostrar_mensagem('Aluno não encontrado!.', 'orange', master)
        return
    id_aluno = aluno[0]['id_aluno']

    if not livro:
        print('Livro não encontrado')
        mostrar_mensagem('Livro não encontrado!.', 'orange', master)
        return
    id_livro = livro[0]['id_livro']
    qtd_disponivel = livro[0]['quantidade_disponivel']

    #verificar livro disponivel
    if qtd_disponivel < 1:
        print('Livro indisponível.')
        mostrar_mensagem('Livro indisponível!.', 'orange', master)
        return

    #registrar emprestimo
    sucesso = executar_comando('INSERT INTO emprestimo (id_aluno, id_livro, data_emprestimo, data_devolucao_prevista, data_devolucao_real) VALUES (%s, %s, %s, %s, NULL)',
                               (id_aluno, id_livro, data_emprestimo, data_prevista)


    )

    if sucesso:
        executar_comando(
            "UPDATE livros SET quantidade_disponivel = quantidade_disponivel - 1 WHERE id_livro = %s",
              (id_livro,)
        )
        print('Empréstimo registrado com sucesso!.')
        mostrar_mensagem('Empréstimo registrado com sucesso!.', 'green', master)


def visualizar_emprestimo(caixa_emprestimo):
    emprestimos = executar_consulta("""
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
    ORDER BY e.data_emprestimo DESC
    """)

    if caixa_emprestimo is None:
        print('Caixa de texto não foi passada')
        return

    caixa_emprestimo.delete('1.0', 'end')

    # Define as cores das tags
    caixa_emprestimo.tag_config('nao_devolvido', foreground='red')
    caixa_emprestimo.tag_config('devolvido', foreground='green')

    for emp in emprestimos:
        devolucao = emp['data_devolucao_real']
        status = "DEVOLVIDO" if devolucao else "EM ATRASO OU EM ABERTO"
        tag = 'devolvido' if devolucao else 'nao_devolvido'

        txt = (f'EMPRÉSTIMO ID: {emp['id_emprestimo']} | ALUNO: {emp['aluno']} | LIVRO: {emp['livro']}\n'
               f'DATA EMPRÉSTIMO: {emp['data_emprestimo']} | PREVISTA: {emp['data_devolucao_prevista']}\n'
               f'DEVOLUÇÃO: {emp['data_devolucao_real'] or 'NÃO DEVOLVIDO'}\n'
               f'STATUS: ')

        caixa_emprestimo.insert('end', txt)
        caixa_emprestimo.insert('end', f'{status}', f'{tag}')
        caixa_emprestimo.insert('end', '\n')
        caixa_emprestimo.insert('end', '-' * 170 + '\n')


def pesquisar_emprestimo(entrada_pesquisar_emprestimo, caixa_texto2_emprestimo):
    query =""" SELECT 
    e.id_emprestimo,
    a.nome_completo AS aluno,
    l.titulo AS livro,
    e.data_emprestimo,
    e.data_devolucao_prevista,
    e.data_devolucao_real
    FROM emprestimo e 
    JOIN alunos a ON e.id_aluno = a.id_aluno
    JOIN livros l ON e.id_livro = l.id_livro
    WHERE a.nome_completo = %s """

    resultado = executar_consulta(query, (entrada_pesquisar_emprestimo,))

    if caixa_texto2_emprestimo is None:
        print('Caixa de texto não foi passada')
        return

    caixa_texto2_emprestimo.delete('1.0', 'end')

    if not resultado:
        caixa_texto2_emprestimo.insert('end', f'Nenhum empréstimo encontrado para o aluno: {entrada_pesquisar_emprestimo}')

    # Define as cores das tags
    caixa_texto2_emprestimo.tag_config('nao_devolvido', foreground='red')
    caixa_texto2_emprestimo.tag_config('devolvido', foreground='green')

    for emp in resultado:
        devolucao = emp['data_devolucao_real']
        status = "DEVOLVIDO" if devolucao else "EM ATRASO OU EM ABERTO"
        tag = 'devolvido' if devolucao else 'nao_devolvido'

        txt = (f'EMPRÉSTIMO ID: {emp['id_emprestimo']} | ALUNO: {emp['aluno']} | LIVRO: {emp['livro']}\n'
               f'DATA EMPRÉSTIMO: {emp['data_emprestimo']} | PREVISTA: {emp['data_devolucao_prevista']}\n'
               f'DEVOLUÇÃO: {emp['data_devolucao_real'] or 'NÃO DEVOLVIDO'}\n'
               f'STATUS: ')

        caixa_texto2_emprestimo. insert('end', txt)
        caixa_texto2_emprestimo.insert('end', f'{status}', tag)
        caixa_texto2_emprestimo.insert('end', '\n')
        caixa_texto2_emprestimo.insert('end', '-' * 170 + '\n')


def registrar_devolucao(nome_emp, lvro, data_real, master):
    aluno = nome_emp.get()
    titulo_livro = lvro.get()
    data = data_real.get()

    aln = executar_consulta("SELECT id_aluno FROM alunos WHERE nome_completo = %s", (aluno,))
    if not aln:
        print('Aluno não encontrado!.')
        mostrar_mensagem('Aluno não encontrado!.', 'orange', master)
        return
    id_aluno = aln[0]['id_aluno']

    #busca id do livro
    livro = executar_consulta("SELECT id_livro FROM livros WHERE titulo = %s", (titulo_livro,))
    if not livro:
        print('Livro não encontrado!.')
        mostrar_mensagem('Livro não encontrado', 'orange', master)
        return
    id_livro = livro[0]['id_livro']

    #verificar se ha emprestimo (sem data de devolução)
    emprestimo = executar_consulta("SELECT id_emprestimo FROM emprestimo WHERE id_aluno = %s AND id_livro = %s AND data_devolucao_real IS NULL",
        (id_aluno, id_livro))

    if not emprestimo:
        print('Nenhum empréstimo ativo encontrado para este aluno e livro.')
        mostrar_mensagem("Nenhum empréstimo ativo encontrado!", "orange", master)
        return

    id_emprestimo = emprestimo[0]['id_emprestimo']
    #atualizar data de devolução
    sucesso = executar_comando("UPDATE emprestimo SET data_devolucao_real = %s WHERE id_emprestimo = %s",
        (data, id_emprestimo))

    if sucesso:
        #devolver livro ao estoque
        executar_comando("UPDATE livros SET quantidade_disponivel = quantidade_disponivel + 1 WHERE id_livro = %s",
            (id_livro,))
        print('Devolução registrada com sucesso!')
        mostrar_mensagem("Devolução registrada com sucesso!", "green", master)
        nome_emp.delete(0, 'end')
        lvro.delete(0, 'end')

    else:
        print("Erro ao registrar devolução.")
        mostrar_mensagem("Erro ao registrar devolução!", "orange", master)
        nome_emp.delete(0, 'end')
        lvro.delete(0, 'end')


def remover_emprestimo(id_emprestimo, nome_remove_emprestimo, master):
    idempret = id_emprestimo.get()
    nome_empret = nome_remove_emprestimo.get()
    try:
        aluno = executar_consulta("SELECT id_aluno FROM alunos WHERE nome_completo = %s", (nome_empret,))

        if not aluno:
            print('Aluno não encontrado!.')
            mostrar_mensagem('Aluno não encontrado!.', 'orange', master)
            return
        id_aluno = aluno[0]['id_aluno']

        executar_comando('DELETE FROM emprestimo WHERE id_emprestimo = %s AND id_aluno = %s', (idempret, id_aluno,))
        mostrar_mensagem('Removido com sucesso!.', 'green', master)
        id_emprestimo.delete(0, 'end')
        nome_remove_emprestimo.delete(0, 'end')

    except Error as erro:
        print('Erro ao remover empréstimo!.')
        mostrar_mensagem('Erro ao remover empréstimo!.', 'orange', master)
        id_emprestimo.delete(0, 'end')
        nome_remove_emprestimo.delete(0, 'end')


def obter_estatisticas_emprestimo(caixa_texto2_emprestimo):
    caixa_texto2_emprestimo.delete('1.0', 'end')
    try:
        # Contar o número total de empréstimos
        cursor = executar_consulta('SELECT COUNT(*) AS total_emprestimos FROM emprestimo')
        total_emprestimos = cursor[0]['total_emprestimos'] if cursor and cursor[0] else 0

        # Contar o número de empréstimos não devolvidos (data_devolucao_real IS NULL)
        cursor_nao_devolvidos = executar_consulta('SELECT COUNT(*) AS nao_devolvidos FROM emprestimo WHERE data_devolucao_real IS NULL')
        nao_devolvidos = cursor_nao_devolvidos[0]['nao_devolvidos'] if cursor_nao_devolvidos and cursor_nao_devolvidos[0] else 0

        em_atraso_ou_aberto = nao_devolvidos

        # Inserir as estatísticas com formatação
        caixa_texto2_emprestimo.insert('end', f'TOTAL DE EMPRÉSTIMOS: ', ('total_label', 'bold'))
        caixa_texto2_emprestimo.insert('end', f'{total_emprestimos}\n', ('total_value', 'white'))

        caixa_texto2_emprestimo.insert('end', f'NÃO DEVOLVIDOS: ', 'bold')
        caixa_texto2_emprestimo.insert('end', f'{nao_devolvidos}\n')

        caixa_texto2_emprestimo.insert('end', f'EM ATRASO OU EM ABERTO: ', 'bold')
        caixa_texto2_emprestimo.insert('end', f'{em_atraso_ou_aberto}\n')

    except Error as erro:
        caixa_texto2_emprestimo.insert('end', f'ERRO ao obter estatísticas de empréstimo: {erro}')
