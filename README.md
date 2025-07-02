# 🔍Undircover

<div align=center>
  <br>
  <a href="https://github.com/farrelega/Undircover" target="_blank"><img src="images/logo.png"/></a>
  <br>

*Scan any domain and find hidden directories!*
  
  [![Python](https://img.shields.io/badge/Python-3.10.6-blue.svg)](https://www.python.org/)
  [![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

</div>

## ⚙️Installation
### Requirements
- Python 3.8+
- Pip (package manager)
### Steps
1. **Clone Repository**
```bash
https://github.com/farrelega/Undircover.git
```
2. **Setup Virtual Environment (Recommended)**
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```
3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

## 🕹️Usage
### Parameter Options
| Parameters | Description | Default |
| - | - | - |
| `-t` | Target domain (required) | - |
| `-w` | Path to wordlist | - |
| `-p` | Protocol (http/https) | `https` |
| `-to` | Timeout (in sec) | `15` |
| `-m` | Scan mode (subdomain/path) | `subdomain` |

### Example Using
1. **Subdomain Scan**
```bash
python undircover.py -t example.com -w wordlists.txt -p https -to 10
```
2. **Path Scan**
```bash
python undircover.py -t example.com -m path
```
<div>
  <br>
    <a><img src="images/example.png"/></a>
  <br>
</div>

## License

MIT © Undircover<br/>
Original Creator - [Farrel Ega](https://github.com/farrelega)
