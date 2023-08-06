# Crypton Tool

Crypton Tool é baseado no pacote <a href="https://cryptography.io/" target="_blank">cryptography.io</a> e tem por objetivo disponibilizar métodos para cryptar arquivos e conteúdos, além de disponibilizar comandos CLI. 

**Documentação:** <a href="https://msbar.github.io/crypton-tool" target="_blank">https://msbar.github.io/crypton-tool</a>

**Source code:** <a href="https://github.com/msbar/crypton-tool" target="_blank">https://github.com/msbar/crypton-tool</a>

## Instalação:

```
pip install crypton-tool
```

## Exemplos:

### Criptando um arquivo ou arquivos em uma pasta.
```Python linenums="1"
from crypton_tool.crypton import Crypton

Crypton.generate_key(to_file='seu/caminho')
token = Crypton.read_token_file("seu/caminho/token.crypton")
```

### Criptando um arquivo ou arquivos em uma pasta.
```Python linenums="1"
crypt.encrypt_file('caminho/para/arquivo_ou_pasta')
```

### Decriptando um arquivo ou arquivos em uma pasta.
```Python linenums="1"
crypt.decrypt_file('caminho/para/arquivo_ou_pasta')
```