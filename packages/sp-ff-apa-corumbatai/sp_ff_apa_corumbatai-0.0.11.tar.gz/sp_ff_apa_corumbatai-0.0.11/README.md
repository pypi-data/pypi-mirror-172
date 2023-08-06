# APA Corumbataí

- [GitHub](https://github.com/open-geodata/sp_ff_apa-corumbatai)
- [PyPi](https://pypi.org/project/sp-ff-apa-corumbatai/)

<br>

A partir da base vetorial, fiz um mapa online, disponível [aqui](https://open-geodata.github.io/blog/apa-corumbata%C3%AD/), para facilitar o acesso. Os vetores são restritos ao perímetro Corumbataí.

<br>

---

### Como Usar?

O repositório faz parte do projeto [**_OpenGeodata_**](https://pypi.org/project/open-geodata), que tem por objetivo compartilhar dados espaciais por meio de _packages_ do python.

```bash
# Install
pip3 install open-geodata --upgrade
pip3 install sp-ff-apa-corumbatai --upgrade
```

<br>

Uma vez instalado os pacotes, é possível listar e carregar os _datasets_ disponíveis, com os comandos abaixo.

```python
# List Datasets from package (dataframes and geodataframes)
geo.get_dataset_from_package('sp_ff_apa_corumbatai')

# Load Dataset from package
geo.load_dataset_from_package('sp_ff_apa_corumbatai', dataset_name)
```

<br>

---

### _TODO_

1. Mudar foto da postagem para https://commons.wikimedia.org/wiki/File:Serra_do_Fazend%C3%A3o-01.jpg
