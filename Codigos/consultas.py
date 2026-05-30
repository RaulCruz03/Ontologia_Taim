"""
30 Consultas SPARQL — Ontologia Banhado do Taim
================================================
Categorias:
  [S] Simples           — consultas por classe (6)
  [M] Múltiplas relações — cruzamento de entidades (7)
  [F] Com filtros        — restrições por valor (8)
  [A] Agregação          — COUNT, GROUP BY (5)
  [C] Cenário relevante  — análises do domínio (4)

Execução:
  pip install rdflib
  python sparql_consultas.py
"""

from rdflib import Graph

# ── Carrega a ontologia povoada ──────────────────────────────
g = Graph()
g.parse("taim_povoado.owl", format="xml")
print(f"✅ Ontologia carregada — {len(g)} triplas\n")

# ── Prefixos comuns a todas as consultas ─────────────────────
PREFIXOS = """
PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl:  <http://www.w3.org/2002/07/owl#>
PREFIX xsd:  <http://www.w3.org/2001/XMLSchema#>
PREFIX ex:   <http://www.exemplo.org/taim#>
"""

SEP = "─" * 60

def nome(uri):
    """Extrai o nome local de uma URI."""
    return str(uri).split("#")[-1] if uri else "—"

def rodar(numero, categoria, descricao, sparql):
    """Executa e exibe uma consulta SPARQL."""
    print(f"\n{'═'*60}")
    print(f"  Consulta {numero:02d} [{categoria}]")
    print(f"  {descricao}")
    print(f"{'═'*60}")
    print(sparql.strip())
    print(SEP)
    try:
        resultados = list(g.query(PREFIXOS + sparql))
        if resultados:
            colunas = [str(v) for v in resultados[0].labels]
            # Cabeçalho
            print("  " + " | ".join(f"{c:<25}" for c in colunas))
            print("  " + "-" * (28 * len(colunas)))
            for linha in resultados[:10]:   # mostra até 10
                valores = [nome(v) for v in linha]
                print("  " + " | ".join(f"{v:<25}" for v in valores))
            if len(resultados) > 10:
                print(f"  ... e mais {len(resultados)-10} resultados")
            print(f"\n  → Total: {len(resultados)} resultado(s)")
        else:
            print("  → Nenhum resultado encontrado.")
    except Exception as e:
        print(f"  ⚠ Erro: {e}")


# ════════════════════════════════════════════════════════════
#  BLOCO 1 — CONSULTAS SIMPLES [S]
# ════════════════════════════════════════════════════════════

rodar(1, "S", "Liste todos os animais cadastrados com nome científico e popular","""
SELECT ?animal ?especie ?popular
WHERE {
  ?animal rdf:type ?tipo .
  ?tipo   rdfs:subClassOf* ex:Animal .
  ?animal ex:nomeEspecie ?especie .
  ?animal ex:nomePopular ?popular .
}
ORDER BY ?popular
""")

rodar(2, "S", "Liste todos os trechos da BR-471 com seus quilômetros","""
SELECT ?trecho ?kmInicial ?kmFinal
WHERE {
  ?trecho rdf:type ex:TrechoRodovia .
  ?trecho ex:kmInicial ?kmInicial .
  ?trecho ex:kmFinal   ?kmFinal .
}
ORDER BY ?kmInicial
""")

rodar(3, "S", "Liste todos os habitats cadastrados com nome e área","""
SELECT ?habitat ?nome ?area
WHERE {
  ?habitat rdf:type ?tipo .
  ?tipo    rdfs:subClassOf* ex:Habitat .
  ?habitat ex:nomeHabitat ?nome .
  ?habitat ex:areaHabitat ?area .
}
ORDER BY DESC(?area)
""")

rodar(4, "S", "Liste todas as condições climáticas com temperatura e pluviosidade","""
SELECT ?clima ?descricao ?temperatura ?pluviosidade
WHERE {
  ?clima rdf:type ?tipo .
  ?tipo  rdfs:subClassOf* ex:CondicaoClimatica .
  ?clima ex:descricaoClima ?descricao .
  ?clima ex:temperatura    ?temperatura .
  ?clima ex:pluviosidade   ?pluviosidade .
}
ORDER BY ?descricao
""")

