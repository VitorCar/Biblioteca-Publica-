from database_connector import *
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os
#biblioteca para executar no fundo do programa para enviar email aut
import threading
import time
from datetime import date, timedelta

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
