# MXFP SimilaritySearch

This application is running at http://similaritysearch.gdb.tools/

The MXFP similarity search is a python Flask app which uses Annoy (Approximate Nearest Neighbors Oh Yeah, by Erik Bernhardsson, https://github.com/spotify/annoy) to search the MXFP non-Lipinski PubChem and non-Lipinski ChEMBL chemical spaces.

In each similarity search instance, the user chooses to search non-Lipinski PubChem or non-Lipinski ChEMBL, and the previously created correspondent Annoy file is selected. The Annoy file is used by the web app to retrieve the compound IDs of a pool of nearest neighbors. Then with a previously created ‘pickle saved’ python dictionary, the compound IDs are associated back to the correspondent PubChem or ChEMBL SMILES. The results are displayed using SmilesDrawer.

Annoy files and pickled saved python dictionaries have been created using `create_tree_dict.py`, and they can be downloaded at https://cloud.gdb.tools/s/m9odqsS2JDZPs3N

To run the app locally:
- Clone this repository
- Make sure you have a valid chemaxon license `license.cxl`
- Download the SimilaritySearchData (dictionaries and annoy files, 11.1 Gigabyte) at https://cloud.gdb.tools/s/m9odqsS2JDZPs3N 
- Run `docker run -p 8080:5000 --mount type=bind,target=/license.cxl,source=/your/absolut/path/license.cxl  --mount type=bind,target=/SimilaritySearchData,source=/your/absolut/path/SimilaritySearchData --mount type=bind,target=/app,source=/your/absolut/path/MXFPSimilaritySearch/Flask --name similaritysearch alicecapecchi/similaritysearchnew:latest`
- MXFP similarity search will be running at http://0.0.0.0:8080/


![MXFPSimilaritySearchInterface](https://cloud.gdb.tools/s/ACXc7NM3st2N3wK/preview)