rodar(5, "S", "Liste todos os fatores de risco e seus níveis","""
SELECT ?fator ?descricao ?nivel
WHERE {
  ?fator rdf:type ?tipo .
  ?tipo  rdfs:subClassOf* ex:FatorRisco .
  ?fator ex:descricaoRisco ?descricao .
  ?fator ex:nivelRisco     ?nivel .
}
ORDER BY DESC(?nivel)
""")

rodar(6, "S", "Liste todos os eventos de atropelamento com data e horário","""
SELECT ?evento ?data ?horario
WHERE {
  ?evento rdf:type ex:EventoAtropelamento .
  ?evento ex:dataEvento    ?data .
  ?evento ex:horarioEvento ?horario .
}
ORDER BY ?data ?horario
""")


# ════════════════════════════════════════════════════════════
#  BLOCO 2 — MÚLTIPLAS RELAÇÕES [M]
# ════════════════════════════════════════════════════════════

rodar(7, "M", "Animais envolvidos em eventos com o trecho onde ocorreram","""
SELECT ?popular ?trecho ?data
WHERE {
  ?evento  rdf:type          ex:EventoAtropelamento .
  ?evento  ex:envolveAnimal  ?animal .
  ?evento  ex:ocorreEm       ?trecho .
  ?evento  ex:dataEvento     ?data .
  ?animal  ex:nomePopular    ?popular .
}
ORDER BY ?popular
""")

rodar(8, "M", "Eventos com animal, trecho, clima e período do dia","""
SELECT ?evento ?popular ?trecho ?clima ?periodo
WHERE {
  ?evento  rdf:type          ex:EventoAtropelamento .
  ?evento  ex:envolveAnimal  ?animal .
  ?evento  ex:ocorreEm       ?trecho .
  ?evento  ex:ocorreSob      ?condicao .
  ?evento  ex:ocorreDurante  ?periodo .
  ?animal  ex:nomePopular    ?popular .
  ?condicao ex:descricaoClima ?clima .
}
""")

rodar(9, "M", "Trechos e os banhados próximos a eles","""
SELECT ?trecho ?kmInicial ?habitat ?nomeHabitat
WHERE {
  ?trecho  rdf:type         ex:TrechoRodovia .
  ?trecho  ex:kmInicial     ?kmInicial .
  ?trecho  ex:proximoA      ?habitat .
  ?habitat ex:nomeHabitat   ?nomeHabitat .
}
ORDER BY ?kmInicial
""")

rodar(10, "M", "Eventos fatais com o animal envolvido e o fator de risco","""
SELECT ?popular ?especie ?fatorDesc ?trecho
WHERE {
  ?evento  rdf:type           ex:EventoAtropelamento .
  ?evento  ex:envolveAnimal   ?animal .
  ?evento  ex:ocorreEm        ?trecho .
  ?evento  ex:possuiFatorRisco ?fator .
  ?evento  ex:resultadoFatal  "true"^^xsd:boolean .
  ?animal  ex:nomePopular     ?popular .
  ?animal  ex:nomeEspecie     ?especie .
  ?fator   ex:descricaoRisco  ?fatorDesc .
}
""")

rodar(11, "M", "Capivaras atropeladas em trechos próximos a banhados","""
SELECT ?evento ?trecho ?nomeHabitat ?data
WHERE {
  ?evento  rdf:type          ex:EventoAtropelamento .
  ?evento  ex:envolveAnimal  ?animal .
  ?evento  ex:ocorreEm       ?trecho .
  ?evento  ex:dataEvento     ?data .
  ?animal  rdf:type          ex:Capivara .
  ?trecho  ex:proximoA       ?habitat .
  ?habitat rdf:type          ex:Banhado .
  ?habitat ex:nomeHabitat    ?nomeHabitat .
}
ORDER BY ?data
""")

rodar(12, "M", "Animais atropelados sob chuva com o trecho e horário","""
SELECT ?popular ?trecho ?horario ?data
WHERE {
  ?evento   rdf:type          ex:EventoAtropelamento .
  ?evento   ex:envolveAnimal  ?animal .
  ?evento   ex:ocorreEm       ?trecho .
  ?evento   ex:ocorreSob      ?condicao .
  ?evento   ex:horarioEvento  ?horario .
  ?evento   ex:dataEvento     ?data .
  ?animal   ex:nomePopular    ?popular .
  ?condicao rdf:type          ex:Chuva .
}
ORDER BY ?data
""")

