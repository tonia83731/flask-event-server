## Environment Setup

Current PYTHON version 3.12.2:
`python --version`

- **Clone project from github/gitlab**

```
git clone <repo-url>
cd <repo-folder>
```

- **Create a virtual environment**

```
python -m venv .env
```

- **Activate the virtual environment**

```
(Windows) .env/Scripts/Activate.ps1
(Mac/Linux) source venv/bin/activate
```

- **Installed required packages**

```
pip install -r requirements.txt
```

- **Checked packages in the environment**

```
python -m pip freeze
```

- **Set environment variables in `.env/` based on `.env.example`**

  - for **development**:

  ```
  .env.dev
  ```

  - for **production**:

  ```
  .env.prod
  ```

- **Set Flask environment variables**

```
(Windows PowerShell)
$env:FLASK_APP = "app:create_app"
$env:FLASK_ENV = "development"
```

```
(Mac/Linux)
export FLASK_APP="app:create_app"
export FLASK_ENV="development"
```

- **To verify the environment variables are set, run (optional)**:

```
(Windows) echo $env:FLASK_APP
(Mac/Linux) export $FLASK_APP
```

- **Run flask APP**

```
flask run
```
