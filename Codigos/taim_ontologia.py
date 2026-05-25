"""
Ontologia OWL - Banhado do Taim
Disciplina: Inteligência Artificial
Ferramenta: owlready2
Aluno: Raul Hohgraefe da Cruz
"""

from owlready2 import *

onto = get_ontology("http://www.exemplo.org/taim#")

with onto:

    # =========================================================
    # CLASSES PRINCIPAIS
    # =========================================================

    class Animal(Thing): pass
    class Habitat(Thing): pass
    class Infraestrutura(Thing): pass
    class EventoAtropelamento(Thing): pass
    class CondicaoAmbiental(Thing): pass
    class FatorRisco(Thing): pass
    class PeriodoTemporal(Thing): pass

    # =========================================================
    # HIERARQUIA: Animal
    # =========================================================

    class Mamifero(Animal): pass
    class Ave(Animal): pass
    class Reptil(Animal): pass

    class Capivara(Mamifero): pass
    class Lontra(Mamifero): pass
    class Tatu(Mamifero): pass
    class Veado(Mamifero): pass

    class AveAquatica(Ave): pass
    class AveTerrestre(Ave): pass

    class Serpente(Reptil): pass
    class Tartaruga(Reptil): pass

    # =========================================================
    # HIERARQUIA: Habitat
    # =========================================================

    class Banhado(Habitat): pass
    class CorpoDagua(Habitat): pass
    class VegetacaoRiparia(Habitat): pass
    class CampoAlagado(Habitat): pass

    class Lagoa(CorpoDagua): pass
    class Rio(CorpoDagua): pass
    class Vala(CorpoDagua): pass

    # =========================================================
    # HIERARQUIA: Infraestrutura
    # =========================================================

    class Rodovia(Infraestrutura): pass
    class TrechoRodovia(Infraestrutura): pass
    class Ponte(Infraestrutura): pass
    class Acostamento(Infraestrutura): pass

    # =========================================================
    # HIERARQUIA: CondicaoAmbiental
    # =========================================================

    class CondicaoClimatica(CondicaoAmbiental): pass
    class NivelLuminosidade(CondicaoAmbiental): pass
    class Estacao(PeriodoTemporal): pass
    class Horario(PeriodoTemporal): pass

    class Chuva(CondicaoClimatica): pass
    class Neblina(CondicaoClimatica): pass
    class CeuAberto(CondicaoClimatica): pass

    class Diurno(NivelLuminosidade): pass
    class Noturno(NivelLuminosidade): pass
    class Crepuscular(NivelLuminosidade): pass

    # =========================================================
    # HIERARQUIA: FatorRisco
    # =========================================================

    class TrafegoVeicular(FatorRisco): pass
    class VisibilidadeReduzida(FatorRisco): pass
    class ProximidadeCorpoHidrico(FatorRisco): pass
    class AusenciaDePassagem(FatorRisco): pass

    # =========================================================
    # PROPRIEDADES DE OBJETO (Object Properties)
    # =========================================================

    # Relações do EventoAtropelamento
    class envolveAnimal(ObjectProperty):
        domain = [EventoAtropelamento]
        range  = [Animal]

    class ocorreEm(ObjectProperty):
        domain = [EventoAtropelamento]
        range  = [TrechoRodovia]

    class ocorreSob(ObjectProperty):
        domain = [EventoAtropelamento]
        range  = [CondicaoAmbiental]

    class ocorreDurante(ObjectProperty):           # RELAÇÃO TEMPORAL
        domain = [EventoAtropelamento]
        range  = [PeriodoTemporal]

    class possuiFatorRisco(ObjectProperty):
        domain = [EventoAtropelamento]
        range  = [FatorRisco]

    # Relações espaciais (TrechoRodovia / Habitat)
    class proximoA(ObjectProperty):                # RELAÇÃO ESPACIAL
        domain = [TrechoRodovia]
        range  = [Habitat]

    class pertenceARodovia(ObjectProperty):
        domain = [TrechoRodovia]
        range  = [Rodovia]

    class contem(ObjectProperty):
        domain = [Habitat]
        range  = [Animal]

    # Relações do Animal
    class viveEm(ObjectProperty):
        domain = [Animal]
        range  = [Habitat]

    class atravessaRodovia(ObjectProperty):
        domain = [Animal]
        range  = [Rodovia]

    # Relações de FatorRisco
    class afetaVisibilidade(ObjectProperty):
        domain = [CondicaoClimatica]
        range  = [VisibilidadeReduzida]

    class aumentaRisco(ObjectProperty):
        domain = [CondicaoAmbiental]
        range  = [FatorRisco]

    # =========================================================
    # PROPRIEDADES DE DADOS (Data Properties)
    # =========================================================

    # Animal
    class nomeEspecie(DataProperty):
        domain = [Animal]
        range  = [str]

    class nomePopular(DataProperty):
        domain = [Animal]
        range  = [str]

    # TrechoRodovia
    class kmInicial(DataProperty):
        domain = [TrechoRodovia]
        range  = [float]

    class kmFinal(DataProperty):
        domain = [TrechoRodovia]
        range  = [float]

    class coordenadaLat(DataProperty):             # DADO ESPACIAL
        domain = [TrechoRodovia]
        range  = [float]

    class coordenadaLon(DataProperty):             # DADO ESPACIAL
        domain = [TrechoRodovia]
        range  = [float]

    class nomeRodovia(DataProperty):
        domain = [Rodovia]
        range  = [str]

    # EventoAtropelamento
    class dataEvento(DataProperty):                # DADO TEMPORAL
        domain = [EventoAtropelamento]
        range  = [str]   # formato ISO: "2024-03-15"

    class horarioEvento(DataProperty):             # DADO TEMPORAL
        domain = [EventoAtropelamento]
        range  = [str]   # formato "HH:MM"

    class resultadoFatal(DataProperty):
        domain = [EventoAtropelamento]
        range  = [bool]

    # CondicaoClimatica
    class descricaoClima(DataProperty):
        domain = [CondicaoClimatica]
        range  = [str]

    class temperatura(DataProperty):
        domain = [CondicaoClimatica]
        range  = [float]

    class pluviosidade(DataProperty):
        domain = [CondicaoClimatica]
        range  = [float]

    # Habitat
    class nomeHabitat(DataProperty):
        domain = [Habitat]
        range  = [str]

    class areaHabitat(DataProperty):
        domain = [Habitat]
        range  = [float]   # em hectares

    # FatorRisco
    class nivelRisco(DataProperty):
        domain = [FatorRisco]
        range  = [int]    # 1 a 5

    class descricaoRisco(DataProperty):
        domain = [FatorRisco]
        range  = [str]

    # =========================================================
    # RESTRIÇÕES (Restrictions)
    # =========================================================

    # Um EventoAtropelamento DEVE envolver pelo menos 1 animal
    EventoAtropelamento.is_a.append(
        envolveAnimal.min(1, Animal)
    )

    # Um EventoAtropelamento DEVE ocorrer em exatamente 1 trecho
    EventoAtropelamento.is_a.append(
        ocorreEm.exactly(1, TrechoRodovia)
    )

    # Um TrechoRodovia DEVE pertencer a exatamente 1 rodovia
    TrechoRodovia.is_a.append(
        pertenceARodovia.exactly(1, Rodovia)
    )

    # Capivara vive obrigatoriamente em Banhado ou CorpoDagua
    Capivara.is_a.append(
        viveEm.some(Banhado | CorpoDagua)
    )

    # AveAquatica vive em CorpoDagua
    AveAquatica.is_a.append(
        viveEm.some(CorpoDagua)
    )


# =========================================================
# SALVAR O ARQUIVO OWL
# =========================================================

onto.save(file="/home/claude/taim.owl", format="rdfxml")
print("✅ Ontologia salva em taim.owl")

# Resumo do que foi criado
classes    = list(onto.classes())
obj_props  = list(onto.object_properties())
data_props = list(onto.data_properties())

print(f"\n📊 Resumo:")
print(f"   Classes:               {len(classes)}")
print(f"   Propriedades objeto:   {len(obj_props)}")
print(f"   Propriedades de dados: {len(data_props)}")
print(f"\n📋 Classes criadas:")
for c in sorted(classes, key=lambda x: x.name):
    parents = [p.name for p in c.is_a if isinstance(p, ThingClass) and p.name != "Thing"]
    if parents:
        print(f"   {c.name} ← {', '.join(parents)}")
    else:
        print(f"   {c.name}  (raiz)")