rodar(13, "M", "Eventos com todas as relações: animal, trecho, clima, período e fator de risco","""
SELECT ?popular ?trecho ?clima ?periodo ?fator
WHERE {
  ?evento  rdf:type            ex:EventoAtropelamento .
  ?evento  ex:envolveAnimal    ?animal .
  ?evento  ex:ocorreEm         ?trecho .
  ?evento  ex:ocorreSob        ?condicao .
  ?evento  ex:ocorreDurante    ?per .
  ?evento  ex:possuiFatorRisco ?fat .
  ?animal  ex:nomePopular      ?popular .
  ?condicao ex:descricaoClima  ?clima .
  ?fat     ex:descricaoRisco   ?fator .
  BIND(STRAFTER(STR(?per), \"#\") AS ?periodo)
}
""")


# ════════════════════════════════════════════════════════════
#  BLOCO 3 — COM FILTROS [F]
# ════════════════════════════════════════════════════════════

rodar(14, "F", "Eventos ocorridos no período noturno (horário entre 20h e 06h)","""
SELECT ?evento ?popular ?horario ?data
WHERE {
  ?evento rdf:type          ex:EventoAtropelamento .
  ?evento ex:envolveAnimal  ?animal .
  ?evento ex:horarioEvento  ?horario .
  ?evento ex:dataEvento     ?data .
  ?animal ex:nomePopular    ?popular .
  FILTER (
    xsd:integer(SUBSTR(?horario, 1, 2)) >= 20 ||
    xsd:integer(SUBSTR(?horario, 1, 2)) <= 5
  )
}
ORDER BY ?horario
""")

rodar(15, "F", "Eventos com chuva forte (pluviosidade acima de 50mm)","""
SELECT ?evento ?popular ?pluviosidade ?data
WHERE {
  ?evento   rdf:type          ex:EventoAtropelamento .
  ?evento   ex:envolveAnimal  ?animal .
  ?evento   ex:ocorreSob      ?condicao .
  ?evento   ex:dataEvento     ?data .
  ?animal   ex:nomePopular    ?popular .
  ?condicao ex:pluviosidade   ?pluviosidade .
  FILTER (?pluviosidade > 50)
}
ORDER BY DESC(?pluviosidade)
""")

rodar(16, "F", "Eventos fatais registrados após 2022","""
SELECT ?evento ?popular ?data ?horario
WHERE {
  ?evento rdf:type          ex:EventoAtropelamento .
  ?evento ex:envolveAnimal  ?animal .
  ?evento ex:resultadoFatal "true"^^xsd:boolean .
  ?evento ex:dataEvento     ?data .
  ?evento ex:horarioEvento  ?horario .
  ?animal ex:nomePopular    ?popular .
  FILTER (?data > "2022-01-01")
}
ORDER BY DESC(?data)
""")

rodar(17, "F", "Eventos em trechos entre os km 307 e km 325","""
SELECT ?evento ?popular ?kmInicial ?kmFinal ?data
WHERE {
  ?evento rdf:type          ex:EventoAtropelamento .
  ?evento ex:envolveAnimal  ?animal .
  ?evento ex:ocorreEm       ?trecho .
  ?evento ex:dataEvento     ?data .
  ?animal ex:nomePopular    ?popular .
  ?trecho ex:kmInicial      ?kmInicial .
  ?trecho ex:kmFinal        ?kmFinal .
  FILTER (?kmInicial >= 307 && ?kmFinal <= 325)
}
ORDER BY ?kmInicial
""")

rodar(18, "F", "Eventos com temperatura abaixo de 15°C","""
SELECT ?evento ?popular ?temperatura ?data
WHERE {
  ?evento   rdf:type          ex:EventoAtropelamento .
  ?evento   ex:envolveAnimal  ?animal .
  ?evento   ex:ocorreSob      ?condicao .
  ?evento   ex:dataEvento     ?data .
  ?animal   ex:nomePopular    ?popular .
  ?condicao ex:temperatura    ?temperatura .
  FILTER (?temperatura < 15)
}
ORDER BY ?temperatura
""")

