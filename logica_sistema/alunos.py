from logica_sistema.logica_sistema import *
from database_connector import *


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
