# support-bot-manager

## Setup

```console
python3 -m venv venv
source venv/bin/activate
```

## Start

### application

```console
python3 app.py
```

- host: 0.0.0.0
- port: 5050

### Apache reverse proxy

```console
htpasswd -b -c apache/htpasswd USERNAME PASSWORD
```

Add more user

```console
htpasswd -b apache/htpasswd USERNAME PASSWORD
```

#### start

```console
docker run --rm --add-host=host.docker.internal:host-gateway \
 -it --name my-apache-app -p 8080:80 \
 -v $PWD/httpd.conf:/usr/local/apache2/conf/httpd.conf \
 -v $PWD/htpasswd:/etc/httpd/htpasswd \
 -v $PWD/apache/public_html:/usr/local/apache2/htdocs/ \
 httpd:2.4.52
```

## Access

http://localhost:5000/

## Transition

```console
dot -T png transition.dot -o transition.png
dot -T vsg transition.dot -o transition.svg
```

## Development

### lint

```console
tox
```

or

```console
flake8 app.py
pep8 app.py
black app.py --check --diff
autoflake --in-place --remove-all-unused-imports app.py
```
