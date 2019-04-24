#!/usr/bin/env python3

import requests
import json

unii = "CD35PMG570" # User inputs a unique chemical identifier called a UNII

url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/" +unii+ "/synonyms/json" # This constructs the url for the PubChem API

r = requests.get(url) # Here we are recovering the data from the API

synonyms_json = r

synonyms_list = synonyms_json.json() # Transforming the JSON data into a Python array for parsing

# The following block of code parses the nested arrays down to just a single list of synonyms for the drug.

synonyms_list = synonyms_list['InformationList']

synonyms_list = synonyms_list['Information']

synonyms_list = synonyms_list[0]

synonyms_list = synonyms_list['Synonym']

big_list = []

for synonym in synonyms_list:

    # First we create the Entrez API query URL
    entrez_url="https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&reldate=1&retmax=1000&retmode=json&term=" + synonym

    # Next we query the API for a list of papers which match that synonym
    entrez_response = requests.get(entrez_url)
    
    # We convert the list to a python array from json
    parsed_json = entrez_response.json()

    key = 'esearchresult'

    # This loop finds whether the json contains the term 'esearchresult' as a key, then appends the value associated with that key
    # (which is a list of pubmed IDs) to a larger, nested list called big_list
    if key in parsed_json:

        list_of_pmids = parsed_json["esearchresult"]["idlist"]

        big_list.append(list_of_pmids)
    
    else:
        pass

# Flattening the big_list
flat_array = [item for sublist in big_list for item in sublist]

# Removing duplicates from the array
flat_array = list(dict.fromkeys(flat_array))

for item in flat_array:

    # This loop is basically the same as the first one except it uses entrez eutils summary instead of eutils search to find info from the PMID,
    # then prints it to the output file

    # Creating the API query URL
    entrez_summary_url = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&retmode=json&id=" + item

    # Obtaining the summary for that PMID
    entrez_summary_response = requests.get(entrez_summary_url)

    # Converting the JSON into a Python Array
    summary_parsed_json = entrez_summary_response.json()

    # Converting the PMID to a string for concatenation to a URL
    pmid = str(item)
    
    pmid_key = "{}".format(pmid)

    # Creating PubMed URL for easy access
    pubmed_url = "https://www.ncbi.nlm.nih.gov/pubmed/" + pmid

    list_key = "result"

    if list_key in summary_parsed_json:

        # Obtaining paper title
        title = summary_parsed_json["result"][pmid_key]["title"]

        article_ids = summary_parsed_json["result"][pmid_key]["articleids"]

        matched_article_id = None

        # Obtaining the DOI for easy access
        for article_id in article_ids:
    
            if article_id['idtype'] == "doi":

                matched_article_id = article_id

                doi = "https://doi.org/" + matched_article_id['value']


        
        # Prints paper title, PMID and pubmed URL in a human-readable form
        print(title + " URL: " + pubmed_url  + " DOI: " + doi)

    else: 
        pass









