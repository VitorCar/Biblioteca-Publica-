from database_connector import *
import datetime
from datetime import date, timedelta
import customtkinter as ctk
import customtkinter


def mostrar_mensagem(texto, cor, master):
    popup = ctk.CTkToplevel(master)
    popup.title('Aviso')
    popup.geometry('300x100')
    popup.configure(fg_color=cor)

    mensagem = ctk.CTkLabel(popup, text=texto, font=('Ariel', 14))
    mensagem.pack(pady=20)

    botao_ok = ctk.CTkButton(popup, text='OK', command=popup.destroy)
    botao_ok.pack(pady=5)


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


def apertar_enter(event, proximo_campo):
    proximo_campo.focus_set()

