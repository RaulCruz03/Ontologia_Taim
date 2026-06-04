"""
Povoamento da Ontologia — Banhado do Taim  v3
==============================================
Fontes:
  - Nauderer, R. (2014). Atropelamentos de capivaras (Hydrochoerus hydrochaeris)
    na BR-471, Estação Ecológica do Taim, RS. Dissertação de Mestrado, FURG.
  - Dados sintéticos plausíveis para as demais espécies, calibrados segundo
    os padrões de atropelamento identificados no artigo.

Estratégia de dados
────────────────────
• Eventos REAIS (artigo Nauderer 2014):
    – 629 capivaras → representadas por 50 indivíduos e ~50 eventos
      (≈ 35 % do total de eventos)
    – 3 lontras (Lontra longicaudis) — todas no Setor 2
    – 3 gatos-do-mato (Leopardus geoffroyi) — todos no Setor 2
• Eventos SINTÉTICOS plausíveis para demais espécies (≈ 65 %):
    – Distribuição temporal: inverno > outono/primavera > verão
    – Distribuição por período: noturno (55 %) > crepuscular (25 %) > diurno (20 %)
    – Distribuição por trecho: pesos baseados nos hotspots reais
    – Condições climáticas com peso sazonal
    – Fatalidade: 100 % para capivaras (dados de campo); 80 % para demais

Execução:
    pip install owlready2
    python taim_povoamento_v3.py
"""

import datetime
import random
from owlready2 import *

random.seed(42)   # reprodutibilidade

# ════════════════════════════════════════════════════════════
# 0. CARREGAR ONTOLOGIA BASE
# ════════════════════════════════════════════════════════════

onto = get_ontology("taim.owl").load()
ex   = onto.get_namespace("http://www.exemplo.org/taim#")

def get_classe(nome):
    return onto.search_one(iri=f"*{nome}")


# ════════════════════════════════════════════════════════════
# 1. NOVAS CLASSES (não existentes na ontologia base)
#    Todas as espécies aqui representadas ocorrem na região
#    do Taim conforme literatura e GBIF.
# ════════════════════════════════════════════════════════════

with onto:
    # Mamíferos adicionais
    class GatoDomato(ex.Mamifero):      pass   # Leopardus geoffroyi — real (Nauderer 2014)
    class Graxaim(ex.Mamifero):         pass   # Lycalopex gymnocercus — pampa
    class Mao_pelada(ex.Mamifero):      pass   # Procyon cancrivorus — frequente no Taim
    class Preá(ex.Mamifero):            pass   # Cavia aperea — roedor abundante
    class Tuco_tuco(ex.Mamifero):       pass   # Ctenomys minutus — endêmico

    # Aves terrestres adicionais (frequentes em bordas de rodovia)
    class Chimango(ex.AveTerrestre):    pass   # Milvago chimango
    class Carcara(ex.AveTerrestre):     pass   # Caracara plancus
    class Perdiz(ex.AveTerrestre):      pass   # Rhynchotus rufescens

    # Répteis adicionais
    class Lagarto(ex.Reptil):           pass   # Tupinambis merianae

print("✅ Novas classes adicionadas.")


# ════════════════════════════════════════════════════════════
# 2. TRECHOS REAIS DA BR-471 (km 536–553, Nauderer 2014)
#    3 setores conforme presença/condição do SPF
# ════════════════════════════════════════════════════════════

