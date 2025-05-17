import pandas as pd

from database_connector import *
exporta_livro = executar_consulta('SELECT * FROM livros')
#print(exporta_livro)
exporta_livro = pd.DataFrame(exporta_livro, columns=['id_livro', 'titulo', 'autor', 'editora', 'ano_publicacao', 'quantidade_total', 'quantidade_disponivel'])
exporta_livro.to_excel('Banco_de_dados_Livros.xlsx', index=False)