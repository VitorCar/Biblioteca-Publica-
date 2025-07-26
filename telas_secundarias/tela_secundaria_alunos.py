from logica_sistema.alunos import *
from excel.export_excel import *
import customtkinter

background_color = "#1a1a1a"

def tela_vizualizacao_remover_alunos():
    customtkinter.set_appearance_mode('dark')
    customtkinter.set_default_color_theme('dark-blue')

    janela_2_alunos = customtkinter.CTkToplevel()
    janela_2_alunos.geometry("1072x768")

    janela_2_alunos.title('Gerenciamento de Biblioteca')

    # Configurar o grid para ter duas colunas com pesos iguais
    janela_2_alunos.grid_columnconfigure(0, weight=1)  # Coluna da visualização de livros
    janela_2_alunos.grid_columnconfigure(1, weight=1)  # Coluna do sistema de remoção de livros
    janela_2_alunos.grid_rowconfigure(0, weight=1)  # Uma única linha que ocupa toda a altura

    # Frame para a visualização de livros
    frame_visualizacao = customtkinter.CTkFrame(janela_2_alunos)
    frame_visualizacao.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
    label_visualizacao = customtkinter.CTkLabel(frame_visualizacao, text="Visualização de Alunos",
                                                font=('Ariel', 36, 'bold'))
    label_visualizacao.pack(padx=20, pady=10)

    caixa_texto_alunos = customtkinter.CTkTextbox(frame_visualizacao, width=600, height=250)
    caixa_texto_alunos.pack(pady=20)

    # funçao que atualiza os dados
    def busca_automatica_viz_laluno():
        vizualizar_alunos(caixa_texto_alunos)
        janela_2_alunos.after(500, busca_automatica_viz_laluno)

    busca_automatica_viz_laluno()

    entrada_pesquisar_alunos = customtkinter.CTkEntry(frame_visualizacao, width=300, placeholder_text='Nome do Aluno')
    entrada_pesquisar_alunos.pack(pady=(40, 10))
    entrada_pesquisar_alunos.bind("<Return>", lambda event: apertar_enter(event, botao_pesquisar_alunos))
    botao_pesquisar_alunos = customtkinter.CTkButton(frame_visualizacao, text='Pesquisar', font=('Ariel', 14, 'bold'),
                                                     command=lambda: pesquisar_aluno(entrada_pesquisar_alunos,
                                                                                     caixa_texto2_alunos))
    botao_pesquisar_alunos.pack()

    caixa_texto2_alunos = customtkinter.CTkTextbox(frame_visualizacao, width=600, height=150)
    caixa_texto2_alunos.pack(pady=(20, 10))

    exporta_alunos = customtkinter.CTkButton(frame_visualizacao, text='Exportar Excel', font=('Ariel', 14, 'bold'), command=lambda :
                                             export_aluno(master=frame_visualizacao))
    exporta_alunos.pack(pady=20)

    # Frame para o sistema de remoção de alunos
    frame_remocao = customtkinter.CTkFrame(janela_2_alunos)
    frame_remocao.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
    frame_remocao.grid_columnconfigure(0, weight=1)  # Centralizar os widgets
    frame_remocao.grid_columnconfigure(1, weight=1)  # Centralizar os widgets

    label_remocao = customtkinter.CTkLabel(frame_remocao, text='Remover Aluno', font=('Ariel', 36, 'bold'),
                                           text_color='Red')
    label_remocao.grid(row=0, column=0, columnspan=2, pady=(20, 10), sticky="ew")

    info_aluno = customtkinter.CTkLabel(frame_remocao, text='[ Remover aluno só se for realmente necessário! ]', font=('Ariel', 14, 'bold'))
    info_aluno.grid(row=1, column=0, columnspan=2, pady=(10, 10), sticky="ew")

    id_aluno = customtkinter.CTkEntry(frame_remocao, width=200, placeholder_text='ID Aluno')
    id_aluno.grid(row=2, column=0, padx=20, pady=40)
    id_aluno.bind("<Return>", lambda event: apertar_enter(event, nome_remove_aluno))

    nome_remove_aluno = customtkinter.CTkEntry(frame_remocao, width=200, placeholder_text='Nome do Aluno')
    nome_remove_aluno.grid(row=2, column=1, padx=20, pady=40)

    botao_remover_aluno = customtkinter.CTkButton(frame_remocao, text='Remover', font=('Ariel', 14, 'bold'),
                                                  fg_color='Red', command=lambda: remover_aluno(id_aluno, nome_remove_aluno, master=frame_remocao))
    botao_remover_aluno.grid(row=3, column=0, columnspan=2, pady=20)

    linha = customtkinter.CTkFrame(frame_remocao, height=2, fg_color='gray')
    linha.grid(row=4, column=0, columnspan=2, padx=10, pady=8, sticky="ew")

    estatistica = customtkinter.CTkLabel(frame_remocao, text='Estatística', font=('Ariel', 36, 'bold'))
    estatistica.grid(row=5, column=0, columnspan=2, pady=(20, 10), sticky="ew")

    caixa_estat_alunos = customtkinter.CTkTextbox(frame_remocao, width=600, height=60)
    caixa_estat_alunos.grid(row=6, column=0, columnspan=2, pady=(20, 10))

    def busca_automatica_cont_al():
        quantidade_alunos_cadastrados(caixa_estat_alunos)
        janela_2_alunos.after(500, busca_automatica_cont_al)

    busca_automatica_cont_al()