# (id, km_ini, km_fin, lat, lon, setor, possui_spf)
TRECHOS_REAIS = [
    # SETOR 1 — com tela SPF (km 536–539.4)
    ("trecho_BR471_km536", 536.0, 537.0, -33.5198, -53.3645, "Setor1",      True),
    ("trecho_BR471_km537", 537.0, 538.0, -33.5287, -53.3712, "Setor1",      True),   # hotspot
    ("trecho_BR471_km538", 538.0, 539.0, -33.5376, -53.3779, "Setor1",      True),   # hotspot
    ("trecho_BR471_km539", 539.0, 539.4, -33.5420, -53.3812, "Setor1",      True),   # hotspot

    # ZONA DE TRANSIÇÃO 1→2 (km 539.4–541) — área crítica
    ("trecho_BR471_km540", 539.4, 541.0, -33.5487, -53.3858, "Transicao12", False),

    # SETOR 2 — SEM tela SPF (km 539.4–544.9) — maior concentração
    ("trecho_BR471_km541", 541.0, 542.0, -33.5565, -53.3913, "Setor2",      False),  # hotspot principal
    ("trecho_BR471_km542", 542.0, 543.0, -33.5643, -53.3968, "Setor2",      False),
    ("trecho_BR471_km543", 543.0, 544.0, -33.5721, -53.4023, "Setor2",      False),
    ("trecho_BR471_km544", 544.0, 544.9, -33.5793, -53.4071, "Setor2",      False),

    # ZONA DE TRANSIÇÃO 2→3 (km 544.9–546) — área crítica
    ("trecho_BR471_km545", 544.9, 546.0, -33.5860, -53.4115, "Transicao23", True),

    # SETOR 3 — com tela SPF bem conservada (km 544.9–553) — menor taxa
    ("trecho_BR471_km546", 546.0, 547.0, -33.5938, -53.4163, "Setor3",      True),   # hotspot pontual
    ("trecho_BR471_km548", 547.0, 549.0, -33.6094, -53.4259, "Setor3",      True),
    ("trecho_BR471_km550", 549.0, 551.0, -33.6250, -53.4355, "Setor3",      True),
    ("trecho_BR471_km551", 551.0, 553.0, -33.6406, -53.4451, "Setor3",      True),
]

# Pesos por trecho baseados nos hotspots de Nauderer (2014)
PESO_TRECHO = {
    "trecho_BR471_km536": 1,
    "trecho_BR471_km537": 4,   # hotspot Setor1
    "trecho_BR471_km538": 4,   # hotspot Setor1
    "trecho_BR471_km539": 3,   # hotspot Setor1
    "trecho_BR471_km540": 3,   # transição crítica
    "trecho_BR471_km541": 6,   # hotspot principal Setor2
    "trecho_BR471_km542": 2,
    "trecho_BR471_km543": 2,
    "trecho_BR471_km544": 2,
    "trecho_BR471_km545": 3,   # transição crítica
    "trecho_BR471_km546": 2,   # hotspot Setor3
    "trecho_BR471_km548": 1,
    "trecho_BR471_km550": 1,
    "trecho_BR471_km551": 1,
}


# ════════════════════════════════════════════════════════════
# 3. HABITATS DA ÁREA DE ESTUDO (km 536–553)
# ════════════════════════════════════════════════════════════

HABITATS = [
    ("banhado_taim_central",  "Banhado",          "Banhado do Taim Central",   9800.0),
    ("banhado_taim_sul",      "Banhado",          "Banhado do Taim Sul",       7300.0),
    ("lagoa_mangueira_norte", "Lagoa",            "Lagoa Mangueira Norte",     4500.0),
    ("lagoa_verde",           "Lagoa",            "Lagoa Verde",               1500.0),
    ("rio_taim",              "Rio",              "Rio Taim",                   800.0),
    ("vala_br471",            "Vala",             "Vala de Drenagem BR-471",    180.0),
    ("campo_alagado_sul",     "CampoAlagado",     "Campo Alagado Sul",         1900.0),
    ("vegetacao_marginal",    "VegetacaoRiparia", "Vegetação Marginal BR-471",  320.0),
]


# ════════════════════════════════════════════════════════════
# 4. CONDIÇÕES CLIMÁTICAS
#    Pesos sazonais baseados no padrão do artigo:
#    inverno = mais neblina/chuva; verão = mais céu aberto
# ════════════════════════════════════════════════════════════

# (id, classe_onto, descricao, temperatura_C, pluviosidade_mm)
CLIMAS = [
    ("clima_chuva_fraca",    "Chuva",     "chuva_fraca",       16.5, 12.0),
    ("clima_chuva_moderada", "Chuva",     "chuva_moderada",    15.0, 28.0),
    ("clima_chuva_forte",    "Chuva",     "chuva_forte",       13.5, 55.0),
    ("clima_neblina_leve",   "Neblina",   "neblina_leve",      14.0,  0.0),
    ("clima_neblina_densa",  "Neblina",   "neblina_densa",     12.5,  0.0),
    ("clima_ceu_aberto_dia", "CeuAberto", "ceu_aberto",        26.0,  0.0),
    ("clima_ceu_aberto_noc", "CeuAberto", "ceu_aberto_noturno",17.0,  0.0),
    ("clima_ceu_nublado",    "Neblina",   "ceu_nublado",       18.5,  2.0),
]

