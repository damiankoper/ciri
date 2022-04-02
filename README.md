# Ciri - General purpose virtial assistant

This project uses:
* Nx - monorepo management tool
* pipenv - python3 venv and dependency management tool
* Rasa - NLU toolkit for intent detection and action handling
* Vue3 + ElementPlus - frontend SPA

To setup and run project follow the following steps.

### Install dependencies and nx globally
```sh
pipenv install --skip-lock
python -m spacy download en_core_web_sm

npm install
npm install -g nx
```

### Train Rasa NLU model
```sh
nx run core:train
```

### Run Rasa server
```sh
nx run core:serve
```

### Run Rasa action server
```sh
nx run core:actions
```

### Serve frontend
```sh
nx run web:serve
```
