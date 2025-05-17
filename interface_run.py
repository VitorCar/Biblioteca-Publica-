from logica_sistema import *
from telas_secundarias import *
import customtkinter as ctk
import customtkinter

customtkinter.set_appearance_mode('dark')
customtkinter.set_default_color_theme('dark-blue')

background_color = "#1a1a1a"

janela = customtkinter.CTk()
janela.geometry('1200x700')
janela.title('Gerenciamento de Biblioteca')
janela.grid_columnconfigure(0, weight=1)

# frame a esquerda
frame = customtkinter.CTkFrame(janela, fg_color=background_color)
frame.pack(fill='x', padx=20)

#criando titulo
titulo = customtkinter.CTkLabel(frame, text='BIBLIOTECA PÚBLICA', font=('Ariel', 36, 'bold'))
titulo.pack(pady=(20, 10))

#-------------- LIVROS -----------------
livros = customtkinter.CTkLabel(janela, text='Novos Livros', font=('Ariel', 22, 'bold'), anchor='w', justify='left' )
livros.pack(anchor='w')

#frame lado a lado
frame_lado = customtkinter.CTkFrame(janela, fg_color=background_color)
frame_lado.pack(pady=20)

entrada_titulo = customtkinter.CTkEntry(frame_lado, width=180, placeholder_text='Título')
entrada_titulo.grid(row=0, column=0, padx=5, pady=5)
entrada_titulo.bind("<Return>", lambda event: apertar_enter(event, entrada_autor))

entrada_autor = customtkinter.CTkEntry(frame_lado, width=180, placeholder_text='Autor')
entrada_autor.grid(row=0, column=1, padx=5, pady=5)
entrada_autor.bind("<Return>", lambda event: apertar_enter(event, entrada_editora))


entrada_editora = customtkinter.CTkEntry(frame_lado, width=180, placeholder_text='Editora')
entrada_editora.grid(row=0, column=2, padx=5, pady=5)
entrada_editora.bind("<Return>", lambda event: apertar_enter(event, ano_publicacao))


ano_publicacao = customtkinter.CTkEntry(frame_lado, width=180, placeholder_text='Ano_publicação')
ano_publicacao.grid(row=0, column=3, padx=5, pady=5)
ano_publicacao.bind("<Return>", lambda event: apertar_enter(event, qtd_total))


qtd_total = customtkinter.CTkEntry(frame_lado, width=180, placeholder_text='Qtd_Total')
qtd_total.grid(row=0, column=4, padx=5, pady=5)
qtd_total.bind("<Return>", lambda event: apertar_enter(event, qtd_disponivel))

qtd_disponivel= customtkinter.CTkEntry(frame_lado, width=180, placeholder_text='Qtd_Disponivel')
qtd_disponivel.grid(row=0, column=5, padx=5, pady=5)


entrada_titulo.grid_columnconfigure(0, weight=1) # Título e "NOVOS LIVROS" ocupam o máximo
entrada_autor.grid_columnconfigure(1, weight=1) # Espaço para os campos se a janela aumentar
entrada_editora.grid_columnconfigure(2, weight=1)
ano_publicacao.grid_columnconfigure(3, weight=1)
qtd_total.grid_columnconfigure(4, weight=1)
qtd_disponivel.grid_columnconfigure(5, weight=1)

# BOTOES LIVROS
frame_botao = customtkinter.CTkFrame(janela, fg_color=background_color)
frame_botao.pack(pady=20)

adicionar_livro = customtkinter.CTkButton(frame_botao, text='Adicionar', font=('Ariel', 14, 'bold')
, command=lambda: adicionar_valores_livros(entrada_titulo, entrada_autor, entrada_editora, ano_publicacao, qtd_total, qtd_disponivel, master=janela))
adicionar_livro.grid(row=0, column=0, padx=5, pady=5)

visualizar_livros = customtkinter.CTkButton(frame_botao, text='Visualizar', font=('Ariel', 14, 'bold'), command=tela_visualizacao_remover)
visualizar_livros.grid(row=0, column=1, padx=5, pady=5)

linha = customtkinter.CTkFrame(janela, height=2, fg_color='gray')
linha.pack(pady=8, fill="x")

#------------- ALUNOS -----------------
alunos = customtkinter.CTkLabel(janela, text='Novos Alunos', font=('Ariel', 22, 'bold'), anchor='w', justify='left')
alunos.pack(anchor='w')

frame_lado_alunos = customtkinter.CTkFrame(janela, fg_color=background_color)
frame_lado_alunos.pack(pady=10)

nome = customtkinter.CTkEntry(frame_lado_alunos, width=180, placeholder_text='Nome Completo')
nome.grid(row=0, column=0, padx=5, pady=5)
nome.bind("<Return>", lambda event: apertar_enter(event, matricula))