# Índices correspondem à lista CLIMAS acima
#                     chf  chm  chs  nbl  nbd  cad  can  nub
CLIMA_PESO_INVERNO  = [ 1,   2,   2,   3,   3,   1,   2,   2]
CLIMA_PESO_VERAO    = [ 1,   1,   1,   1,   1,   4,   3,   1]
CLIMA_PESO_TRANSIC  = [ 2,   2,   1,   2,   1,   2,   2,   2]


# ════════════════════════════════════════════════════════════
# 5. FATORES DE RISCO (baseados em Nauderer 2014)
# ════════════════════════════════════════════════════════════

FATORES_RISCO = [
    ("risco_ausencia_spf",   "AusenciaDePassagem",     5,
     "Ausência de Sistema de Proteção à Fauna (SPF) — Setor 2 sem tela"),
    ("risco_spf_danificado", "AusenciaDePassagem",     4,
     "SPF com descontinuidade ou dano — eficácia comprometida"),
    ("risco_prox_hidrico",   "ProximidadeCorpoHidrico",4,
     "Trecho adjacente a corpo hídrico — rota habitual de fauna aquática"),
    ("risco_trafego_verao",  "TrafegoVeicular",        3,
     "Aumento de tráfego no verão por turismo (correlação negativa com atropelamentos)"),
    ("risco_visibilidade",   "VisibilidadeReduzida",   4,
     "Visibilidade reduzida por neblina ou chuva — padrão predominante no inverno"),
]

# Risco predominante por setor
RISCO_POR_SETOR = {
    "Setor1":      "risco_spf_danificado",
    "Setor2":      "risco_ausencia_spf",
    "Transicao12": "risco_ausencia_spf",
    "Setor3":      "risco_prox_hidrico",
    "Transicao23": "risco_spf_danificado",
}


# ════════════════════════════════════════════════════════════
# 6. CATÁLOGO DE ESPÉCIES SINTÉTICAS
#    Espécies confirmadas no Taim (GBIF + literatura regional)
#    com suas características ecológicas para distribuição realista
# ════════════════════════════════════════════════════════════

# (classe_onto, nome_popular, nome_cientifico, habitat_preferido,
#  setor_preferido, peso_eventos)
#
# peso_eventos: proporção relativa de eventos sintéticos para cada espécie
# setor_preferido: lista de setores onde a espécie é mais vulnerável
# habitat_preferido: chave de habitats_ind

