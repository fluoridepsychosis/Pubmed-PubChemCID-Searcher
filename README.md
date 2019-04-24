# Pubmed-PubChemCID-Searcher

A simple script that allows you to search PubMed using a molecule's PubChem CID.

The CID is a unique identifier which is used to label drugs and other substances by PubChem. It is useful as an unambiguous way of getting data about a particular compound. 

Unfortunately PubMed does not always label papers with unique identifiers of the molecules which they concern. This makes searching for all papers about a given drug, which may have many names, and whose names may also refer to other compounds, quite difficult.

This script uses the PubChem API to obtain a list of synonyms for a drug which is identified with it's CID. These synonyms are part of the MeSH controlled vocabulary PubMed uses to label papers. The script can then search PubMed for papers which match this list of names, and returns a list of all papers published within the a chosen number of days which relate to that molecule.

