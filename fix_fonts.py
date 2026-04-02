with open('static/css/bootstrap-icons.min.css', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    'url("fonts/bootstrap-icons.woff2',
    'url("/static/fonts/bootstrap-icons.woff2'
).replace(
    'url("fonts/bootstrap-icons.woff',
    'url("/static/fonts/bootstrap-icons.woff'
)

with open('static/css/bootstrap-icons.min.css', 'w', encoding='utf-8') as f:
    f.write(content)

print('Chemin corrigé !')