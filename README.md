# support-bot-manager

## Setup

```python
python3 -m venv venv
source venv/bin/activate
```

## Start

```console
mkdir db
```

```console
python3 app.py
```

- host: 0.0.0.0
- port: 5050

## Access

http://localhost:5000/

## via Apache for user login

### Create new htpasswd

```console
htpasswd -b -c apache/htpasswd USERNAME PASSWORD
```

### Add User

```console
htpasswd -b apache/htpasswd NEWUSERNAME NEWPASSWORD
```

### exec Apache in Docker , app in localhost

Use `--add-host=host.docker.internal:host-gateway`
Ref: https://stackoverflow.com/a/43541681

```console
docker run --rm --add-host=host.docker.internal:host-gateway \
 -it --name my-apache-app -p 8080:80 \
 -v $PWD/apache/apache_docker_app_local_httpd.conf:/usr/local/apache2/conf/httpd.conf \
 -v $PWD/apache/htpasswd:/etc/httpd/htpasswd \
 -v $PWD/apache/public_html:/usr/local/apache2/htdocs/ \
 httpd:2.4.52
```

## Transition of web pages

```console
dot -T png transition.dot -o transition.png
dot -T vsg transition.dot -o transition.svg
```
