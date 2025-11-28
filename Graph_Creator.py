import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import pandas as pd
import easygui as eg
import sys

def main():
    def criardf():

        file_path = eg.fileopenbox(title="Selecione um arquivo CSV ou Excel para abrir")
        
        if file_path:
            try:

                if file_path.endswith('.csv'):
                    # Lê o arquivo CSV e retorna o DataFrame
                    df = pd.read_csv(file_path)
                    print("Arquivo CSV lido com sucesso!")
                    return df
                elif file_path.endswith(('.xls', '.xlsx')):
                    # Lê o arquivo Excel e retorna o DataFrame
                    df = pd.read_excel(file_path, engine='openpyxl')
                    print("Arquivo Excel lido com sucesso!")
                    return df
                else:
                    print("O arquivo selecionado não é um CSV ou Excel.")
                    return criardf()
            except Exception as e:
                print(f"Erro ao processar o arquivo: {e}")
                sys.exit()
                return
        else:
            print("Nenhum arquivo foi selecionado.")
            sys.exit()
            return

    def formata_csv(df):
        #indexando colunas
        primeira_coluna = df.columns[0]
        df = df.set_index(primeira_coluna) 
        #Tratando nome das colunas
        df.columns = [x.upper() for x in df.columns]
        #completando espaços vazios
        df = df.apply(lambda col: col.fillna(col.mean()) if col.dtype in ['float64', 'int64'] else col)
        df = df.dropna(axis="columns")
        #se a coluna for int ou float substitui o NaN pela média dos valores. Se for outro tipo ele tira ela
        return df

    def define_colunas(df):
        col_csv_index = df.columns
        col_csv = []
        for i in col_csv_index:
            col_csv.append(i)
        col_csv2 = ", ".join(col_csv)
        print(f"As colunas existentes são: {col_csv2}")
        colunas = []
        while True:
            ans = input("Insira as colunas que serão inseridas no gráfico/ Digite 'fim' ou ' ' para finalizar: ")
            ans = ans.upper()
            if ans == "" or ans.lower() == "fim":
                break
            if ans not in df.columns:
                print("Coluna não encotrada, insira o nome corretamente")
                continue
            colunas.append(ans)
            print(f"Colunas selecionadas: {", ".join(colunas)}")
        return df[colunas],colunas

    def opera_colunas(df,resposta):
        resposta = resposta.upper()
        col_csv_index = df.columns
        col_csv = []
        for i in df.columns:
            col_csv.append(i)
        col_csv2 = ", ".join(col_csv)   
        print(f"Colunas existentes: {col_csv2}")
        if resposta == "SOMAR":
            operação = "somada"
            simbolo = "+"
        elif resposta == "SUBTRAIR":
            operação = "subtraída"
            simbolo = "-"
        elif resposta == "MULTIPLICAR":
            operação = "multiplicada"
            simbolo = "*"
        elif resposta == "DIVIDIR":
            operação = "dividida"
            simbolo = "/"
        
        while True:
            col1 = input(f"selecione a primeira coluna para ser {operação}: ").upper()
            col2 = input(f"selecione a segunda coluna para ser {operação}: ").upper()
            if col1 not in col_csv_index or col2 not in col_csv_index:
                print("Uma das colunas inseridas não existe, insira os nomes corretamente")
            else:   
                break
        valores_col1 = df[col1].tolist()
        valores_col2 = df[col2].tolist()
        opera_lista = []
        if resposta == "SOMAR":
            for i,valor in enumerate(valores_col1):
                soma_valor = round(valores_col1[i] + valores_col2[i], 2)
                opera_lista.append(soma_valor)
        elif resposta == "SUBTRAIR":
            while True:
                pergunta_valor_menor_que_zero = input("A coluna deve aceitar valores menores que 0? [S/N]: ").upper()
                if pergunta_valor_menor_que_zero == "S":
                    valor_menor_que_zero = True
                    break
                elif pergunta_valor_menor_que_zero == "N":
                    valor_menor_que_zero = False
                    break
                else:
                    print("Insira 'S' para incluir valores negativos e 'N' para não incluir valores negativos")
                    continue
            for i,valor in enumerate(valores_col1):
                subtrai_valor = round(valores_col1[i] - valores_col2[i], 2)
                if not valor_menor_que_zero and subtrai_valor < 0:
                    subtrai_valor = 0
                opera_lista.append(subtrai_valor)
        elif resposta == "MULTIPLICAR":
            for i,valor in enumerate(valores_col1):
                multiplica_valor = round(valores_col1[i] * valores_col2[i], 2)
                opera_lista.append(multiplica_valor)
        elif resposta == "DIVIDIR":
            for i,valor in enumerate(valores_col1):
                divide_valor = round(valores_col1[i] / valores_col2[i], 2)
                opera_lista.append(divide_valor)
        nome_coluna = col1+simbolo+col2
        df[f"{nome_coluna}"] = opera_lista
        print(f"Colunas atualizadas: {col_csv2 + ", " + nome_coluna}")
        return df


    def completa_lista(lista1,lista2):
        if len(lista1) > len(lista2):
            lista2.extend([0] * (len(lista1) - len(lista2))) #preenche os espaços vazios com 0 no eixo y
            print('O número de valores no eixo x é maior do que no eixo y')
            return lista1, lista2
        
        elif len(lista1) < len(lista2):
            lista1.extend(['Valor(es) não definido(s)'] * (len(lista2) - len(lista1))) #preenche os espaços vazios com 'Valor não difinido' no eixo x
            print('O número de valores no eixo y é maior do que no eixo x')
            return lista1, lista2
                
    def cria_barras(lista_eixo_x,lista_eixo_y,nome_eixo_x = None,nome_eixo_y = None,cor_preenchimento = None,cor_contorno = None,titulo=None): #hex RBG/RGBA ou notação da lib            
        try:
            completa_lista(lista_eixo_x,lista_eixo_y)
            plt.xlabel(nome_eixo_x)
            plt.ylabel(nome_eixo_y)
            plt.tight_layout()
            plt.xticks(rotation = 25, ha = 'right')
            plt.axis([-0.5,-0.5+len(lista_eixo_x),0,max(lista_eixo_y)+ 5]) #delimita o espaçamento do gráfico
            plt.grid(True,axis = 'y',linestyle = ('--'))
            plt.gca().yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
            plt.gca().yaxis.set_major_locator(LinearLocator(numticks = 10))
            plt.title(titulo)
            plt.bar(lista_eixo_x,lista_eixo_y,facecolor = cor_preenchimento,edgecolor = cor_contorno)

            plt.show()

        except:
            print('Tem um erro')

    def cria_linhas(lista_eixo_x,lista_eixo_y,lista_nome_linha = ['Linha1'] ,nome_eixo_x = None,nome_eixo_y = None,titulo=None): #hex RBG/RGBA ou notação da lib  
            def traça_linha(nome_linha,cor = None):
                    #Eixo y é a lista da coluna selecionada
                    lista_y = lista_eixo_y[i]
                    completa_lista(lista_eixo_x,lista_y)

                    #Nomeia os eixos e o gráfico
                    plt.xlabel(nome_eixo_x) 
                    plt.ylabel(nome_eixo_y)
                    plt.title(titulo)

                    #Estilização
                    plt.tight_layout()
                    plt.xticks(rotation = 35, ha = 'right')
                    plt.grid(True,linestyle = ('--'))

                    #Deixa o eixo y em decimais e limita a 10 valores
                    plt.gca().yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
                    plt.gca().yaxis.set_major_locator(LinearLocator(numticks = 10))

                    #Desenha o gráfico
                    plt.plot(lista_eixo_x,lista_y,color = cor, linestyle = '-', label = nome_linha)    

            def escolhe_cor():
                #Dicionário de cores
                dicionario_cores = mcolors.CSS4_COLORS

                #Busca a cor inputada no dicionário
                while True:
                        cor_resposta = input('Insira o nome de uma cor em inglês: ').lower()
                        try:
                            cor = dicionario_cores[cor_resposta]
                            return cor
                        except:
                            print('Essa cor não está disponível')

            opção = input('Você quer escolher a cor das linhas? [S/N]')
            for i,nome in enumerate(lista_nome_linha):
                if not opção == 'S':
                    traça_linha(nome)
                else:
                    traça_linha(nome,escolhe_cor())

            #Cria a legenda e mostra o gráfico
            plt.legend()
            plt.show()

    def pega_titulo(msg):
        titulo = input(msg)
        if titulo == '':
            return None
        else:
            return titulo
        

    print('Selecione um arquivo válido(Excel ou CSV)')    
    df = criardf()
    df = formata_csv(df)

    while True:
        pergunta_operacao = input("Deseja realizar alguma operação entre colunas? (soma ou subtração) [S/N] ").upper()
        if pergunta_operacao == "S":
            tipo_operacao = input("Insira a operação que deseja ['+' -> Soma / '-' -> Subtração / '*' -> Multiplicação / '/' -> Divisão]: ")
            if tipo_operacao == "+":
                opera_colunas(df,"somar")
            elif tipo_operacao == "-":
                opera_colunas(df,"subtrair")
            elif tipo_operacao == "*":
                opera_colunas(df,"multiplicar")
            elif tipo_operacao == "/":
                opera_colunas(df, "dividir")
            else:
                print("Insira '+' para somar, '-' para subtrair,  '*' para multiplicar e '/' para dividir")
        elif pergunta_operacao == "N":
            break
        else:
            print("Insira 'S' caso deseje realizar alguma operação ou 'N' caso não deseje realizar uma operação")
    new_df, coluna = define_colunas(df)

    xlist = []
    for i in new_df.index:
        xlist.append(str(i)) 

    ylist = []
    for i in coluna:
        ylist.append(new_df[i].tolist())    

    name_list = coluna

    titulo_grafico = pega_titulo('Digite o título do seu gráfico: ')
    titulo_x = pega_titulo('Digite o título para o eixo x do seu gráfico: ') 
    titulo_y = pega_titulo('Digite o título para o eixo y do seu gráfico: ' )
    
    cria_linhas(xlist,ylist,nome_eixo_y = titulo_y,nome_eixo_x = titulo_x, lista_nome_linha = name_list, titulo = titulo_grafico)
    
if __name__ == '__main__':
    main()