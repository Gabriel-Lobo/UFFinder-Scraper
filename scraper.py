import json
import requests
from bs4 import BeautifulSoup
from functions import print_progress


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

log = open('log.txt', 'a')

for i, item in enumerate(dept_option):
    page = 0
    html = parse_html('https://app.uff.br/graduacao/quadrodehorarios/?utf8=✓&page={page}&q[anosemestre_eq]={ano_semestre}&q[disciplina_cod_departamento_eq]={departamento}',
                      page=page, ano_semestre='20191', departamento=item.get('value'))
    table = html.find('tbody')

    if table:
        dept = dict.fromkeys(dept_kws)
        dept['codigo'] = item.get('value')
        dept['nome'] = item.text

        lects = []

        while table:
            for row in table.find_all('tr'):
                lect = dict.fromkeys(lect_kws)
                for index, column in zip(range(9), row.find_all('td')):
                    lect[lect_kws[index]] = column.text.strip('\n')
                lects.append(lect)

            log.write(dept['nome'] + ' - ' + 'page ' + str(page) + '\n')

            page += 1
            html = parse_html(
                'https://app.uff.br/graduacao/quadrodehorarios/?utf8=✓&page={page}&q[anosemestre_eq]={ano_semestre}&q[disciplina_cod_departamento_eq]={departamento}',
                page=page, ano_semestre='20191', departamento=item.get('value'))
            table = html.find('tbody')

        dept['disciplinas'] = lects

        depts.append(dept)
    else:
        continue

    print_progress(i, len(dept_option))

log.close()

api = json.dumps(depts, indent=4)

file = open('uff_api.json', 'w')
file.write(api)
file.close()
