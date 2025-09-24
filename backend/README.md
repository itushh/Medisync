### Guide to fork

visit <a href="https://github.com/itushh/Medisync">repository</a>, click fork.

```
git clone https://github.com/<your_github_username>/Medisync.git
```

```
cd Medisync
```

```
cd backend
```

```
python -m venv xenv
```

```
xenv\Scripts\Activate
```

```
pip install -r requirements.txt
```

```
uvicorn app.main:app --reload
```