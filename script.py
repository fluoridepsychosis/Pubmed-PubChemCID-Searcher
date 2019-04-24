#!/usr/bin/env python3

import requests
import json

cid = input("Enter your CID: ") # User inputs a unique chemical identifier called a CID

days = input("How far back in time, in days, do you want the search to go?: ")



url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/" + cid + "/JSON?heading=mesh+entry+terms" # This constructs the url for the PubChem API


synonyms_json = requests.get(url) # Here we are recovering the data from the API

synonyms_list = synonyms_json.json() # Transforming the JSON data into a Python array for parsing

# The following block of code parses the nested arrays down to just a single list of synonyms for the drug.

synonyms_list = synonyms_list['Record']['Section'][0]['Section'][0]['Section'][0]['Information'][0]['Value']['StringWithMarkup']

big_list = []

for synonymdict in synonyms_list:

    for key, synonym in synonymdict.items():

        # First we create the Entrez API query URL
        entrez_url="https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&reldate=" +days+ "&retmax=1000&retmode=json&term=" + synonym

        # Next we query the API for a list of papers which match that synonym
        entrez_response = requests.get(entrez_url)
        
        # We convert the list to a python array from json
        parsed_json = entrez_response.json()

        key = 'esearchresult'

        name = synonym

        # This loop finds whether the json contains the term 'esearchresult' as a key, then appends the value associated with that key
        # (which is a list of pubmed IDs) to a larger, nested list called big_list
        if key in parsed_json:

            list_of_pmids = parsed_json["esearchresult"]["idlist"]

            namedict = {}

            for item in list_of_pmids:
                namedict[item] = name
    
        
        else:
            pass
        
        big_list.append(namedict)

# Flattening the big_list
flat_dictionary = {}

for dictionary in big_list:
    
    flat_dictionary.update(dictionary)


for key, item in flat_dictionary.items():

    # This loop is basically the same as the first one except it uses entrez eutils summary instead of eutils search to find info from the PMID,
    # then prints it to the output file

    # Creating the API query URL
    entrez_summary_url = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&retmode=json&id=" + key

    # Obtaining the summary for that PMID
    entrez_summary_response = requests.get(entrez_summary_url)

    # Converting the JSON into a Python Array
    summary_parsed_json = entrez_summary_response.json()

    # Converting the PMID to a string for concatenation to a URL
    pmid = str(key)
    
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
        print("[{}] ".format(item) + title + " URL: " + pubmed_url  + " DOI: " + doi)

    else: 
        pass









