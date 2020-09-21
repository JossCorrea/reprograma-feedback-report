# Instruções para gerar relatórios:

1) Instale o python 3 e o gerenciador de pacotes pip 

2) Instale o venv (caso não esteja presenta na instalação do python)

3) Rode o commando abaixo para criar um abiente virtual
   `python3 -m venv venv`

4) Rode o comando abaixo para ativar o ambiente virtual (esteja na pasta do projeto):
    `source venv/bin/activate`

    >Nota: Na linha de commando vai aparecer (venv) indicando que o ambiente foi inicializado

5) Rode o comando abaixo para instalar as dependências do projeto:
    `pip install -r requirements.txt`

6) Baixe a planilha de feedbacks do seu drive no formato .tsv e substitua o arquivo feedback.tsv pelo seu arquivo (importante deixar apenas o arquivo que será lido)

7) Na linha de commando digite `python build-report.py`. O script solicitará as seguintes informações:
- Número da semana
- Tema da semana (mesmo do cronograma)
- Nome da professora
- Data que ocorreu a aula no formato dd/mm/aaaa ( o dia que é considerado início da semana) 

8) Se tudo correr bem o script vai gerar um pdf no próprio diretório, só dar uma conferida no resultado e ser feliz

9) Se algo der ruim, tira um print, me manda no zap/slack ou abre uma issue no repo

10) Aproveite o tempo que você ganhou relaxando!


Beijos

Jô Corrêa