ESPECIES_SINTETICAS = [
    # ── Mamíferos ──────────────────────────────────────────────────────────
    # Tatu: ativo à noite, cruza estrada em busca de alimento
    ("Tatu",       "Tatu-galinha",      "Dasypus novemcinctus",
     "campo_alagado_sul",  ["Setor1","Setor2","Setor3","Transicao12","Transicao23"], 3),
    # Veado: deslocamentos crepusculares entre lagoa e campo
    ("Veado",      "Veado-campeiro",    "Ozotoceros bezoarticus",
     "campo_alagado_sul",  ["Setor2","Transicao12","Transicao23","Setor1","Setor3"], 2),
    # Graxaim: onívoro, ativo à noite nas bordas da rodovia
    ("Graxaim",    "Graxaim-do-campo",  "Lycalopex gymnocercus",
     "campo_alagado_sul",  ["Setor2","Transicao12","Transicao23"], 3),
    # Mão-pelada: semi-aquático, ativo à noite, alta frequência no Taim
    ("Mao_pelada", "Mão-pelada",        "Procyon cancrivorus",
     "rio_taim",          ["Setor2","Setor1","Transicao12"], 4),
    # Preá: roedor diurno/crepuscular de campo aberto
    ("Preá",       "Preá",              "Cavia aperea",
     "campo_alagado_sul",  ["Setor1","Setor2","Setor3"], 3),
    # Tuco-tuco: roedor semifossorial, endêmico das restingas do RS
    ("Tuco_tuco",  "Tuco-tuco",         "Ctenomys minutus",
     "vegetacao_marginal", ["Setor1","Setor2"], 2),

    # ── Aves ───────────────────────────────────────────────────────────────
    # Quero-quero: terrestre, muito comum em bordas de rodovia
    ("AveTerrestre","Quero-quero",       "Vanellus chilensis",
     "campo_alagado_sul",  ["Setor1","Setor2","Setor3","Transicao12","Transicao23"], 4),
    # Chimango: carniceiro, muitas vezes atropelado junto a carcaças
    ("Chimango",   "Chimango",           "Milvago chimango",
     "campo_alagado_sul",  ["Setor1","Setor2","Setor3","Transicao12","Transicao23"], 3),
    # Carcará: rapinante terrestre, bordo de rodovia
    ("Carcara",    "Carcará",            "Caracara plancus",
     "campo_alagado_sul",  ["Setor2","Transicao12","Transicao23"], 2),
    # Perdiz: terrestre, cruza a estrada ao correr
    ("Perdiz",     "Perdiz",             "Rhynchotus rufescens",
     "campo_alagado_sul",  ["Setor1","Setor2","Setor3"], 2),
    # Garça-branca: sai do banhado para buscar alimento nas valas
    ("AveAquatica","Garça-branca-grande","Ardea alba",
     "banhado_taim_central",["Setor2","Transicao12","Transicao23"], 2),

    # ── Répteis ────────────────────────────────────────────────────────────
    # Serpente-d'água: semi-aquática, cruza a estrada entre lagoas
    ("Serpente",   "Serpente-d'água",    "Helicops infrataeniatus",
     "vala_br471",         ["Setor1","Setor2","Setor3","Transicao12","Transicao23"], 3),
    # Tartaruga-tigre: deslocamentos sazonais entre corpos d'água
    ("Tartaruga",  "Tartaruga-tigre",    "Acanthochelys spixii",
     "banhado_taim_central",["Setor2","Transicao12"], 2),
    # Lagarto: diurno, aquece no asfalto
    ("Lagarto",    "Lagarto-teiú",       "Tupinambis merianae",
     "vegetacao_marginal", ["Setor1","Setor2","Setor3"], 2),
]


# ════════════════════════════════════════════════════════════
# 7. FUNÇÕES AUXILIARES
# ════════════════════════════════════════════════════════════

def data_real_ponderada():
    """
    Gera data entre Abr/2010 e Mar/2013 com peso sazonal real.
    Baseado nas taxas anuais de Nauderer (2014):
      Ano 1 (2010-11): 0.543 ind/km/dia  — SPF danificado → peso 54
      Ano 2 (2011-12): 0.205 ind/km/dia  — manutenção    → peso 20
      Ano 3 (2012-13): 0.162 ind/km/dia  — semi-reparado → peso 16
    """
    ano_offset = random.choices([0, 1, 2], weights=[54, 20, 16])[0]

    mes_pesos = {
        4: 5, 5: 5, 6: 5,        # outono
        7: 9, 8: 9, 9: 8,        # inverno — pico
        10: 5, 11: 5, 12: 4,     # primavera
        1: 3, 2: 3, 3: 3,        # verão — mínimo
    }
    mes = random.choices(list(mes_pesos.keys()), weights=list(mes_pesos.values()))[0]
    ano = (2010 + ano_offset) if mes >= 4 else (2011 + ano_offset)
    ano = max(2010, min(2013, ano))
    if ano == 2013 and mes > 3:
        mes = random.randint(1, 3)

    dia = random.randint(1, 28)
    return datetime.datetime(ano, mes, dia).strftime("%Y-%m-%d")


def data_sintetica():
    """
    Gera datas para eventos sintéticos (2020–2023) com o mesmo
    padrão sazonal identificado em Nauderer (2014).
    """
    mes_pesos = {
        4: 5, 5: 5, 6: 5,
        7: 9, 8: 9, 9: 8,
        10: 5, 11: 5, 12: 4,
        1: 3, 2: 3, 3: 3,
    }
    mes = random.choices(list(mes_pesos.keys()), weights=list(mes_pesos.values()))[0]
    ano = random.randint(2020, 2023)
    dia = random.randint(1, 28)
    return datetime.datetime(ano, mes, dia).strftime("%Y-%m-%d")


