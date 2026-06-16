# Workspace

The Workspace project is split into two parts: a **web page** and a **desktop application**.

```
Workspace/
├── web_page/       # Web page project
│   └── app.py      # Main web app entry point
└── desktop_app/    # Desktop software project
    └── main.py     # Main desktop app entry point
```

---

## Prerequisites

- Python 3.x
- MySQL Server 8.0
- Libraries listed in `requirements.txt`

---

## 1. Set up the database (MySQL)

Open the **Command Prompt** and connect to MySQL:

```bash
"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" -u root -p
```

Enter your password and run the schema:

```sql
SOURCE schema.sql;
```

Then open the `.env` file in the project root and fill in the variables:

```env
HOST=localhost
USER=root
PASSWORD=your_password
DB_NAME=workspace_db
```

---

## 2. Install dependencies

From the project root folder (`Workspace/`), run:

```bash
pip install -r requirements.txt
```

---

## 3. Run the project

**Web page**

```bash
cd web_page
python app.py
```

Open in your browser: [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

---

**Desktop application**

```bash
cd desktop_app
python main.py
```
