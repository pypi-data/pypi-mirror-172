# Comitê de Bacias do Alto Tietê

- [GitHub](https://github.com/open-geodata/sp_bh_at)
- [PyPi](https://pypi.org/project/sp-bh-at)

<br>

O [**Comitê de Bacias do Alto Tietê**](https://comiteat.sp.gov.br) disponibiliza alguns _shapefiles_ relevantes.

Cheguei ao [_site_](https://comiteat.sp.gov.br/a-bacia/shapefiles/) após ler, na Lei Estadual nº 16.568, de 10.11.2017 (que criou a APRM Alto Cotia), que o Comitê seria o gestor de informações georreferenciadas.

> Artigo 16 - Fica criado o Sistema Gerencial de Informações - SGI da APRM-AC, **vinculado à gestão da UGRHI 6**, com as seguintes atribuições:<br>
>
> 1. permitir a caracterização e avaliação da qualidade ambiental da APRM-AC;<br>
> 2. subsidiar as decisões decorrentes das disposições desta lei, constituindo referência para a implementação de todos os instrumentos de planejamento e gestão da APRM-AC;<br>
> 3. disponibilizar a todos os agentes públicos e privados os dados e informações gerados.

<br>

A **UGRHI 6 (Alto Tietê)** corresponde à área drenada pelo rio Tietê desde suas nascentes em Salesópolis, até a barragem de Rasgão, integrada por 34 municípios. O território abrangido por essa UGRHI ocupa grande parte do território da RMSP.

<br>

A partir dai, fui obter os dados e, com o _script_ elaborado, foi possível obter todos os dados disponíveis, trata-los e divulga-los

<br>

No site do Comitê do Alto Tietê é informado que

> **_Arquivos gerados no Plano da Bacia Hidrográfica do Alto Tietê (2018)_**

<br>

---

### Como Usar?

O repositório faz parte do projeto [**_OpenGeodata_**](https://pypi.org/project/open-geodata), que tem por objetivo compartilhar dados espaciais por meio de _packages_ do python.

```bash
# Install
pip3 install open-geodata --upgrade
pip3 install sp-bh-at --upgrade
```

<br>

Uma vez instalado os pacotes, é possível listar e carregar os _datasets_ disponíveis, com os comandos abaixo.

```python
# List Datasets from package (dataframes and geodataframes)
geo.get_dataset_from_package('sp_bh_at')

# Load Dataset from package
geo.load_dataset_from_package('sp_bh_at', dataset_name)
```

<br>

---

### _TODO_

1. ~~Fazer _download_ dos dados~~
2. Ajustar as tabelas de atributos!
