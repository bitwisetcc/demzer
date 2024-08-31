# DEMZER - um sistema acadêmico geral

## Abrindo o servidor localmente

Copie o arquivo `.env`, disponível nos canais de comunicação, para a raiz do projeto.

### Instale as dependências do projeto:

```sh
pip install -r requirements.txt
npm i
```

### Autentique os serviços de nuvem:

```sh
az login
```

### Inicie os servidores

```sh
npm run watch
python manage.py runserver
```

No seu navegador, visite `http://localhost:8000` e comece a testar.

> [!TIP]
> Ao abrir o projeto no VSCode, instale as extensões sugeridas pelo projeto. Isso ajuda a padronizar o estilo de código e agilizam a sua produtividade com as tecnologias utilizadas.

## Modelagem de dados

![diagrama conceitual da base de dados](assets/db-diagram.png)

## Tela de exemplo

![tela de login](assets/login-screenshot.png)

## Criando um usuário admin

O site possui uma área secreta em `/secret`, onde são criadas as contas de administradores. Ao finalizar o formulário, será necessária uma chave de segurança, que é definida em `settings.py` em `SECURITY_KEY`.

---

## Recursos externos

- Adicionando views no Django: [https://docs.djangoproject.com/en/4.2/intro/tutorial01](https://docs.djangoproject.com/en/4.2/intro/tutorial01/#write-your-first-view)
- Usando templates no Django: [https://docs.djangoproject.com/en/4.2/ref/templates/language](https://docs.djangoproject.com/en/4.2/ref/templates/language/)
- Introdução ao TailwindCSS: [https://tailwindcss.com/docs/utility-first](https://tailwindcss.com/docs/utility-first)
- Introdução ao Alpine.js: [https://alpinejs.dev/start-here](https://alpinejs.dev/start-here)
- Usando Git e GitHub no VSCode: [https://code.visualstudio.com/docs/sourcecontrol/intro-to-git](https://code.visualstudio.com/docs/sourcecontrol/intro-to-git)
