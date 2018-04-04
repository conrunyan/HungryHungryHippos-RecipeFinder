find . -path "*/migrations/*.py" -not -name "__init__.py" -not -path "*_pyenv3/*" -delete
find . -path "*/migrations/*.pyc" -not -path "*_pyenv3/*" -delete