rodar(19, "F", "Animais com nome científico contendo 'Ardea' (garças)","""
SELECT ?animal ?especie ?popular
WHERE {
  ?animal rdf:type ?tipo .
  ?tipo   rdfs:subClassOf* ex:Animal .
  ?animal ex:nomeEspecie ?especie .
  ?animal ex:nomePopular ?popular .
  FILTER (CONTAINS(LCASE(?especie), "ardea"))
}
""")

rodar(20, "F", "Eventos ocorridos no período crepuscular (5h às 8h)","""
SELECT ?evento ?popular ?horario ?data
WHERE {
  ?evento rdf:type          ex:EventoAtropelamento .
  ?evento ex:envolveAnimal  ?animal .
  ?evento ex:horarioEvento  ?horario .
  ?evento ex:dataEvento     ?data .
  ?animal ex:nomePopular    ?popular .
  FILTER (
    xsd:integer(SUBSTR(?horario, 1, 2)) >= 5 &&
    xsd:integer(SUBSTR(?horario, 1, 2)) <= 8
  )
}
ORDER BY ?horario
""")

rodar(21, "F", "Eventos envolvendo mamíferos em habitats com área maior que 5000 hectares","""
SELECT ?popular ?especie ?nomeHabitat ?area
WHERE {
  ?evento  rdf:type          ex:EventoAtropelamento .
  ?evento  ex:envolveAnimal  ?animal .
  ?evento  ex:ocorreEm       ?trecho .
  ?animal  rdf:type          ?tipo .
  ?tipo    rdfs:subClassOf*  ex:Mamifero .
  ?animal  ex:nomePopular    ?popular .
  ?animal  ex:nomeEspecie    ?especie .
  ?trecho  ex:proximoA       ?habitat .
  ?habitat ex:nomeHabitat    ?nomeHabitat .
  ?habitat ex:areaHabitat    ?area .
  FILTER (?area > 5000)
}
""")


# ════════════════════════════════════════════════════════════
#  BLOCO 4 — AGREGAÇÃO [A]
# ════════════════════════════════════════════════════════════

rodar(22, "A", "Contagem de atropelamentos por nome popular da espécie","""
SELECT ?popular (COUNT(?evento) AS ?total)
WHERE {
  ?evento rdf:type          ex:EventoAtropelamento .
  ?evento ex:envolveAnimal  ?animal .
  ?animal ex:nomePopular    ?popular .
}
GROUP BY ?popular
ORDER BY DESC(?total)
""")

rodar(23, "A", "Contagem de eventos por trecho da rodovia","""
SELECT ?trecho ?kmInicial (COUNT(?evento) AS ?total)
WHERE {
  ?evento rdf:type      ex:EventoAtropelamento .
  ?evento ex:ocorreEm  ?trecho .
  ?trecho ex:kmInicial ?kmInicial .
}
GROUP BY ?trecho ?kmInicial
ORDER BY DESC(?total)
""")

rodar(24, "A", "Contagem de eventos por condição climática","""
SELECT ?descricao (COUNT(?evento) AS ?total)
WHERE {
  ?evento   rdf:type           ex:EventoAtropelamento .
  ?evento   ex:ocorreSob       ?condicao .
  ?condicao ex:descricaoClima  ?descricao .
}
GROUP BY ?descricao
ORDER BY DESC(?total)
""")

rodar(25, "A", "Proporção de eventos fatais vs. não fatais","""
SELECT ?fatal (COUNT(?evento) AS ?total)
WHERE {
  ?evento rdf:type          ex:EventoAtropelamento .
  ?evento ex:resultadoFatal ?fatal .
}
GROUP BY ?fatal
ORDER BY DESC(?total)
""")

rodar(26, "A", "Média de temperatura nas condições climáticas dos eventos","""
SELECT (AVG(?temperatura) AS ?tempMedia) (MIN(?temperatura) AS ?tempMin) (MAX(?temperatura) AS ?tempMax)
WHERE {
  ?evento   rdf:type        ex:EventoAtropelamento .
  ?evento   ex:ocorreSob    ?condicao .
  ?condicao ex:temperatura  ?temperatura .
}
""")