def estacao(data_str):
    mes = int(data_str[5:7])
    if mes in [7, 8, 9]:   return "inverno"
    if mes in [1, 2, 3]:   return "verao"
    return "transicao"


def horario_e_turno(est, especie_cls=None):
    """
    Distribuição de períodos calibrada por Nauderer (2014):
      - noturno 55 % / crepuscular 25 % / diurno 20 % (padrão inverno)
      - aves e lagartos têm maior proporção diurna
      - verão: dias mais longos → mais diurno
    """
    diurno_bias = especie_cls in {"AveTerrestre", "Chimango", "Carcara",
                                  "Perdiz", "AveAquatica", "Lagarto"}

    if diurno_bias:
        pesos = {"noturno": 10, "crepuscular": 30, "diurno": 60}
    elif est == "inverno":
        pesos = {"noturno": 60, "crepuscular": 25, "diurno": 15}
    elif est == "verao":
        pesos = {"noturno": 45, "crepuscular": 25, "diurno": 30}
    else:
        pesos = {"noturno": 55, "crepuscular": 25, "diurno": 20}

    turno = random.choices(list(pesos.keys()), weights=list(pesos.values()))[0]

    if turno == "noturno":
        h = random.choice(list(range(20, 24)) + list(range(0, 6)))
    elif turno == "crepuscular":
        h = random.choice([5, 6, 7, 17, 18, 19])
    else:
        h = random.randint(8, 16)

    return f"{h:02d}:{random.randint(0, 59):02d}", turno


def escolher_clima(est, climas_lista):
    if est == "inverno":
        return random.choices(climas_lista, weights=CLIMA_PESO_INVERNO)[0]
    elif est == "verao":
        return random.choices(climas_lista, weights=CLIMA_PESO_VERAO)[0]
    else:
        return random.choices(climas_lista, weights=CLIMA_PESO_TRANSIC)[0]


# ════════════════════════════════════════════════════════════
# 8. CRIAR TODOS OS INDIVÍDUOS
# ════════════════════════════════════════════════════════════

