from logica_sistema.livros import *
from excel.export_excel import *
import customtkinter

background_color = "#1a1a1a"

def tela_visualizacao_remover():
    customtkinter.set_appearance_mode('dark')
    customtkinter.set_default_color_theme('dark-blue')

    janela_2 = customtkinter.CTkToplevel()
    janela_2.geometry("1072x768")

    janela_2.title('Gerenciamento de Biblioteca')

    # Configurar o grid para ter duas colunas com pesos iguais
    janela_2.grid_columnconfigure(0, weight=1)  # Coluna da visualização de livros
    janela_2.grid_columnconfigure(1, weight=1)  # Coluna do sistema de remoção de livros
    janela_2.grid_rowconfigure(0, weight=1)  # Uma única linha que ocupa toda a altura

    # Frame para a visualização de livros
    frame_visualizacao = customtkinter.CTkFrame(janela_2)
    frame_visualizacao.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
    label_visualizacao = customtkinter.CTkLabel(frame_visualizacao, text="Visualização de Livros",
                                                font=('Ariel', 36, 'bold'))
    label_visualizacao.pack(padx=20, pady=10)

    caixa_texto = customtkinter.CTkTextbox(frame_visualizacao, width=600, height=250)
    caixa_texto.pack(pady=20)

    # funçao que atualiza os dados
    def busca_automatica():
        visualizar_livros(caixa_texto)
        janela_2.after(500, busca_automatica)

    busca_automatica()

    entrada_pesquisar = customtkinter.CTkEntry(frame_visualizacao, width=300, placeholder_text='Titulo do Livro')
    entrada_pesquisar.pack(pady=(40, 10))
    entrada_pesquisar.bind("<Return>", lambda event: apertar_enter(event, button_pesquisar))

    button_pesquisar = customtkinter.CTkButton(frame_visualizacao, text='Pesquisar', font=('Ariel', 14, 'bold'),
                                               command=lambda: pesquisar_livro(entrada_pesquisar,
                                                                               caixa_texto2))  # Assumindo que caixa_texto2 está no outro frame ou será criado
    button_pesquisar.pack()

    caixa_texto2 = customtkinter.CTkTextbox(frame_visualizacao, width=600, height=150)
    caixa_texto2.pack(pady=(20, 10))

    exporta = customtkinter.CTkButton(frame_visualizacao, text='Exportar Excel', font=('Ariel', 14, 'bold'), command=lambda : export_livro(master=frame_visualizacao))
    exporta.pack(pady=20)

    ##REMOVER-----------------------
    # Frame para o sistema de remoção de livros
    frame_remocao = customtkinter.CTkFrame(janela_2)
    frame_remocao.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
    frame_remocao.grid_columnconfigure(0, weight=1)  # Centralizar os widgets
    frame_remocao.grid_columnconfigure(1, weight=1)  # Centralizar os widgets

    label_remocao = customtkinter.CTkLabel(frame_remocao, text='Remover Livro', font=('Ariel', 36, 'bold'),
                                           text_color='Red')
    label_remocao.grid(row=0, column=0, columnspan=2, pady=(20, 10), sticky="ew")

    info_livro = customtkinter.CTkLabel(frame_remocao, text='[ Remover livro só se for realmente necessário! ]', font=('Ariel', 14, 'bold'))
    info_livro.grid(row=1, column=0, columnspan=2, pady=(10, 10), sticky="ew")

    id_livro = customtkinter.CTkEntry(frame_remocao, width=200, placeholder_text='ID Livro')
    id_livro.grid(row=2, column=0, padx=20, pady=40)
    id_livro.bind("<Return>", lambda event: apertar_enter(event, nome_remove_livro))

    nome_remove_livro = customtkinter.CTkEntry(frame_remocao, width=200, placeholder_text='Titulo do Livro')
    nome_remove_livro.grid(row=2, column=1, padx=20, pady=40)

    botao_remover_livro = customtkinter.CTkButton(frame_remocao, text='Remover', font=('Ariel', 14, 'bold'),
                                                  fg_color='Red', command=lambda: remover_livro(id_livro, nome_remove_livro, master=frame_remocao))
    botao_remover_livro.grid(row=3, column=0, columnspan=2, pady=20)

    linha = customtkinter.CTkFrame(frame_remocao, height=2, fg_color='gray')
    linha.grid(row=4, column=0, columnspan=2, padx=10, pady=8, sticky="ew")

    estatistica = customtkinter.CTkLabel(frame_remocao, text='Estatística', font=('Ariel', 36, 'bold'))
    estatistica.grid(row=5, column=0, columnspan=2, pady=(20, 10), sticky="ew")

    caixa_estat = customtkinter.CTkTextbox(frame_remocao, width=600, height=60)
    caixa_estat.grid(row=6, column=0, columnspan=2, pady=(20, 10))

    def busca_automatica_cont_lv():
        mensagem_estatisticas = obter_estatisticas_livros()
        caixa_estat.delete('1.0', 'end')
        caixa_estat.insert('end', mensagem_estatisticas)
        janela_2.after(500, busca_automatica_cont_lv)

    busca_automatica_cont_lv()
