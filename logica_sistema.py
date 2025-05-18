from database_connector import *
import datetime
from datetime import date, timedelta
import customtkinter as ctk
import customtkinter
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os
#biblioteca para executar no fundo do programa para enviar email aut
import threading
import time


#---------------- LIVROS ------------------
def mostrar_mensagem(texto, cor, master):
    popup = ctk.CTkToplevel(master)
    popup.title('Aviso')
    popup.geometry('300x100')
    popup.configure(fg_color=cor)

    mensagem = ctk.CTkLabel(popup, text=texto, font=('Ariel', 14))
    mensagem.pack(pady=20)

    botao_ok = ctk.CTkButton(popup, text='OK', command=popup.destroy)
    botao_ok.pack(pady=5)


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


#-------------------------------- ALUNOS --------------------------------------------

def adicionar_aluno(nome, matricula, email, celular, master=None):
    verificar_nome = nome.get()
    verificar_matricula = matricula.get()
    verificar_email = email.get()
    verificar_celular = celular.get()

    #verificar se algum campo esta vazio
    if not all([verificar_nome, verificar_matricula, verificar_email, verificar_celular]):
        print('Preencha todos os campos!.')
        mostrar_mensagem('Preencha todos os campos!.', 'orange', master)
        return
    try:
        executar_comando(
            "INSERT INTO alunos (nome_completo, matricula, email, telefone) VALUES (%s, %s, %s, %s)",
            (verificar_nome,
             verificar_matricula,
             verificar_email,
             verificar_celular)
        )

        print('Aluno Adicionado!.')
        mostrar_mensagem('Aluno adicionado com sucesso!', 'green', master)

        #limpando o campo
        nome.delete(0, 'end'),
        matricula.delete(0, 'end'),
        email.delete(0, 'end'),
        celular.delete(0, 'end')

    except Error as erro:
        print(f'ERRO ao Adicionar Aluno:{erro}')
        mostrar_mensagem('Error ao adicionar Aluno!.', 'red', master)


def vizualizar_alunos(caixa_txt):
    alunos = executar_consulta("SELECT id_aluno, nome_completo, matricula, email, telefone FROM alunos")
    if caixa_txt is None:
        print('Caixa de texto não foi passada')
        return
    caixa_txt.delete('1.0', 'end')
    for aluno in alunos:
        txt = (f'ID: {aluno['id_aluno']}| NOME: {aluno['nome_completo']} | MATRICULA: {aluno['matricula']}\n'
               f'EMAIL: {aluno['email']} | CELULAR: {aluno['telefone']}\n'
               f'{'-' * 120}\n')

        caixa_txt.insert('end', txt)


def pesquisar_aluno(entrada_pesquisar_alunos, caixa_texto2_alunos):
    nome_entrada = entrada_pesquisar_alunos.get().strip()
    caixa_texto2_alunos.delete('1.0', 'end')
    if not nome_entrada:
        caixa_texto2_alunos.insert('end', 'Digite o nome do aluno\n')
        return
    parametro = (f"%{nome_entrada}%",)
    alunos = executar_consulta("SELECT id_aluno, nome_completo, matricula, email, telefone FROM alunos WHERE nome_completo LIKE %s",
                               parametro)
    if alunos:
        for a in alunos:
            texto = (f'ID: {a['id_aluno']}| NOME: {a['nome_completo']} | MATRICULA: {a['matricula']}\n'
               f'EMAIL: {a['email']} | CELULAR: {a['telefone']}\n'
               f'{'-' * 120}\n')

            caixa_texto2_alunos.insert('end', texto)

    else:
        caixa_texto2_alunos.insert('end', 'Nenhum aluno encontrado com esse Nome!.')


def remover_aluno(id_aluno, nome_remove_aluno, master):
    idaluno = id_aluno.get()
    nome_alu = nome_remove_aluno.get()
    try:
        executar_comando('DELETE FROM alunos WHERE id_aluno = %s AND nome_completo = %s',
                         (idaluno,
                          nome_alu))


        mostrar_mensagem('Removido com sucesso!.', 'green', master)
        id_aluno.delete(0, 'end')
        nome_remove_aluno.delete(0, 'end')

    except Error as erro:
        mostrar_mensagem('Erro ao remover Aluno!.', 'orange', master)
        id_aluno.delete(0, 'end')
        nome_remove_aluno.delete(0, 'end')


