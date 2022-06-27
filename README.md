<p align="center">
  <img src="https://github.com/dolevf/Open-Policy-Agent-Alfred/blob/main/static/images/logo.png?raw=true" width="300px" alt="Alfred"/>
</p>

# Table of Contents
* [About](#about)
* [Features](#features)
* [Screenshot](#screenshot)
* [Install](#how-to-install)
  * [Installation - Docker](#docker)
  * [Installation - Docker Registry](#docker-registry)
  * [Installation - Server](#server)
* [Maintainers](#maintainers)
* [License](#license)

# OPA Alfred
Reasonably usable self-hosted version of OPA's Playground

# About
Ever wanted to have your own version of [OPA's Playground](https://play.openpolicyagent.org)? now it's possible with a reasonably usable version of the original Playground, called Alfred!

# Features
- Syntax Highlighting
- Policy Publishing
- Coverage Highlighting
- Data / Input / Policy Editor
- Restrict Execution of Builtins, such as: `http.send` or `opa.runtime`
- Download Policy as File / Copy to Clipboard

# Screenshot
<p align="center">
  <img src="https://github.com/dolevf/Open-Policy-Agent-Alfred/blob/main/static/images/alfred_view.png?raw=true" width="900px" alt="Alfred"/>
</p>

# Configuration
There is not a whole lot of configurations required for Alfred. If you want to restrict certain builtins from running in policies, you can do so in `config.py`:

```
RESTRICTED_BUILTINS = [
    'http.send',
    'opa.runtime'
]
```

By default, all builtins are allowed.

# How to Install
## Clone repository
`git clone https://github.com/dolevf/Open-Policy-Agent-Alfred`

`cd Open-Policy-Agent-Alfred`

## Docker
### Build Docker Image
`docker build -t alfred .`

### Run Alfred Container
`docker run -d -p 5000:5000 alfred`

## Docker Registry
### Pull Alfred from Registry
`docker pull dolevf/alfred`

### Run Alfred Container
`docker run -d -p 5000:5000 dolevf/alfred`

## Server
### Install requirements

`pip3 install -r requirements.txt`

`python3 setup.py`

### Download OPA binary
For Linux:

`curl -L -o bin/opa https://openpolicyagent.org/downloads/v0.41.0/opa_linux_amd64_static`

For MacOSX:

`curl -L -o bin/opa https://openpolicyagent.org/downloads/v0.41.0/opa_darwin_amd64`

### Set permissions
`chmod u+x bin/opa`

### Run Alfred
`python3 alfred.py`


# Open Alfred
[http://localhost:5000](http://localhost:5000)


# Maintainers
- Dolev Farhi

# License
It is distributed under the MIT License. See LICENSE for more information.
