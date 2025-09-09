# Sistema de Gerenciamento de Biblioteca Pública

Este é um sistema completo de gerenciamento de biblioteca desenvolvido em **Python**, com interface gráfica em **CustomTkinter** e banco de dados **MySQL**. Ele permite gerenciar alunos, livros, registrar e devolver empréstimos, além de enviar e-mails automáticos em caso de devoluções atrasadas.

## Funcionalidades

- Cadastro de alunos com nome, matrícula, e-mail e telefone
- Cadastro de livros com controle de quantidade disponível
- Registro de empréstimos com datas previstas e reais de devolução
- Controle de devoluções com atualização automática do estoque
- Alerta de devolução atrasada via e-mail usando SMTP
- Pesquisa de empréstimos por nome do aluno
- Interface gráfica moderna e responsiva com CustomTkinter

## Tecnologias Utilizadas

- **Python 3**
- **MySQL** (banco de dados relacional)
- **CustomTkinter** (interface gráfica moderna)
- **SMTP (smtplib)** para envio de e-mails
- **dotenv** para gerenciamento seguro de variáveis como senha de e-mail
- **Pandas & os** Exportar para excel
##  Segurança

- As credenciais sensíveis (como e-mail e senha) são armazenadas em um arquivo `.env` e não devem ser expostas no repositório.

##    Imagens

- ![image](https://github.com/user-attachments/assets/fe00f0f6-7306-4ac4-b118-9adfcf1c8f75)
- ![image](https://github.com/user-attachments/assets/ba9c4821-ae1a-44f6-a4b3-c859316e26b1)


