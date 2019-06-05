import json
import requests
from bs4 import BeautifulSoup
from functions import print_progress


# This function receives an URL as parameter and return it's response, parsed as HTML.
# **kwargs can be passed as URL GET parameters.
def parse_html(url, **kwargs):
    if len(kwargs) > 0:
        url = url.format(**kwargs)

    response = requests.get(url)
    html = response.content
    html = BeautifulSoup(html, features="html.parser")

    return html

# Requests page "Quadro de Horários", get and stores departments, as a HTML "option" tag, into "dept_option" list.
html = parse_html('https://app.uff.br/graduacao/quadrodehorarios/')
dept_select = html.find('select', {'id': 'iddepartamento_coordenacao'})
dept_option = dept_select.find_all('option')

# List of keywords "dept_kws" for "dept" dictionary.
dept_kws = ['codigo', 'nome', 'disciplinas']
depts = []

# List of keywords "lect_kws" for "lect" dictionary.
lect_kws = ['codigo', 'nome', 'turma', 'modulo', 'segunda', 'terca', 'quarta', 'quinta', 'sexta']

# Open log file to keep track of the pages that were iterated with.
log = open('log.txt', 'a')

# Iterates through every department, as item, in the "dept_options" departments list.
for i, item in enumerate(dept_option):
    page = 0

    # Requests page "Quadro de Horários" with "page", "ano_semestre" and "departamento" as GET parameters and check if
    # the returned HTML has a table.
    html = parse_html('https://app.uff.br/graduacao/quadrodehorarios/?utf8=✓&page={page}&q[anosemestre_eq]={ano_semestre}&q[disciplina_cod_departamento_eq]={departamento}',
                      page=page, ano_semestre='20191', departamento=item.get('value'))
    table = html.find('tbody')

    if table:
        # (Re)declares "dept" dictionary and assigns "codigo" and "nome" values.
        dept = dict.fromkeys(dept_kws)
        dept['codigo'] = item.get('value')
        dept['nome'] = item.text

        # Empty list used to store lectures of the current department.
        lects = []

        # Keeps iterating through the same department while the requested page has a table.
        while table:

            # Iterates through every row of the table, (re)declaring "lect" dictionary in every iteration.
            for row in table.find_all('tr'):
                lect = dict.fromkeys(lect_kws)

                # For each row column, assign it's value to the next "lect" dictionary attribute.
                for index, column in zip(range(9), row.find_all('td')):
                    lect[lect_kws[index]] = column.text.strip('\n')
                # Append current "lect" dictionary to the current department list of lectures.
                lects.append(lect)

            # Save current department/page iterated into log file.
            log.write(dept['nome'] + ' - ' + 'page ' + str(page) + '\n')

            # Requests department next page of lectures.
            page += 1
            html = parse_html(
                'https://app.uff.br/graduacao/quadrodehorarios/?utf8=✓&page={page}&q[anosemestre_eq]={ano_semestre}&q[disciplina_cod_departamento_eq]={departamento}',
                page=page, ano_semestre='20191', departamento=item.get('value'))
            table = html.find('tbody')

        # Assign list of lectures to current department "disciplinas" attribute.
        dept['disciplinas'] = lects

        # Append current "dept" to list of departments.
        depts.append(dept)
    else:
        continue

    print_progress(i, len(dept_option))

# Close log file.
log.close()

# Creates pretty printed json file from "depts" list.
api = json.dumps(depts, indent=4)

file = open('uff_api.json', 'w')
file.write(api)
file.close()
