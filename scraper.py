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

data = parse_html('https://app.uff.br/graduacao/quadrodehorarios/')
disci_select = data.find('select', {'id': 'iddepartamento_coordenacao'})

disci_list = disci_select.find_all('option')

keys = ['codigo', 'nome', 'disciplinas']

departamentos = []

for disci in disci_list:
    data = dict.fromkeys(keys)
    data['codigo'] = disci.get('value')
    data['nome'] = disci.text
    departamentos.append(data)

api = json.dumps(departamentos, indent=4)

print(api)

options = {
    'ano_semestre': '20191',
    'departamento': 'd-98'
}

data = parse_html('https://app.uff.br/graduacao/quadrodehorarios/?utf8=✓&page=0&q[anosemestre_eq]={ano_semestre}&q[disciplina_cod_departamento_eq]={departamento}', **options)
table = data.find('tbody')

keys = ['codigo', 'nome', 'turma', 'modulo', 'segunda', 'terca', 'quarta', 'quinta', 'sexta']

disciplinas = []

for row in table.find_all('tr'):
    data = dict.fromkeys(keys)
    for index, column in zip(range(9), row.find_all('td')):
        data[keys[index]] = column.text.strip('\n')
    disciplinas.append(data)

api = json.dumps(disciplinas, indent=4)

print(api)
