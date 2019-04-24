import json
import requests
from bs4 import BeautifulSoup

def parse_html(url, **kwargs):
    if len(kwargs) > 0:
        url = url.format(**kwargs)

    response = requests.get(url)
    html = response.content
    html = BeautifulSoup(html, features="html.parser")

    return html

html = parse_html('https://app.uff.br/graduacao/quadrodehorarios/')
dept_select = html.find('select', {'id': 'iddepartamento_coordenacao'})
dept_option = dept_select.find_all('option')

dept_kws = ['codigo', 'nome', 'disciplinas']
depts = []

lect_kws = ['codigo', 'nome', 'turma', 'modulo', 'segunda', 'terca', 'quarta', 'quinta', 'sexta']

for item in dept_option:
    html = parse_html('https://app.uff.br/graduacao/quadrodehorarios/?utf8=✓&page=0&q[anosemestre_eq]={ano_semestre}&q[disciplina_cod_departamento_eq]={departamento}',
                      ano_semestre = '20191', departamento = item.get('value'))
    table = html.find('tbody')

    if not table:
        continue

    dept = dict.fromkeys(dept_kws)
    dept['codigo'] = item.get('value')
    dept['nome'] = item.text

    lects = []

    for row in table.find_all('tr'):
        lect = dict.fromkeys(lect_kws)
        for index, column in zip(range(9), row.find_all('td')):
            lect[lect_kws[index]] = column.text.strip('\n')
        lects.append(lect)

    dept['disciplinas'] = lects

    depts.append(dept)

api = json.dumps(depts, indent=4)

file = open('uff_api.json', 'w')
file.write(api)
file.close()
