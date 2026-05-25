# 🦦 Ontologia do Banhado do Taim

> Trabalho da disciplina de **Inteligência Artificial** — Representação de Conhecimento via OWL  
> Universidade Federal de Santa Maria (UFSM)

---

## 📋 Descrição

Desenvolvimento de uma ontologia OWL para representar o domínio ecológico e operacional relacionado ao **Banhado do Taim (RS)**, com foco em eventos de atropelamento de fauna na região da BR-471.

A ontologia estrutura o conhecimento sobre espécies, habitats, condições ambientais e eventos de atropelamento, criando uma base consultável via SPARQL para análise de padrões e apoio à conservação ambiental.

---

## 🗂️ Estrutura do Repositório

```
.
├── ontologia/
│   ├── taim.owl                  # Arquivo principal da ontologia (OWL/RDF-XML)
│   └── taim_ontologia.py         # Script de definição das classes e propriedades
│
├── povoamento/
│   └── taim_povoamento.py        # Script de geração dos 100+ indivíduos
│
├── consultas/
│   └── sparql_consultas.py       # 30 consultas SPARQL com resultados
│
├── relatorio/
│   └── relatorio.pdf             # Relatório final em PDF
│
└── README.md
```

---

## 🧠 Estrutura da Ontologia

### Classes (43 no total)

| Classe raiz | Subclasses |
|---|---|
| `Animal` | `Mamifero`, `Ave`, `Reptil` → `Capivara`, `Lontra`, `Tatu`, `Veado`, `AveAquatica`, `AveTerrestre`, `Serpente`, `Tartaruga` |
| `Habitat` | `Banhado`, `CorpoDagua`, `VegetacaoRiparia`, `CampoAlagado` → `Lagoa`, `Rio`, `Vala` |
| `Infraestrutura` | `Rodovia`, `TrechoRodovia`, `Ponte`, `Acostamento` |
| `EventoAtropelamento` | — |
| `CondicaoAmbiental` | `CondicaoClimatica`, `NivelLuminosidade` → `Chuva`, `Neblina`, `CeuAberto`, `Diurno`, `Noturno`, `Crepuscular` |
| `FatorRisco` | `TrafegoVeicular`, `VisibilidadeReduzida`, `ProximidadeCorpoHidrico`, `AusenciaDePassagem` |
| `PeriodoTemporal` | `Estacao`, `Horario` |

### Propriedades de Objeto (12)

| Propriedade | Domínio → Alcance | Tipo |
|---|---|---|
| `envolveAnimal` | EventoAtropelamento → Animal | — |
| `ocorreEm` | EventoAtropelamento → TrechoRodovia | — |
| `ocorreSob` | EventoAtropelamento → CondicaoAmbiental | — |
| `ocorreDurante` | EventoAtropelamento → PeriodoTemporal | **Temporal** |
| `proximoA` | TrechoRodovia → Habitat | **Espacial** |
| `pertenceARodovia` | TrechoRodovia → Rodovia | — |
| `viveEm` | Animal → Habitat | — |
| `atravessaRodovia` | Animal → Rodovia | — |
| `possuiFatorRisco` | EventoAtropelamento → FatorRisco | — |
| `contem` | Habitat → Animal | — |
| `afetaVisibilidade` | CondicaoClimatica → VisibilidadeReduzida | — |
| `aumentaRisco` | CondicaoAmbiental → FatorRisco | — |

### Propriedades de Dados (17)

Incluem: `nomeEspecie`, `nomePopular`, `kmInicial`, `kmFinal`, `coordenadaLat`, `coordenadaLon`, `nomeRodovia`, `dataEvento`, `horarioEvento`, `resultadoFatal`, `descricaoClima`, `temperatura`, `pluviosidade`, `nomeHabitat`, `areaHabitat`, `nivelRisco`, `descricaoRisco`

---

## ⚙️ Requisitos

```bash
Python 3.8+
owlready2
rdflib
```

Instalar dependências:

```bash
pip install owlready2 rdflib
```

---

## 🚀 Como Executar

**1. Gerar a ontologia (classes e propriedades):**
```bash
python ontologia/taim_ontologia.py
```
Gera o arquivo `taim.owl`.

**2. Povoar com indivíduos:**
```bash
python povoamento/taim_povoamento.py
```
Adiciona 100+ indivíduos à ontologia.

**3. Executar as consultas SPARQL:**
```bash
python consultas/sparql_consultas.py
```

**4. Visualizar no Protégé:**  
Abra o arquivo `taim.owl` no [Protégé](https://protege.stanford.edu/) para visualização gráfica da ontologia.

---

## 🔍 Exemplo de Consulta SPARQL

Atropelamentos de capivara em trechos próximos a banhados, sob chuva:

```sparql
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX ex:  <http://www.exemplo.org/taim#>

SELECT ?evento ?trecho ?data
WHERE {
  ?evento  rdf:type        ex:EventoAtropelamento .
  ?evento  ex:envolveAnimal ?animal .
  ?evento  ex:ocorreEm     ?trecho .
  ?evento  ex:ocorreSob    ?condicao .
  ?evento  ex:dataEvento   ?data .
  ?animal  rdf:type        ex:Capivara .
  ?condicao rdf:type       ex:Chuva .
  ?trecho  ex:proximoA     ?habitat .
  ?habitat rdf:type        ex:Banhado .
}
ORDER BY ?data
```

---

## 🌿 Contexto

O **Banhado do Taim** é uma das principais áreas úmidas do Rio Grande do Sul, com rica biodiversidade e papel essencial na preservação de ecossistemas. A BR-471, que corta a região, representa um vetor significativo de atropelamentos de fauna silvestre.

Esta ontologia visa organizar e integrar informações dispersas sobre esses eventos, criando uma base de conhecimento estruturada e consultável que pode apoiar futuros sistemas de monitoramento e conservação ambiental.

---

## 👤 Autoria

**Disciplina:** Inteligência Artificial  
**Aluno:** Raul Hohgraefe da Cruz  
**Instituição:** Universidade Federal de Santa Maria — UFSM  
**Ano:** 2026
