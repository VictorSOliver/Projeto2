"""
select Nome, DataNascimento, Descricao, SaldoInicial;
from Usuario;
join Contas on Usuario.idUsuario = contas.Usuario_idUsuario;
where SaldoInicial >= 235 and UF = 'ce' and CEP <> '62930000';

select idUsuario, Nome, DataNascimento, Descricao, SaldoInicial, UF, Descrição;
from Usuario;
join Contas on Usuario.idUsuario = Contas.Usuario_idUsuario;
join TipoConta on TipoConta.idTipoConta = Contas.TipoConta_idTipoConta;
where SaldoInicial < 3000 and UF = 'ce' and Descrição <> 'Conta Corrente' and idUsuario > 3;
"""
import sqlparse
import re

comando = input('Digite o comando SQL: ')

lista_comando = sqlparse.split(comando)
lista_comando[-1] = lista_comando[-1].replace('and', '^')
banco = {
    'Usuario': ['idUsuario', 'Nome', 'Logradouro', 'Numero', 'Bairro', 'CEP', 'UF', 'DataNascimento'],
    'Contas': ['idConta', 'Descricao', 'TipoConta_idTipoConta', 'Usuario_idUsuario', 'SaldoInicial'],
    'TipoConta': ['idTipoConta', 'Descricao'],
    'Movimentacao': ['idMovimentacao', 'DataMovimetacao', 'Descricao', 'TipoMovimento_idTipoMovimento',
                     'Categoria_idCategoria', 'Contas_idContas', 'Valor'],
    'TipoMovimento': ['idTipoMovimento', 'DescMovimentacao'],
    'Categoria': ['idCategoria', 'DescCategoria']
}

re_projecao = re.split(r'select|,\s|;', lista_comando[0])
retirar = ['select', ';']
incluir = ['π', '']
projecao = lista_comando[0]
for i in range(0, len(retirar)):
    projecao = projecao.replace(retirar[i], incluir[i])
lista_projecao = ' '.join(re_projecao).split()
# print(projecao)

tabelas = set()
for chave in banco.keys():
    for linha in lista_comando:
        if chave in linha:
            tabelas.add(chave)
tabelas = list(tabelas)
# print(tabelas)

junc = []
for linha in lista_comando[1: -1]:
    if 'join' in linha:
        reg_juncao = re.search(r'^join\s\w+\son\s\w+.(\w+\s=\s\w+.\w+);', linha)
        linha_mod = reg_juncao.group(1)
        print(linha_mod)
        re_juncao = re.search(r'\w+\s=\s(\w+.)\w+', linha_mod)
        linha_mod = linha_mod.replace(re_juncao.group(1), '')
        linha_mod = linha_mod.replace('=', '')
        junc.extend(linha_mod.split())
dict_juncoes = {}
for tabela in tabelas:
    for chave in junc:
        if chave in banco[tabela]:
            dict_juncoes[tabela] = chave
# print(dict_juncoes)

dict_selecao = {}
for tabela in tabelas:
    dict_selecao[tabela] = []
reg_selecao = re.search(r"(\w+\s[<>=]+\s'?((?<=')\w+\s?\w+?'|\w+)|\s\^\s\w+\s[<>=]+\s'?((?<=')\w+\s?\w+?'|\w+))+",
                        lista_comando[-1])
str_selecao = reg_selecao.group()
# print(str_selecao)
lista_selecao = str_selecao.split(sep='^')
# print(lista_selecao)
for tabela in tabelas:
    for str in lista_selecao:
        reg = re.search(r'\w+', str)
        if reg.group(0) in banco[tabela]:
            dict_selecao[tabela].append(re.search(r"\w+\s[<>=]+\s'?((?<=')\w+\s?\w+?'|\w+)", str).group(0))
for chave in dict_selecao.keys():
    if len(dict_selecao[chave]) > 1:
        s = ''
        for i in range(0, len(dict_selecao[chave]) - 1):
            s = s + f'{dict_selecao[chave][i]} ^ '
        s = s + f'{dict_selecao[chave][-1]}'
        dict_selecao[chave].append(s)
# print(tabela_selecao)

# Montagem da álgebra relacinonal
indice_tabela = list(dict_selecao.keys())
juncoes = []
for tabela in dict_juncoes:
    str_selecao = f'π {dict_juncoes[tabela]}'
    for atb_proj in lista_projecao:
        for atb_selecao in dict_selecao[tabela]:
            if atb_proj in atb_selecao:
                str_selecao += f' ^ {atb_proj}'
    juncoes.append(str_selecao)
# print(juncoes)

# Montagem da árvore
if len(tabelas) == 1:
    algebra_relacional = f'{projecao}(σ {dict_selecao[indice_tabela[0]][-1]}({tabelas[0]}))'
    print(f'\nAlgébra relacional:')
    print(algebra_relacional)
    reg_tabelas = re.findall(r'\(\w+\)', algebra_relacional)
    reg_selecoes = re.findall(r"(σ\s\w+\s[<>=]+\s'?((?<=')\w+\s?\w+?'|\w+)"
                              r"(\s\^\s\w+\s[<>=]+\s'?((?<=')\w\s?\w+?')|\w+)+?)", algebra_relacional)
    reg_projecoes = re.findall(r"(π\s\w+(\s\^\s?\w+)?)", algebra_relacional)
    str_arvore = f'1º{reg_tabelas[0]} 2º{reg_selecoes[0][0]} 3º{reg_projecoes[0][0]}'
elif len(tabelas) == 2:
    i = 0
    j = 1
    algebra_relacional = f'{projecao}(({juncoes[i]}(σ {dict_selecao[indice_tabela[i]][-1]}({tabelas[i]}))) |X| ' \
                         f'({juncoes[j]}(σ {dict_selecao[indice_tabela[j]][-1]}({tabelas[j]}))))'
    print('\nAlgébra relacional:')
    print(algebra_relacional)
    reg_tabelas = re.findall(r'\(\w+\)', algebra_relacional)
    reg_selecoes = re.findall(r"(σ\s\w+\s[<>=]+\s'?((?<=')\w+\s?\w+?'|\w+)"
                              r"(\s\^\s\w+\s[<>=select Nome, DataNascimento, Descricao; from Usuario; join Contas on Usuario.idUsuario = Contas.Usuario_idUsuario; where SaldoInicial > 235 and UF = 'ce' and CEP <> '62930000']+\s'?((?<=')\w\s?\w+?')|\w+)+?)", algebra_relacional)
    reg_projecoes = re.findall(r"\((π\s\w+(\s\^\s?\w+)?)", algebra_relacional)
    str_arvore = f'1º{reg_tabelas[i]} 2º{reg_selecoes[i][0]} 3º{reg_projecoes[i][0]} 4º{reg_tabelas[j]} ' \
                 f'5º{reg_selecoes[j][0]} 6º{reg_projecoes[j][0]} ' \
                 f'7º{dict_juncoes[indice_tabela[i]]} |X| {dict_juncoes[indice_tabela[j]]} 8º{projecao}'

print(f'\nÁrvore:')
print(str_arvore)



