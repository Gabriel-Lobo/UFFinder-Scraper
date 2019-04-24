import json
import requests
from bs4 import BeautifulSoup

def parse_html(url, **kwargs):
    if len(kwargs) > 0:
        url = url.format(**kwargs)

    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html, features="html.parser")

    return soup

options = {
    'ano_semestre': '20191',
    'departamento': 'd-98'
}

teste = parse_html('https://app.uff.br/graduacao/quadrodehorarios/?utf8=✓&page=0&q[anosemestre_eq]={ano_semestre}&q[disciplina_cod_departamento_eq]={departamento}', **options)
table = teste.find('tbody')

keys = ['codigo', 'disciplina', 'turma', 'modulo', 'segunda', 'terca', 'quarta', 'quinta', 'sexta']

disciplinas = []

for row in table.find_all('tr'):
    data = dict.fromkeys(keys)
    for index, column in zip(range(9), row.find_all('td')):
        data[keys[index]] = column.text.strip('\n')
    disciplinas.append(data)

json = json.dumps(disciplinas, indent=4)

print(json)
