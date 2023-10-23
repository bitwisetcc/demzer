# DEMZER - um sistema acadêmico geral

## Como rodar o programa

Copie o arquivo `.env` do Discord, no canal de recursos para a raiz do projeto.
No terminal, execute `npm i` e `pip install -r requirements.txt`.
Ainda no terminal rode `az login` e depois `npm run watch`. Abra outro terminal e rode `python manage.py runserver`.

No seu navegador, visite `http://localhost:8000` e comece a testar o app!

![diagrama conceitual da base de dados](assets/db-diagram.png)

![tela de login](assets/login-screenshot.png)

## Criando um usuário admin

O site possui uma área secreta em `/secret`, onde são criadas as contas de administradores. Ao finalizar o formulário, será necessária uma chave de segurança, que é definida em `settings.py` em `SECURITY_KEY`.

---

Uma **última dica** é que, quando você abrir o projeto no VSCode, deverá aparecer uma mensagem no canto da tela, sugerindo extensões para o editor. Essas extensões forçam um estilo de código unificado no projeto e agilizam a sua produtividade usando algumas das tecnologias instaladas.

## Tutoriais externos

- Adicionando views no Django: [https://docs.djangoproject.com/en/4.2/intro/tutorial01](https://docs.djangoproject.com/en/4.2/intro/tutorial01/#write-your-first-view)
- Usando templates no Django: [https://docs.djangoproject.com/en/4.2/ref/templates/language](https://docs.djangoproject.com/en/4.2/ref/templates/language/)
- Introdução ao TailwindCSS: [https://tailwindcss.com/docs/utility-first](https://tailwindcss.com/docs/utility-first)
- Introdução ao Alpine.js: [https://alpinejs.dev/start-here](https://alpinejs.dev/start-here)
- Usando Git e GitHub no VSCode: [https://code.visualstudio.com/docs/sourcecontrol/intro-to-git](https://code.visualstudio.com/docs/sourcecontrol/intro-to-git)
