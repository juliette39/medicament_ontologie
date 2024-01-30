from rdflib import Graph, Literal, Namespace, RDF, URIRef
from rdflib.namespace import OWL, RDFS
import csv

medication_tsv_path = "/Users/juliettedebono/Documents/TSP/3A/Big Data/Projet Ontology/CIS_bdpm.tsv"
substance_tsv_path = "/Users/juliettedebono/Documents/TSP/3A/Big Data/Projet Ontology/CIS_COMPO_bdpm.tsv"

def tsv_to_dict(tsv_file_path, header):
    data = []
    with open(tsv_file_path, newline='', encoding='ISO-8859-1') as tsvfile:
        csv_reader = csv.reader(tsvfile, delimiter='\t')
        for row in csv_reader:
            dico = {}
            for i in range(len(header)):
                dico[header[i]] = row[i]
            data.append(dico)
    return data

header_medication = ["CodeCIS", "Dénomination", "FormePharmaceutique", "VoieAdministration", "StatutAdminAMM",
"TypeProcedureAAM", "EtatCommercialisation", "DateAMM", "StatutBdm", "NumAutorisationEU", 
"Titulaire", "Surveillance"]

header_substance = ["CodeCIS", "ÉlémentPharmaceutique", "CodeSubstance", "DénominationSubstance", 
"DosageSubstance", "RefDosage", "NatureComposant", "Numéro"]

data_medication = tsv_to_dict(medication_tsv_path, header_medication)
data_substance = tsv_to_dict(substance_tsv_path, header_substance)

ns = Namespace("http://example.org/ontology#")
g = Graph()

g.bind("ex", ns)

for row in data_medication:
    medicament_uri = ns[row["CodeCIS"]]
    g.add((medicament_uri, RDF.type, ns.Medicament))
    g.add((medicament_uri, ns.Denomination, Literal(row["Dénomination"])))
    g.add((medicament_uri, ns.FormePharmaceutique, Literal(row["FormePharmaceutique"])))
    g.add((medicament_uri, ns.EtatCommercialisation, Literal(row["EtatCommercialisation"])))
    g.add((medicament_uri, ns.StatutBdm, Literal(row["StatutBdm"])))
    g.add((medicament_uri, ns.VoieAdministration, Literal(row["VoieAdministration"])))
    g.add((medicament_uri, ns.Titulaire, Literal(row["Titulaire"])))


    autorisation_uri = ns[f'Autorisation_{row["CodeCIS"]}']
    g.add((autorisation_uri, RDF.type, ns.Autorisation))
    g.add((medicament_uri, ns.AObtenuAutorisation, autorisation_uri))
    g.add((autorisation_uri, ns.StatutAdminAMM, Literal(row["StatutAdminAMM"])))
    g.add((autorisation_uri, ns.TypeProcedureAAM, Literal(row["TypeProcedureAAM"])))
    date = row["DateAMM"]
    dateList = date.split("/")
    if len(dateList) > 2:
        year = int(dateList[-1])
    else:
        year = date
    g.add((autorisation_uri, ns.DateAMM, Literal(year)))


for row in data_substance:
    substance_uri = ns[row["CodeSubstance"]]
    g.add((substance_uri, RDF.type, ns.SubstanceActive))
    g.add((substance_uri, ns.DenominationSubstance, Literal(row["DénominationSubstance"])))

    medicament_uri = ns[row["CodeCIS"]]
    g.add((medicament_uri, ns.ComprendSubstanceActive, substance_uri))


g.serialize("medicaments.owl", format="xml")
