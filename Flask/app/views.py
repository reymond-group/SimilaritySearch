from multiprocessing import Pool
import time
from app import app
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from flask import Flask, session, redirect, url_for, escape, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from flask_restful import reqparse
from .functs import similarity_search_annoy
from rdkit import Chem
from rdkit.Chem import AllChem


@app.route('/', methods=['GET']) 
def index():
    """passes the data to the index HTML page
    
    Returns:
        render_template -- template for index.html
    """

    return render_template("index.html", DB = ['PubChem', 'ChEMBL'])
    
@app.route('/wait', methods=['POST', 'GET'])
def wait():    
    """gets the data from the user choices in index.html and 
        passes them to results.html: database, query SMILES and number of required NNs
       
    Returns:
        render_template -- wait.html
    """  

    body = render_template('wait.html')
    
    db = request.form['db']
    smiles = request.form['smiles']
    hits = request.form['hits']
    
    session['db'] = db
    session['smiles'] = smiles
    session['hits'] = hits

    predurl= "1; url=results"

    return (body, 200, {'Refresh': predurl})

@app.route('/results', methods=['POST', 'GET'])
def results():
    """gets the data from wait.html, calculates the NNs, 
    passes the results and the number of NN to results.html.

    Returns:
        render_template -- results.html
    """
    db = session.get('db', None)
    print(db)
    smiles = session.get('smiles', None)
    hits = session.get('hits', None)
    results = similarity_search_annoy(db, smiles, hits)

    if db == 'PubChem':
        ID = 'CID '
        url = 'https://pubchem.ncbi.nlm.nih.gov/compound/'
    else:
        ID = ''
        url = 'https://www.ebi.ac.uk/chembl/compound/inspect/'

    return render_template('results.html', results = results, 
        hits = hits, query = smiles, db = db, ID = ID, url = url)


