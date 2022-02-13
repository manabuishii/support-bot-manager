# support-bot-manager

## Setup

```
python3 -m venv venv
source venv/bin/activate
```
## Start

```
python3 app.py
```

- host: 0.0.0.0
- port: 5050

## Access

http://localhost:5000/

## Transition

```
dot -T png transition.dot -o transition.png
dot -T vsg transition.dot -o transition.svg
```

## Development

### lint

```
tox
```

or 

```console
flake8 app.py
pep8 app.py
black app.py --check --diff
autoflake --in-place --remove-all-unused-imports app.py
```