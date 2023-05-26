# DEMZER backend

## Instruções

Este projeto consiste em um servidor que pode ser gerido local ou remotamente. Para que funcione, precisará de algumas dependências:

- [Node JS 18.16](https://nodejs.org/pt-br) (LTS)
- [Python 3.11](https://www.python.org/)
- MySQL (opcional)

_No futuro o projeto usará uma ferramenta chamada Docker para rodar tudo independente da máquina base._

```sh
npm i
pip install -r requirements.txt
./manage.py makemigrations
./manage.py migrate

./manage.py runserver # run django
npm run watch # watch JS and CSS files
```

Set the `DB_ENGINE` evironment variable as `mysql` or `sqlite3`. Though, if you're pushing to production, set all other environment variables required in settings.py. And if you're using MySQL, remember to install a package called `python-mysql-connector`. It is essential for django to connect to MySQL databases.

## TO-DO

- `__str__()` methods on models.
- `ordering` property on methods
- Add `Class` date and order
- Download or import fonts
- Add auto reload on dvelopment mode
- Create a docker image
- Add prettier and editorconfig files
- Be able to fill in residence from CEP
