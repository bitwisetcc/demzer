# DEMZER backend

## Run it on your machine

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