#validar ate um certo numero MATRICULA
def validar_matricula(p, matricula):
    valor = matricula.get()
    novo_valor = ''.join(filter(str.isdigit, valor))[:5]
    if valor != novo_valor or not novo_valor.isdigit():
        # Substitui o texto no campo com o valor limpo
        matricula.delete(0, ctk.END)
        matricula.insert(0, novo_valor)


#Validar celular 9 digitos
def validar_celular(c, celular):
    num = celular.get()
    novo_num = ''.join(filter(str.isdigit, num))[:9]
    if num != novo_num or not novo_num.isdigit():
        celular.delete(0, ctk.END)
        celular.insert(0, novo_num)


def quantidade_alunos_cadastrados(caixa_estat_alunos):
    caixa_estat_alunos.delete('1.0', 'end')
    try:
        alunos_resultado = executar_consulta('SELECT COUNT(*) AS total_alunos FROM alunos')
        if alunos_resultado and alunos_resultado[0]:
            total_alunos = alunos_resultado[0]['total_alunos']
            txt = f'Foram cadastrados: {total_alunos} Alunos.'
            caixa_estat_alunos.insert('end', txt)
        else:
            caixa_estat_alunos.insert('end', 'Nenhum aluno cadastrado.')
    except Error as erro:
        caixa_estat_alunos.insert('end', f'ERRO ao contar alunos cadastrados!: {erro}')


#---------------- EMPRESTIMO ----------------
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


#DATA EM TEMPO REAL
def atualizar_data(janela, data_emprestimo):
    data_atual = date.today().strftime('%Y-%m-%d')
    data_emprestimo.delete(0, 'end')
    data_emprestimo.insert(0, data_atual)
    janela.after(1000, lambda:atualizar_data(janela, data_emprestimo))


def atualizar_data_prevista(janela, data_prevista):
    data_atual = date.today()
    prevista = data_atual + timedelta(days=120)
    data_prevista.delete(0, 'end')
    data_prevista.insert(0, prevista)
    janela.after(1000, lambda: atualizar_data_prevista(janela, data_prevista))


#APERTAR ENTER
def apertar_enter(event, proximo_campo):
    proximo_campo.focus_set()

#--------------ENVIAR EMAIL-------------------

def enviar_email(destinatario, assunto, mensagem):
    load_dotenv()

    remetente = os.getenv("EMAIL_USUARIO")
    senha = os.getenv("EMAIL_SENHA")

    msg = MIMEText(mensagem, 'plain', 'utf-8')
    msg['Subject'] = assunto
    msg['From'] = remetente
    msg['To'] = destinatario

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as servidor:
            servidor.starttls()
            servidor.login(remetente, senha)
            servidor.sendmail(remetente, destinatario, msg.as_string())
            print(f"E-mail enviado para {destinatario}")
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")


def notificar_emprestimos_atrasados():
    hoje = date.today()

    query = """
    SELECT 
        a.nome_completo,
        a.email,
        l.titulo,
        e.data_devolucao_prevista
    FROM emprestimo e
    JOIN alunos a ON e.id_aluno = a.id_aluno
    JOIN livros l ON e.id_livro = l.id_livro
    WHERE e.data_devolucao_real IS NULL AND e.data_devolucao_prevista < %s
    """

    emprestimos_vencidos = executar_consulta(query, (hoje,))

    for emp in emprestimos_vencidos:
        nome = emp['nome_completo']
        email = emp['email']
        livro = emp['titulo']
        data_prevista = emp['data_devolucao_prevista'].strftime('%d/%m/%Y')

        mensagem = (
            f"Olá {nome},\n\n"
            f"O livro '{livro}' que você pegou emprestado deveria ter sido devolvido até {data_prevista}.\n"
            "Por favor, devolva o mais breve possível para evitar restrições.\n\n"
            "Obrigado,\nBiblioteca Pública"
        )

        enviar_email(email, "Empréstimo vencido - Biblioteca", mensagem)


def verificar_atrasos_periodicamente():
    while True:
        notificar_emprestimos_atrasados()
        time.sleep(86400)  # Espera 24 horas (em segundos)

# Inicia a thread quando o programa for iniciado
thread = threading.Thread(target=verificar_atrasos_periodicamente)
thread.daemon = True  # Encerra a thread quando a interface fecha
thread.start()
