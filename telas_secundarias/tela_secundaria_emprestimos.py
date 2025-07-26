from logica_sistema.emprestimos import *
from excel.export_excel import *
import customtkinter

background_color = "#1a1a1a"

def tela_visualizacao_remover_emprestimo():
    customtkinter.set_appearance_mode('dark')
    customtkinter.set_default_color_theme('dark-blue')

    janela_3_emprestimo = customtkinter.CTkToplevel()
    janela_3_emprestimo.geometry("1072x768")

    janela_3_emprestimo.title('Gerenciamento de Biblioteca')

    # Configurar o grid para ter duas colunas com pesos iguais
    janela_3_emprestimo.grid_columnconfigure(0, weight=1)  # Coluna da visualização de livros
    janela_3_emprestimo.grid_columnconfigure(1, weight=1)  # Coluna do sistema de remoção de livros
    janela_3_emprestimo.grid_rowconfigure(0, weight=1)  # Uma única linha que ocupa toda a altura

    # Frame para a visualização de livros
    frame_visualizacao = customtkinter.CTkFrame(janela_3_emprestimo)
    frame_visualizacao.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
    label_visualizacao = customtkinter.CTkLabel(frame_visualizacao, text="Visualização de Empréstimos",
                                                font=('Ariel', 36, 'bold'))
    label_visualizacao.pack(padx=20, pady=10)

    caixa_emprestimo = customtkinter.CTkTextbox(frame_visualizacao, width=600, height=250)
    caixa_emprestimo.pack(pady=20)

    #funçao que atualiza os dados
    def busca_automatica_visualizar():
        visualizar_emprestimo(caixa_emprestimo)
        janela_3_emprestimo.after(500, busca_automatica_visualizar)

    busca_automatica_visualizar()



    entrada_pesquisar_emprestimo = customtkinter.CTkEntry(frame_visualizacao, width=300,
                                                          placeholder_text='Nome do aluno')
    entrada_pesquisar_emprestimo.pack(pady=(40, 10))

    botao_pesquisar_emprestimo = customtkinter.CTkButton(frame_visualizacao, text='Pesquisar',
                                                         font=('Ariel', 14, 'bold'),
                                                         command=lambda: pesquisar_emprestimo(entrada_pesquisar_emprestimo.get(),
                                                                                                                          caixa_texto2_emprestimo))
    botao_pesquisar_emprestimo.pack()

    caixa_texto2_emprestimo = customtkinter.CTkTextbox(frame_visualizacao, width=600, height=150)
    caixa_texto2_emprestimo.pack(pady=(20, 10))

    botao_estatistica = customtkinter.CTkButton(frame_visualizacao, text='Estatística', font=('Ariel', 14, 'bold'), command=tela_estatistica)
    botao_estatistica.pack(pady=(10, 10))

    # Frame para o sistema de remoção de alunos
    frame_remocao = customtkinter.CTkFrame(janela_3_emprestimo)
    frame_remocao.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
    frame_remocao.grid_columnconfigure(0, weight=1)  # Centralizar os widgets
    frame_remocao.grid_columnconfigure(1, weight=1)  # Centralizar os widgets

    devolucao = customtkinter.CTkLabel(frame_remocao, text='Devolução', font=('Ariel', 36, 'bold'))
    devolucao.grid(row=0, column=0, columnspan=2, pady=(20, 10), sticky='ew')

    nome_emp = customtkinter.CTkEntry(frame_remocao, width=200, placeholder_text='Nome Aluno')
    nome_emp.grid(row=1, column=0, padx=20, pady=40)
    nome_emp.bind("<Return>", lambda event: apertar_enter(event, lvro))

    lvro = customtkinter.CTkEntry(frame_remocao, width=200, placeholder_text='Titulo do Livro')
    lvro.grid(row=1, column=1, padx=20, pady=40)

    data_real = customtkinter.CTkEntry(frame_remocao, width=200, placeholder_text='Data Real')
    data_real.grid(row=2, column=0, columnspan=2, pady=10)
    atualizar_data(frame_remocao, data_real)

    botao_concluir = customtkinter.CTkButton(frame_remocao, text='Concluir', font=('Ariel', 14, 'bold'), command=lambda :
                                             registrar_devolucao(nome_emp, lvro, data_real, master=frame_remocao))
    botao_concluir.grid(row=3, column=0, columnspan=2, pady=30)


    linha = customtkinter.CTkFrame(frame_remocao, height=2, fg_color='gray')
    linha.grid(row=4, column=0, columnspan=2, padx=10, pady=8, sticky="ew")

    label_remocao = customtkinter.CTkLabel(frame_remocao, text='Remover Empréstimo', font=('Ariel', 36, 'bold'),
     text_color='Red')
    label_remocao.grid(row=5, column=0, columnspan=2, pady=(20, 10), sticky="ew")

    info_remocao = customtkinter.CTkLabel(frame_remocao, text='[ Remover Empréstimo se necessário após 1 ano da sua data. ]', font=('Ariel', 14, 'bold'))
    info_remocao.grid(row=6, column=0, columnspan=2, pady=(10, 10), sticky="ew")

    id_emprestimo = customtkinter.CTkEntry(frame_remocao, width=200, placeholder_text='ID Empréstimo')
    id_emprestimo.grid(row=7, column=0, padx=10, pady=40)
    id_emprestimo.bind("<Return>", lambda event: apertar_enter(event, nome_remove_emprestimo))

    nome_remove_emprestimo = customtkinter.CTkEntry(frame_remocao, width=200, placeholder_text='Nome do Aluno')
    nome_remove_emprestimo.grid(row=7, column=1, padx=10, pady=40)

    botao_remover_aluno = customtkinter.CTkButton(frame_remocao, text='Remover', font=('Ariel', 14, 'bold'),
    fg_color='Red', command=lambda : remover_emprestimo(id_emprestimo, nome_remove_emprestimo, master=frame_remocao))
    botao_remover_aluno.grid(row=8, column=0, columnspan=2, pady=10)


def tela_estatistica():
    customtkinter.set_appearance_mode('dark')
    customtkinter.set_default_color_theme('dark-blue')

    janela_4_emprestimo = customtkinter.CTkToplevel()
    janela_4_emprestimo.geometry("400x300")

    janela_4_emprestimo.title('Gerenciamento de Biblioteca')

    titulo = customtkinter.CTkLabel(janela_4_emprestimo, text='Estatística', font=('Ariel', 36, 'bold'))
    titulo.pack(pady=10)

    caixa_texto2_emprestimo = customtkinter.CTkTextbox(janela_4_emprestimo, width=400, height=70)
    caixa_texto2_emprestimo.pack(pady=10)

    botao_ok = customtkinter.CTkButton(janela_4_emprestimo, text='OK', font=('Ariel', 14, 'bold'), command=janela_4_emprestimo.destroy)
    botao_ok.pack(pady=60)

    def busca_automatica_visualizar_emp():
        obter_estatisticas_emprestimo(caixa_texto2_emprestimo)
        janela_4_emprestimo.after(500, busca_automatica_visualizar_emp)

    busca_automatica_visualizar_emp()

