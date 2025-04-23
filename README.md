# 🐍 Capyba API RESTful

API RESTful desenvolvida em Flask para o desafio técnico da Capyba.  
Gerencia pessoas, autenticação, confirmação de e-mail e muito mais.

---

## 🚀 Tecnologias utilizadas

- Python 3.10+
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Flask-JWT-Extended
- Flask-Marshmallow
- Passlib (bcrypt)
- SQLite (padrão local)
- Postman (para testes)

---

## ⚙️ Instalação do projeto

### 🔹 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/capyba-api.git
cd capyba-api
```

### 🔹 2. Crie um ambiente virtual

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

### 🔹 3. Instale as dependências

```bash
pip install -r requirements.txt
```

---

## 🛠️ Configuração do banco de dados

### 🔹 4. Inicialize as migrações e o banco de dados

```bash
flask db init         # apenas na primeira vez
flask db migrate -m "Criação inicial"
flask db upgrade
```
Após executar as migrações será gerado um arquivo .db na pasta instance, onde voçê pode consultar a persintência dos dados no banco de dados
---

## ▶️ Executando o projeto

```bash
flask run
```

A aplicação estará disponível em:  
👉 `http://127.0.0.1:5000`

---

## 🔐 Autenticação

Utilize o endpoint `/auth/login` para obter um token JWT.  
Adicione o token como `Bearer` no header `Authorization` para acessar rotas protegidas.

---

## 📬 Confirmação de e-mail

### Enviar token:
```http
POST /email/enviar-token
Body: { "email": "exemplo@email.com" }
```

### Validar token:
```http
POST /email/validar-token
Body: { "email": "exemplo@email.com", "token": "123456" }
```

---

## 📮 Testes com Postman

Você pode importar a [coleção Postman disponível aqui](https://drive.google.com/file/d/1TCF_pU-LOefgPOg8xMadYPM4czxsZhFg/view?usp=sharing)  
Ela já inclui:
- Login e logout
- Pessoas (CRUD + paginação, filtros, ordenação)
- Verificação de e-mail

---

## 📌 Estrutura de pastas

```
capyba-api/
├── app/
│   ├── models/
│   ├── routes/
│   ├── schemas/
│   ├── utils/
│   └── database.py
├── instance/
├── migrations/
├── app.py
├── requirements.txt
├── README.md
```

---

## 📧 Contato

Desenvolvido por [Alexsander Araujo] para o desafio Capyba.  
LinkedIn: https://www.linkedin.com/in/alexsanderaraujo4/ 
Email: alexsanderthorne@gmail.com
