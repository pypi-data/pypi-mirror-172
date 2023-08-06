# bjcli

bjcli is a simple command line utility to run Bjoern WSGI server

## Features

- Forks
- Environment variables support

## Installation 
pip install bjcli

## Usage
bjcli -w 4 -i 127.0.0.1 -p 8088 app.wsgi:application

##### Using sockets

bjcli -w 4 -i unix:/path/to/socket app.wsgi:application

Examples above would import application from app.wsgi and pass it to Bjoern

| Argument | Description | Required | Default | Type |
| ------ | ------ | ------ | ------ | ------ |
| -w | Number of workers | False | 1 | int
| -i | Host | False | 127.0.0.1 | str
| -p | Port. If left blank and the host is an IP address, 8088 is assigned | False | None | None/int
| module:wsgi_app (first positional) | Module containing "wsgi_app" (module attr name after ":")| True | - | module

