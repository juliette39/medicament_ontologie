# Ontologie des médicaments

Projet de création d'une Ontologie à partir de deux tsv de données sur les médicaments.
Les bases de données proviennent de : [base-donnees-publique.medicaments.gouv.fr](https://base-donnees-publique.medicaments.gouv.fr/telechargement.php?fbclid=IwAR0Dn0o25n9bgtNkhsE8HfmpAYWYgzAozD9FWDt5G0h-9XrGjOcldJWiXXU)

Nous avons utilisé deux bases :

- [CIS_bdpm.txt](https://base-donnees-publique.medicaments.gouv.fr/telechargement.php?fichier=CIS_bdpm.txt), dans le projet [CIS_bdpm.tsv](/CIS_bdpm.tsv)
- [CIS_COMPO_bdpm.txt](https://base-donnees-publique.medicaments.gouv.fr/telechargement.php?fichier=CIS_COMPO_bdpm.txt), dans le projet [CIS_COMPO_bdpm.tsv](/CIS_COMPO_bdpm.tsv)

La première base liste les médicaments, la deuxième leur composition.

Le fichier [convert.py](/convert.py) convertir les tsv en une ontologie owl [medicaments.owl](/medicaments.owl).

Une fois cette ontologie chargée dans [Jena](https://jena.apache.org), voici quelques règles et requêtes [SparQL](https://fr.wikipedia.org/wiki/SPARQL) pour interagir avec cette ontologie.

- [Ontologie des médicaments](#ontologie-des-médicaments)
  - [Récupération de tous les médicaments](#récupération-de-tous-les-médicaments)
  - [Récupération de tous les attributs d'un médicament](#récupération-de-tous-les-attributs-dun-médicament)
  - [Les substances dans les médicaments](#les-substances-dans-les-médicaments)
  - [10 médicaments contenant du Paracétamol](#10-médicaments-contenant-du-paracétamol)
  - [Tous les médicaments produit par Sandoz](#tous-les-médicaments-produit-par-sandoz)
  - [Tous les médicamment commercialisés](#tous-les-médicamment-commercialisés)
  - [Tous les médicaments ayant reçu une autorisation entre 2015 et 2019](#tous-les-médicaments-ayant-reçu-une-autorisation-entre-2015-et-2019)
  - [Sous classe de la voie d'administration des médicaments par voie orale](#sous-classe-de-la-voie-dadministration-des-médicaments-par-voie-orale)
  - [Autorisation valide/non valide](#autorisation-validenon-valide)
  - [Vieux médicament (\>20ans) encore autorisés](#vieux-médicament-20ans-encore-autorisés)
  - [Récapitulatif des règles Jena](#récapitulatif-des-règles-jena)

## Récupération de tous les médicaments

Requête :

```
PREFIX ns: <http://example.org/ontology#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX tg:<http://www.turnguard.com/functions#>

SELECT ?med ?titulaire ?voieAdministration ?statut ?commercialisation ?forme ?denomination
WHERE {
?med a ns:Medicament .
?med ns:Titulaire ?titulaire .
?med ns:VoieAdministration ?voieAdministration .
OPTIONAL {?med ns:StatutBdm ?statut .}
?med ns:EtatCommercialisation ?commercialisation .
?med ns:FormePharmaceutique ?forme .
?med ns:Denomination ?denomination .
}
```

## Récupération de tous les attributs d'un médicament

Requête :

```
PREFIX ns: <http://example.org/ontology#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX tg:<http://www.turnguard.com/functions#>

SELECT ?proprety ?object
WHERE {
<http://example.org/ontology#62611169> ?proprety ?object
}
```

## Les substances dans les médicaments

Requête :

```
PREFIX ns: <http://example.org/ontology#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX tg: <http://www.turnguard.com/functions#>

SELECT ?med ?denominationMedicament ?sub ?denominationSubstance
WHERE {
?med a ns:Medicament .
?med ns:Denomination ?denominationMedicament .
?med ns:ComprendSubstanceActive ?sub .
?sub a ns:SubstanceActive .
?sub ns:DenominationSubstance ?denominationSubstance
}
```

## 10 médicaments contenant du Paracétamol

D'abord on cherche le numéro du Paracétamol :

Requête :

```
PREFIX ns: <http://example.org/ontology#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX tg: <http://www.turnguard.com/functions#>

SELECT ?sub
WHERE {
?sub a ns:SubstanceActive .
?sub ns:DenominationSubstance "PARACÉTAMOL" .
}
```

Puis on cherche 1à médicament contenant du Paracétamol

Requête :

```
PREFIX ns: <http://example.org/ontology#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX tg: <http://www.turnguard.com/functions#>

SELECT ?med ?denominationMedicament
WHERE {
?med a ns:Medicament .
?med ns:Denomination ?denominationMedicament .
?med ns:ComprendSubstanceActive <http://example.org/ontology#02202> .
}
LIMIT 10
```

## Tous les médicaments produit par Sandoz

Requête :

```
PREFIX ns: <http://example.org/ontology#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX tg:<http://www.turnguard.com/functions#>

SELECT ?med ?denomination
WHERE {
?med a ns:Medicament .
?med ns:Titulaire " SANDOZ" .
?med ns:Denomination ?denomination .
}
```

## Tous les médicamment commercialisés

Requête :

```
PREFIX ns: <http://example.org/ontology#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX tg: <http://www.turnguard.com/functions#>

SELECT ?med ?denominationMedicament ?commercialisation
WHERE {
?med a ns:Medicament .
?med ns:Denomination ?denominationMedicament .
?med ns:EtatCommercialisation ?commercialisation .
FILTER (?commercialisation = "Commercialisée") .
}
```

## Tous les médicaments ayant reçu une autorisation entre 2015 et 2019

Requête :

```
PREFIX ns: <http://example.org/ontology#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX tg:<http://www.turnguard.com/functions#>

SELECT ?med ?denomination ?anneeAutorisation
WHERE {
?med a ns:Medicament .
?med ns:Denomination ?denomination .
?med ns:AObtenuAutorisation ?auth .
?auth a ns:Autorisation .
?auth ns:DateAMM ?anneeAutorisation .
FILTER (?anneeAutorisation >= 2015 && ?anneeAutorisation <= 2019) .
}
```

## Sous classe de la voie d'administration des médicaments par voie orale

On crée une règle pour créer une classe de Médicament nommée MedicamentOral, contentn tous les médoicaments qui se prennent par voie orale.

Règles :

```
@prefix ns: <http://example.org/ontology#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

[rule1: (?med rdf:type ns:Medicament) (?med ns:VoieAdministration "orale") ->  (?med rdf:type ns:MedicamentOral) ]
```

Requête :

```sparql
PREFIX ns: <http://example.org/ontology#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX tg: <http://www.turnguard.com/functions#>

SELECT ?med ?denomination ?voieAdmin
WHERE {
  ?med rdf:type ns:MedicamentOral .
  ?med ns:Denomination ?denomination .
  ?med ns:VoieAdministration ?voieAdmin .
}
```

## Autorisation valide/non valide

On crée un erègle pour créer une sous classe de autorisation pour définir si une autorisation est accordée ou non.

Règles :

```
[rule2: (?auth rdf:type ns:Autorisation) (?auth ns:StatutAdminAMM "Autorisation abrogée") ->  (?auth rdf:type ns:AutorisationNonValide)]
[rule3: (?auth rdf:type ns:Autorisation) (?auth ns:StatutAdminAMM "Autorisation archivée") ->  (?auth rdf:type ns:AutorisationNonValide)]
[rule4: (?auth rdf:type ns:Autorisation) (?auth ns:StatutAdminAMM "Autorisation retirée") ->  (?auth rdf:type ns:AutorisationNonValide)]
[rule5: (?auth rdf:type ns:Autorisation) (?auth ns:StatutAdminAMM "Autorisation active") ->  (?auth rdf:type ns:AutorisationValide)]
```

Requête :

```
PREFIX ns: <http://example.org/ontology#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX tg: <http://www.turnguard.com/functions#>

SELECT ?med ?denomination ?status
WHERE {
?med a ns:Medicament .
?med ns:Denomination ?denomination .
?med ns:AObtenuAutorisation ?auth .
?auth a ns:AutorisationNonValide .
?auth ns:StatutAdminAMM ?status .

}
```

## Vieux médicament (>20ans) encore autorisés

On crée deux règles, une pour dire si une autorisation valide a plus de 20 ans, l'autre pour dire si un médicament a une ancienne autirisation, alors c'est une sous classe de Médicament : VieuxMedoc.

Règle :

```
[rule6: (?auth rdf:type ns:AutorisationValide) (?auth ns:DateAMM ?date) lessThan(?date, 2004) ->  (?auth rdf:type ns:VieilleAutorisation)]
[rule7: (?med rdf:type ns:Medicament) (?med ns:AObtenuAutorisation ?auth) (?auth rdf:type ns:VieilleAutorisation) ->  (?med rdf:type ns:VieuxMedoc)]
```

Requête :

```
PREFIX ns: <http://example.org/ontology#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX tg:<http://www.turnguard.com/functions#>

SELECT ?med ?denomination ?statutAutorisation ?dateAutorisation
WHERE {
?med a ns:VieuxMedoc .
?med ns:Denomination ?denomination .
?med ns:AObtenuAutorisation ?auth .
?auth a ns:Autorisation .
?auth ns:DateAMM ?dateAutorisation .
?auth ns:StatutAdminAMM ?statutAutorisation .
}
```

## Récapitulatif des règles Jena

```
@prefix ns: <http://example.org/ontology#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

[rule1: (?med rdf:type ns:Medicament) (?med ns:VoieAdministration "orale") ->  (?med rdf:type ns:MedicamentOral) ]
[rule2: (?auth rdf:type ns:Autorisation) (?auth ns:StatutAdminAMM "Autorisation abrogée") ->  (?auth rdf:type ns:AutorisationNonValide)]
[rule3: (?auth rdf:type ns:Autorisation) (?auth ns:StatutAdminAMM "Autorisation archivée") ->  (?auth rdf:type ns:AutorisationNonValide)]
[rule4: (?auth rdf:type ns:Autorisation) (?auth ns:StatutAdminAMM "Autorisation retirée") ->  (?auth rdf:type ns:AutorisationNonValide)]
[rule5: (?auth rdf:type ns:Autorisation) (?auth ns:StatutAdminAMM "Autorisation active") ->  (?auth rdf:type ns:AutorisationValide)]
[rule6: (?auth rdf:type ns:AutorisationValide) (?auth ns:DateAMM ?date) lessThan(?date, 2004) ->  (?auth rdf:type ns:VieilleAutorisation)]
[rule7: (?med rdf:type ns:Medicament) (?med ns:AObtenuAutorisation ?auth) (?auth rdf:type ns:VieilleAutorisation) ->  (?med rdf:type ns:VieuxMedoc)]
```