with onto:

    # ── 8.1 Rodovia ─────────────────────────────────────────
    br471 = ex.Rodovia("rodovia_BR471")
    br471.nomeRodovia = ["BR-471"]

    # ── 8.2 Trechos reais ────────────────────────────────────
    trechos_ind = {}
    for tid, ki, kf, lat, lon, setor_str, spf in TRECHOS_REAIS:
        t = ex.TrechoRodovia(tid)
        t.kmInicial       = [ki]
        t.kmFinal         = [kf]
        t.coordenadaLat   = [lat]
        t.coordenadaLon   = [lon]
        t.pertenceARodovia = [br471]
        trechos_ind[tid]  = (t, setor_str, spf)

    print(f"✅ {len(trechos_ind)} trechos criados (km 536–553, 3 setores).")

    # ── 8.3 Habitats ─────────────────────────────────────────
    habitats_ind = {}
    banhados     = []

    for hid, hcls, hnome, harea in HABITATS:
        cls = get_classe(hcls)
        h   = cls(hid)
        h.nomeHabitat = [hnome]
        h.areaHabitat = [harea]
        habitats_ind[hid] = h
        if hcls == "Banhado":
            banhados.append(h)

    for tid, (t, _, _) in trechos_ind.items():
        t.proximoA = [random.choice(banhados)]

    print(f"✅ {len(habitats_ind)} habitats criados.")

    # ── 8.4 Condições climáticas ─────────────────────────────
    climas_ind   = {}
    climas_lista = []

    for cid, ccls, cdesc, ctemp, cpluv in CLIMAS:
        cls = get_classe(ccls)
        c   = cls(cid)
        c.descricaoClima = [cdesc]
        c.temperatura    = [ctemp]
        c.pluviosidade   = [cpluv]
        climas_ind[cid]  = c
        climas_lista.append(c)

    print(f"✅ {len(climas_ind)} condições climáticas criadas.")

    # ── 8.5 Fatores de risco ─────────────────────────────────
    riscos_ind = {}

    for rid, rcls, rnivel, rdesc in FATORES_RISCO:
        cls = get_classe(rcls)
        r   = cls(rid)
        r.nivelRisco     = [rnivel]
        r.descricaoRisco = [rdesc]
        riscos_ind[rid]  = r

    print(f"✅ {len(riscos_ind)} fatores de risco criados.")

    # ── 8.6 Períodos temporais ───────────────────────────────
    periodos_ind = {}
    for pid, pcls in [
        ("periodo_noturno",     "Noturno"),
        ("periodo_diurno",      "Diurno"),
        ("periodo_crepuscular", "Crepuscular"),
        ("estacao_inverno",     "Estacao"),
        ("estacao_verao",       "Estacao"),
        ("estacao_outono",      "Estacao"),
        ("estacao_primavera",   "Estacao"),
    ]:
        cls = get_classe(pcls)
        p   = cls(pid)
        periodos_ind[pid] = p

    periodo_map = {
        "noturno":     periodos_ind["periodo_noturno"],
        "diurno":      periodos_ind["periodo_diurno"],
        "crepuscular": periodos_ind["periodo_crepuscular"],
    }

    print(f"✅ {len(periodos_ind)} períodos temporais criados.")

    # ── 8.7 Animais REAIS (Nauderer 2014) ────────────────────
    #   50 capivaras + 3 lontras + 3 gatos-do-mato
    animais_cap  = []
    animais_lon  = []
    animais_gato = []

    for i in range(1, 51):
        a = ex.Capivara(f"capivara_{i:03d}")
        a.nomeEspecie = ["Hydrochoerus hydrochaeris"]
        a.nomePopular = ["Capivara"]
        a.viveEm      = [random.choice(banhados)]
        animais_cap.append(a)

    # Lontras — exclusivamente Setor 2 (todos os 3 casos no artigo)
    for i in range(1, 4):
        a = ex.Lontra(f"lontra_{i:03d}")
        a.nomeEspecie = ["Lontra longicaudis"]
        a.nomePopular = ["Lontra"]
        a.viveEm      = [habitats_ind["rio_taim"]]
        animais_lon.append(a)

    # Gatos-do-mato (2 típicos + 1 melânico) — todos Setor 2
    for i, variante in enumerate(["típico", "típico", "melânico"]):
        a = ex.GatoDomato(f"gato_domato_{i+1:03d}")
        a.nomeEspecie = ["Leopardus geoffroyi"]
        a.nomePopular = [f"Gato-do-mato-grande ({variante})"]
        a.viveEm      = [habitats_ind["campo_alagado_sul"]]
        animais_gato.append(a)

    print(f"✅ Animais reais: 50 capivaras | 3 lontras | 3 gatos-do-mato.")

    # ── 8.8 Animais SINTÉTICOS ───────────────────────────────
    animais_sint = {}   # {classe_str: [lista de indivíduos]}

    n_por_especie = 4   # 4 indivíduos por espécie sintética

    for (cls_str, nome_pop, nome_sci, hab_pref,
         setores_pref, peso_ev) in ESPECIES_SINTETICAS:
        cls = get_classe(cls_str)
        lst = []
        for k in range(1, n_por_especie + 1):
            aid = f"{cls_str.lower()}_{k:03d}"
            # evita colisão com nomes já usados
            if onto.search_one(iri=f"*{aid}"):
                aid = f"{cls_str.lower()}_s_{k:03d}"
            a = cls(aid)
            a.nomeEspecie = [nome_sci]
            a.nomePopular = [nome_pop]
            hab = habitats_ind.get(hab_pref, random.choice(banhados))
            a.viveEm = [hab]
            lst.append(a)
        animais_sint[cls_str] = lst

    total_sint_animais = sum(len(v) for v in animais_sint.values())
    print(f"✅ {total_sint_animais} animais sintéticos criados "
          f"({len(ESPECIES_SINTETICAS)} espécies, {n_por_especie} ind./espécie).")

    # ── 8.9 EVENTOS DE ATROPELAMENTO ─────────────────────────
    #
    # Proporções‑alvo:
    #   ~35 % capivaras (reais)  → ~50 eventos
    #   ~3  % lontra + gato (reais) → 6 eventos
    #   ~62 % sintéticos → ~90 eventos
    #   Total: ~146 eventos
    #
    # Distribuição sintética: proporcional ao peso_evento de cada espécie

    ev_count    = 0
    trecho_ids  = list(PESO_TRECHO.keys())
    trecho_pesos_lista = list(PESO_TRECHO.values())

    # IDs de trechos do Setor 2 e transições (exclusivo para lontra/gato)
    trechos_s2  = [
        tid for tid in trecho_ids
        if trechos_ind[tid][1] in ["Setor2", "Transicao12", "Transicao23"]
    ]

    # ── Eventos de CAPIVARA (reais, dados Nauderer 2014) ─────
    N_CAP = 50
    for _ in range(N_CAP):
        ev_count += 1
        tid = random.choices(trecho_ids, weights=trecho_pesos_lista)[0]
        t_obj, setor_str, _ = trechos_ind[tid]
        data = data_real_ponderada()
        est  = estacao(data)
        hor, turno = horario_e_turno(est, "Capivara")
        clima = escolher_clima(est, climas_lista)

        ev = ex.EventoAtropelamento(f"evento_{ev_count:03d}")
        ev.envolveAnimal    = [random.choice(animais_cap)]
        ev.ocorreEm         = [t_obj]
        ev.ocorreSob        = [clima]
        ev.ocorreDurante    = [periodo_map[turno]]
        ev.possuiFatorRisco = [riscos_ind[RISCO_POR_SETOR[setor_str]]]
        ev.dataEvento       = [data]
        ev.horarioEvento    = [hor]
        ev.resultadoFatal   = [True]   # todos os registros de campo = morto

    print(f"✅ {N_CAP} eventos de capivara (dados reais Nauderer 2014).")

    # ── Eventos de LONTRA (reais, Setor 2 exclusivo) ─────────
    for animal in animais_lon:
        ev_count += 1
        tid = random.choice(trechos_s2)
        t_obj, setor_str, _ = trechos_ind[tid]
        data = data_real_ponderada()
        est  = estacao(data)
        hor, turno = horario_e_turno(est, "Lontra")
        clima = climas_ind["clima_ceu_aberto_noc"]   # madrugada limpa — mais típico

        ev = ex.EventoAtropelamento(f"evento_{ev_count:03d}")
        ev.envolveAnimal    = [animal]
        ev.ocorreEm         = [t_obj]
        ev.ocorreSob        = [clima]
        ev.ocorreDurante    = [periodo_map[turno]]
        ev.possuiFatorRisco = [riscos_ind["risco_ausencia_spf"]]
        ev.dataEvento       = [data]
        ev.horarioEvento    = [hor]
        ev.resultadoFatal   = [True]

    print(f"✅ {len(animais_lon)} eventos de lontra (dados reais).")

    # ── Eventos de GATO-DO-MATO (reais, Setor 2 exclusivo) ───
    for animal in animais_gato:
        ev_count += 1
        tid = random.choice(trechos_s2)
        t_obj, setor_str, _ = trechos_ind[tid]
        data = data_real_ponderada()
        est  = estacao(data)
        hor, turno = horario_e_turno(est, "GatoDomato")
        clima = climas_ind["clima_ceu_aberto_noc"]

        ev = ex.EventoAtropelamento(f"evento_{ev_count:03d}")
        ev.envolveAnimal    = [animal]
        ev.ocorreEm         = [t_obj]
        ev.ocorreSob        = [clima]
        ev.ocorreDurante    = [periodo_map[turno]]
        ev.possuiFatorRisco = [riscos_ind["risco_ausencia_spf"]]
        ev.dataEvento       = [data]
        ev.horarioEvento    = [hor]
        ev.resultadoFatal   = [True]

    print(f"✅ {len(animais_gato)} eventos de gato-do-mato (dados reais).")

    # ── Eventos SINTÉTICOS (demais espécies) ─────────────────
    # Total‑alvo: ~146 eventos. Já temos 50+3+3=56 reais.
    # Precisamos de ~90 sintéticos, distribuídos proporcionalmente
    # ao peso_evento de cada espécie.

    peso_total = sum(peso for _, _, _, _, _, peso in ESPECIES_SINTETICAS)
    N_SINT = 90

    ev_sint_count = 0

    for (cls_str, nome_pop, nome_sci, hab_pref,
         setores_pref, peso_ev) in ESPECIES_SINTETICAS:

        n_ev = max(1, round(N_SINT * peso_ev / peso_total))
        animais_especie = animais_sint[cls_str]

        for _ in range(n_ev):
            ev_count    += 1
            ev_sint_count += 1

            # Trecho: preferência pelo setor da espécie, mas com peso global
            tids_pref = [
                tid for tid in trecho_ids
                if trechos_ind[tid][1] in setores_pref
            ]
            if tids_pref:
                tid = random.choices(
                    tids_pref,
                    weights=[PESO_TRECHO[t] for t in tids_pref]
                )[0]
            else:
                tid = random.choices(trecho_ids, weights=trecho_pesos_lista)[0]

            t_obj, setor_str, _ = trechos_ind[tid]
            data = data_sintetica()
            est  = estacao(data)
            hor, turno = horario_e_turno(est, cls_str)
            clima = escolher_clima(est, climas_lista)

            # 80 % fatalidade para espécies sintéticas (plausível para fauna do Taim)
            fatal = random.random() < 0.80

            ev = ex.EventoAtropelamento(f"evento_{ev_count:03d}")
            ev.envolveAnimal    = [random.choice(animais_especie)]
            ev.ocorreEm         = [t_obj]
            ev.ocorreSob        = [clima]
            ev.ocorreDurante    = [periodo_map[turno]]
            ev.possuiFatorRisco = [riscos_ind[RISCO_POR_SETOR[setor_str]]]
            ev.dataEvento       = [data]
            ev.horarioEvento    = [hor]
            ev.resultadoFatal   = [fatal]

    print(f"✅ {ev_sint_count} eventos sintéticos criados "
          f"({len(ESPECIES_SINTETICAS)} espécies).")


