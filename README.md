# Workspace

O projeto Workspace é dividido em duas partes: uma **página web** e uma **aplicação desktop**.

```
Workspace/
├── web_page/       # Projeto da página web
│   └── app.py      # Código principal do site
└── desktop_app/    # Projeto do software desktop
    └── main.py     # Código principal do software
```

---

## Pré-requisitos

- Python 3.x
- MySQL Server 8.0
- Bibliotecas listadas em `requirements.txt`

---

## 1. Configurar o banco de dados (MySQL)

Abra o **Prompt de Comando** e conecte-se ao MySQL:

```bash
"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" -u root -p
```

Digite sua senha e execute o schema:

```sql
SOURCE schema.sql;
```

Em seguida, abra o arquivo `.env` na raiz do projeto e preencha as variáveis:

```env
HOST=localhost
USER=root
PASSWORD=sua_senha
DB_NAME=workspace_db
```

---

## 2. Instalar dependências

Na pasta raiz do projeto (`Workspace/`), execute:

```bash
pip install -r requirements.txt
```

---

## 3. Executar o projeto

**Página web**

```bash
cd web_page
python app.py
```

Acesse no navegador: [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

---

**Aplicação desktop**

```bash
cd desktop_app
python main.py
```
