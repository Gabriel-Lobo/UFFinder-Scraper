import json
import requests
from bs4 import BeautifulSoup

options = {
    'ano_semestre': '20191',
    'departamento': 'd-98'
}

url = 'https://app.uff.br/graduacao/quadrodehorarios/?utf8=✓&page=0&q[anosemestre_eq]={ano_semestre}&q[disciplina_cod_departamento_eq]={departamento}'.format(**options)
response = requests.get(url)
html = response.content
soap = BeautifulSoup(html, features="html.parser")
table = soap.find('tbody')

keys = ['codigo', 'disciplina', 'turma', 'modulo', 'segunda', 'terca', 'quarta', 'quinta', 'sexta']

disciplinas = []

for row in table.find_all('tr'):
    data = dict.fromkeys(keys)
    for index, column in zip(range(9), row.find_all('td')):
        data[keys[index]] = column.text.strip('\n')
    disciplinas.append(data)

json = json.dumps(disciplinas, indent=4)

print(json)