matricula = (customtkinter.CTkEntry(frame_lado_alunos, width=180, placeholder_text='Matricula[5 dígitos]'))
matricula.grid(row=0, column=1, padx=5, pady=5)
matricula.bind("<KeyRelease>", lambda event: validar_matricula(event, matricula))
matricula.bind("<Return>", lambda event: apertar_enter(event, email))

email = customtkinter.CTkEntry(frame_lado_alunos, width=180, placeholder_text='Email')
email.grid(row=0, column=2, padx=5, pady=5)
email.bind("<Return>", lambda event: apertar_enter(event, celular))

celular = customtkinter.CTkEntry(frame_lado_alunos, width=180, placeholder_text='Celular[9 dígitos]')
celular.bind("<KeyRelease>", lambda event: validar_celular(event, celular))
celular.grid(row=0, column=3, padx=5, pady=5)

nome.grid_columnconfigure(0, weight=1)
matricula.grid_columnconfigure(1, weight=1)
email.grid_columnconfigure(2, weight=1)
celular.grid_columnconfigure(3, weight=1)

# BOTOES ALUNOS
frame_botao_alunos = customtkinter.CTkFrame(janela, fg_color=background_color)
frame_botao_alunos.pack(pady=20)

botao_adicionar_aluno = customtkinter.CTkButton(frame_botao_alunos, text='Adicionar', font=('Ariel', 14, 'bold'), command=lambda: adicionar_aluno(nome, matricula, email, celular, master=janela))
botao_adicionar_aluno.grid(row=0, column=0, padx=5, pady=5)

visualizar_aluno = customtkinter.CTkButton(frame_botao_alunos, text='Visualizar', font=('Ariel', 14, 'bold'), command=tela_vizualizacao_remover_alunos)
visualizar_aluno.grid(row=0, column=1, padx=5, pady=5)

linha = customtkinter.CTkFrame(janela, height=2, fg_color='gray')
linha.pack(pady=8, fill="x")

#------------- EMPRESTIMO -----------------

emprestimo = customtkinter.CTkLabel(janela, text='Empréstimo', font=('Ariel', 22, 'bold'), anchor='w', justify='left')
emprestimo.pack(anchor='w')

frame_lado_emprestimo = customtkinter.CTkFrame(janela, fg_color=background_color)
frame_lado_emprestimo.pack(pady=10)

nome_aluno = customtkinter.CTkEntry(frame_lado_emprestimo, width=180, placeholder_text='Nome Aluno')
nome_aluno.grid(row=0, column=0, padx=5, pady=5)
nome_aluno.bind("<Return>", lambda event: apertar_enter(event, titulo_livro))

titulo_livro = customtkinter.CTkEntry(frame_lado_emprestimo, width=180, placeholder_text='Titulo Livro')
titulo_livro.grid(row=0, column=1, padx=5, pady=5)
#titulo_livro.bind("<Return>", lambda event: apertar_enter(event, data_real))

data_emprestimo = customtkinter.CTkEntry(frame_lado_emprestimo, width=180, placeholder_text='Data Empréstimo')
data_emprestimo.grid(row=0, column=2, padx=5, pady=5)
atualizar_data(janela, data_emprestimo)

data_prevista = customtkinter.CTkEntry(frame_lado_emprestimo, width=180, placeholder_text='Data Empréstimo previsto')
data_prevista.grid(row=0, column=3, padx=5, pady=5)
atualizar_data_prevista(janela, data_prevista)

#data_real = customtkinter.CTkEntry(frame_lado_emprestimo, width=180, placeholder_text='Data Real')
#data_real.grid(row=0, column=4, padx=5, pady=5)

nome_aluno.grid_columnconfigure(0, weight=1)
titulo_livro.grid_columnconfigure(1, weight=1)
data_emprestimo.grid_columnconfigure(2, weight=1)
data_prevista.grid_columnconfigure(3, weight=1)
#data_real.grid_columnconfigure(4, weight=1)

#------------- BOTOES EMPRESTIMO ------------

frame_botao_emprestimo = customtkinter.CTkFrame(janela, fg_color=background_color)
frame_botao_emprestimo.pack(pady=20)

adicionar_emprestimo = customtkinter.CTkButton(frame_botao_emprestimo, text='Empréstimo', font=('Ariel', 14, 'bold'),
                                               command= lambda: realizar_emprestimo(nome_aluno.get(), titulo_livro.get(),data_emprestimo.get(), data_prevista.get(), master=janela))
adicionar_emprestimo.grid(row=0, column=0, padx=5, pady=5)

visualizar_emprestimo = customtkinter.CTkButton(frame_botao_emprestimo, text='Visualizar', font=('Ariel', 14, 'bold'), command=tela_visualizacao_remover_emprestimo)
visualizar_emprestimo.grid(row=0, column=1, padx=5, pady=5)

exporta = customtkinter.CTkButton(janela, text='Exportar Excel', font=('Ariel', 14, 'bold'))
exporta.pack()

janela.mainloop()