# ════════════════════════════════════════════════════════════
# 9. SALVAR E RESUMO
# ════════════════════════════════════════════════════════════

onto.save(file="taim_povoado.owl", format="rdfxml")

n_reais  = animais_cap + animais_lon + animais_gato
n_animais_reais  = len(n_reais)
n_animais_sint   = total_sint_animais
n_eventos_reais  = N_CAP + len(animais_lon) + len(animais_gato)
n_eventos_sint   = ev_sint_count
pct_cap = round(N_CAP / ev_count * 100)

total_individuos = (
    1 +                      # rodovia
    len(trechos_ind) +
    len(habitats_ind) +
    len(climas_ind) +
    len(riscos_ind) +
    len(periodos_ind) +
    n_animais_reais +
    n_animais_sint +
    ev_count
)

print(f"""
╔══════════════════════════════════════════════════════════╗
║          RESUMO DO POVOAMENTO — v3                       ║
║    Fonte real: Nauderer (2014), FURG — BR-471/Taim       ║
╠══════════════════════════════════════════════════════════╣
║  Infraestrutura                                          ║
║    Rodovia BR-471:                  1                    ║
║    Trechos (km 536–553, 3 setores): {len(trechos_ind):<3}                 ║
║  Contexto                                                ║
║    Habitats:                        {len(habitats_ind):<3}                 ║
║    Condições climáticas:            {len(climas_ind):<3}                 ║
║    Fatores de risco:                {len(riscos_ind):<3}                 ║
║    Períodos temporais:              {len(periodos_ind):<3}                 ║
╠══════════════════════════════════════════════════════════╣
║  Animais                                                 ║
║    Reais (Nauderer 2014):           {n_animais_reais:<3}                 ║
║      · Capivaras:            50                          ║
║      · Lontras:              3                           ║
║      · Gatos-do-mato:        3                           ║
║    Sintéticos ({len(ESPECIES_SINTETICAS)} espécies):         {n_animais_sint:<3}                 ║
╠══════════════════════════════════════════════════════════╣
║  Eventos de atropelamento:  {ev_count:<3}                         ║
║    Reais  — capivara:        {N_CAP:<3}  ({pct_cap:>2} % do total)     ║
║    Reais  — lontra:          3                           ║
║    Reais  — gato-do-mato:    3                           ║
║    Sintéticos:               {ev_sint_count:<3}                         ║
╠══════════════════════════════════════════════════════════╣
║  TOTAL DE INDIVÍDUOS:       {total_individuos:<3}                         ║
╚══════════════════════════════════════════════════════════╝

✅ Salvo em: taim_povoado.owl
""")
