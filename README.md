<p align="center">
  <img src="https://github.com/dolevf/Open-Policy-Agent-Alfred/blob/main/static/images/logo.png?raw=true" width="300px" alt="Alfred"/>
</p>

# Open-Policy-Agent-Alfred
Reasonably usable self-hosted version of OPA's Playground

# About
Ever wanted to have your own version of [OPA's Playground](https://play.openpolicyagent.org)? Now it's possible!

# Features
- Syntax Highlighting
- Coverage Highlighting
- Data / Input / Policy Editor
- Download Policy as File / Copy to Clipboard

# Screenshot
<p align="center">
  <img src="https://github.com/dolevf/Open-Policy-Agent-Alfred/blob/main/static/images/alfred_view.png?raw=true" width="300px" alt="Alfred"/>
</p>

# How to Install and Use
Clone repository
`git clone https://github.com/dolevf/Open-Policy-Agent-Alfred`
`cd Open-Policy-Agent-Alfred`

## Dockerfile
### Build Docker Image
`docker build -t alfred .`

### Run Alfred Docker
`docker run -d -p 5000:5000 alfred`

## Bare Metal
### Install requirements

`pip3 install -r requirements.txt`

### Run Alfred
`python3 alfred.py`


# Open Alfred
[http://localhost:5000](http://localhost:5000)