# ════════════════════════════════════════════════════════════
#  BLOCO 5 — CENÁRIOS RELEVANTES [C]
# ════════════════════════════════════════════════════════════

rodar(27, "C", "CENÁRIO — Trechos de maior risco: próximos a banhado com fator de risco nível 4 ou 5","""
SELECT ?trecho ?kmInicial ?nomeHabitat ?fatorDesc ?nivel
WHERE {
  ?evento  rdf:type            ex:EventoAtropelamento .
  ?evento  ex:ocorreEm         ?trecho .
  ?evento  ex:possuiFatorRisco ?fator .
  ?trecho  ex:kmInicial        ?kmInicial .
  ?trecho  ex:proximoA         ?habitat .
  ?habitat rdf:type            ex:Banhado .
  ?habitat ex:nomeHabitat      ?nomeHabitat .
  ?fator   ex:descricaoRisco   ?fatorDesc .
  ?fator   ex:nivelRisco       ?nivel .
  FILTER (?nivel >= 4)
}
ORDER BY DESC(?nivel) ?kmInicial
""")

rodar(28, "C", "CENÁRIO — Espécies mais vulneráveis: ranking por número de atropelamentos fatais","""
SELECT ?popular ?especie (COUNT(?evento) AS ?atropelamentosFatais)
WHERE {
  ?evento rdf:type          ex:EventoAtropelamento .
  ?evento ex:envolveAnimal  ?animal .
  ?evento ex:resultadoFatal "true"^^xsd:boolean .
  ?animal ex:nomePopular    ?popular .
  ?animal ex:nomeEspecie    ?especie .
}
GROUP BY ?popular ?especie
ORDER BY DESC(?atropelamentosFatais)
""")

rodar(29, "C", "CENÁRIO — Correlação chuva e atropelamento de mamíferos à noite","""
SELECT ?popular ?pluviosidade ?horario ?nomeHabitat ?data
WHERE {
  ?evento   rdf:type          ex:EventoAtropelamento .
  ?evento   ex:envolveAnimal  ?animal .
  ?evento   ex:ocorreSob      ?condicao .
  ?evento   ex:ocorreEm       ?trecho .
  ?evento   ex:horarioEvento  ?horario .
  ?evento   ex:dataEvento     ?data .
  ?animal   rdf:type          ?tipo .
  ?tipo     rdfs:subClassOf*  ex:Mamifero .
  ?animal   ex:nomePopular    ?popular .
  ?condicao rdf:type          ex:Chuva .
  ?condicao ex:pluviosidade   ?pluviosidade .
  ?trecho   ex:proximoA       ?habitat .
  ?habitat  ex:nomeHabitat    ?nomeHabitat .
  FILTER (
    xsd:integer(SUBSTR(?horario, 1, 2)) >= 20 ||
    xsd:integer(SUBSTR(?horario, 1, 2)) <= 5
  )
}
ORDER BY DESC(?pluviosidade)
""")

rodar(30, "C", "CENÁRIO — Diagnóstico completo: trecho, espécie, clima, período e fatalidade para apoio à decisão","""
SELECT ?kmInicial ?popular ?clima ?periodo ?fatal (COUNT(?evento) AS ?ocorrencias)
WHERE {
  ?evento   rdf:type            ex:EventoAtropelamento .
  ?evento   ex:envolveAnimal    ?animal .
  ?evento   ex:ocorreEm         ?trecho .
  ?evento   ex:ocorreSob        ?condicao .
  ?evento   ex:ocorreDurante    ?per .
  ?evento   ex:resultadoFatal   ?fatal .
  ?animal   ex:nomePopular      ?popular .
  ?trecho   ex:kmInicial        ?kmInicial .
  ?condicao ex:descricaoClima   ?clima .
  BIND(STRAFTER(STR(?per), \"#\") AS ?periodo)
}
GROUP BY ?kmInicial ?popular ?clima ?periodo ?fatal
ORDER BY DESC(?ocorrencias) ?kmInicial
""")

print(f"\n{'═'*60}")
print("  ✅ 30 consultas executadas com sucesso.")
print(f"{'═'*60}\n")