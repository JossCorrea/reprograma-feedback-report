# coding: utf-8
import pandas as pd
from datetime import datetime, timedelta
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
import os

# Um valor por linha
def aggregateByLineValues(dataframe, columnName, totalRows):
    f = lambda x: round(100*x/totalRows,1)
    g = lambda x: f'{x} %'
   
    table = dataframe[[columnName]].fillna('Não respondeu').value_counts()
    return (table.sort_values(ascending=False).apply(f)).apply(g)    


# Vários valores por linha
def aggregateByLineMultivalues(dataframe, columnName):
    f = lambda x: round(100*x/dataframe.shape[0],1)
    g = lambda x: f'{x} %'

    table = (dataframe[columnName]).fillna('Não respondeu')
    df_table = pd.DataFrame(table.str.split(',')).explode(columnName).value_counts()
    return (df_table.sort_values(ascending=False).apply(f)).apply(g) 


def main():
    print("---------------------------------------------------------------------------")
    print("                           {Reprograma Tools}                              ")
    print("                  Report de feedback de professoras                        ")
    print("---------------------------------------------------------------------------")

    semana = input('Digite o número da semana que deseja gerar o relatório: ')
    tema = input('Digite o tema da semana (mesmo do cronograma): ')
    professora = input ('Digite o nome da professora da semana: ')
    dt_aula = input('Digite a data que ocorreu a aula no formato dd/mm/aaaa: ')
        
    #1. Extração

    # 1.1 Avaliações
    arquivo = os.getcwd()+'/data/'+os.listdir(os.getcwd()+'/data')[0]
    df_avaliacoes_raw = pd.read_csv(arquivo, sep='\t', header=0)
    
    #Removendo espaços nos nomes das colunas
    columns = list(df_avaliacoes_raw.columns)
    new_columns = dict()

    for column in columns:
        new_columns[column] = str(column.rstrip(' '))

    df_avaliacoes = df_avaliacoes_raw.rename(columns=new_columns,inplace=False)

    # 1.2 Período considerado na avaliação
    dt_inicio = datetime.strptime(dt_aula,"%d/%m/%Y" )  
    dt_fim = dt_inicio + timedelta(days = 6)

    # 2. Transformação

    # 2.1 Conversão das datas de string para data
    df_avaliacoes['Submitted At'] = pd.to_datetime(df_avaliacoes['Submitted At'])

    # 2.2 Filtrando dados por intervalo de datas (semana)
    filtro_semana = (df_avaliacoes['Submitted At'] >= dt_inicio) & (df_avaliacoes['Submitted At'] <= dt_fim)
    df_sem = df_avaliacoes[filtro_semana]

    # 2.3 Calculando valores dos relatórios
    total_respostas = df_sem.shape[0]

    media_dedicacao = df_sem[['O quanto você se dedicou essa semana?']].mean()
    media_aprendizado = df_sem[['O quanto você acha que aprendeu sobre o tema dessa semana?']].mean()

    #  2.3.1 Tabela 1 - Avaliação conteúdo
    df_table1 = aggregateByLineValues(df_sem,'Como você avalia o conteúdo apresentado nessa semana?', total_respostas)

    #  2.3.2 Tabela 2 - Motivos avaliação conteúdo
    df_table2 = aggregateByLineMultivalues(df_sem,'Qual(is) o(s) motivo(s) para esta avaliação sobre o conteúdo?')

    #  2.3.3 Tabela 3 - Conteúdos não compreendidos
    df_table3 = aggregateByLineValues(df_sem,'Dos conteúdos vistos essa semana, existe algum que você  considera não ter compreendido?', total_respostas)

    #  2.3.4 Tabela 4 - Avaliação professora
    df_table4 = aggregateByLineValues(df_sem,'Como você avalia a professora dessa semana?', total_respostas)

    #  2.3.5 Tabela 5 - Motivos Avaliação professora
    df_table5 = aggregateByLineMultivalues(df_sem,'Qual(is) o(s) motivo(s) para esta avaliação da professora?')

    #  2.3.6 - Avaliação monitoria 
    media_monitoria = df_sem[['Como você avalia a sua experiência com o plantão de dúvidas no slack essa semana?']].mean()

    #  2.3.7 Tabela 6 - Motivos Avaliação monitoria
    df_table6 = aggregateByLineMultivalues(df_sem,'Qual(is) o(s) motivo(s) para esta avaliação sobre o plantão de dúvidas?')

    #  2.3.8 Tabela 7 - Oportunidades de melhoria
    df_table7 = aggregateByLineValues(df_sem,'O que poderia ser melhorado nessa semana?',total_respostas)

    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template("template.html")


    # 3. Gerar report
    # 3.1 - Configuração do template
    template_vars = {
        "semana" : 'Semana ' + semana,
        "assunto": tema,
        "professora": professora,
        "media_dedicacao" : round(media_dedicacao.values[0],1),
        "media_aprendizado" : round(media_aprendizado.values[0],1),
        "media_monitoria": round(media_monitoria.values[0],1),
        "df_table1" : df_table1.to_frame().rename(columns={0:''},inplace=False).to_html(),
        "df_table2" : df_table2.to_frame().rename(columns={0:''},inplace=False).to_html(),
        "df_table3" : df_table3.to_frame().rename(columns={0:''},inplace=False).to_html(),
        "df_table4" : df_table4.to_frame().rename(columns={0:''},inplace=False).to_html(),
        "df_table5" : df_table5.to_frame().rename(columns={0:''},inplace=False).to_html(),
        "df_table6" : df_table6.to_frame().rename(columns={0:''},inplace=False).to_html(),
        "df_table7" : df_table7.to_frame().rename(columns={0:''},inplace=False).to_html()
    }

    html_out = template.render(template_vars)

    #3.2 - Gerando PDF
    HTML(string=html_out).write_pdf(f'Report_semana_{semana}.pdf', stylesheets=["style.css"])

if __name__ == "__main__":
    main()
