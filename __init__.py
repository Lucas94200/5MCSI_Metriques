from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
import requests
from collections import Counter
import matplotlib.pyplot as plt
import io
import base64
                                                                                                                                       
app = Flask(__name__)                                                                                                                  
                                                                                                                                       
@app.route('/')
def hello_world():
    return render_template('hello.html')
  
@app.route('/contact/')
def contact():
    return render_template('contact.html')
  
@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15 # Conversion de Kelvin en °c 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)
  
@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")
    return jsonify(results=results)
  
@app.route('/histogramme/')
def histogramme():
    return render_template('histogramme.html')
  
@app.route('/commits/')
def commits_graph():
    # API GitHub pour récupérer les commits
    url = "https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits"
    response = requests.get(url)
    
    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch commits from GitHub API"}), response.status_code
    
    commits = response.json()
    
    # Extraire les minutes des dates de commits
    minutes = []
    for commit in commits:
        date_string = commit['commit']['author']['date']
        date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
        minutes.append(date_object.minute)
    
    # Compter les commits par minute
    commit_count = Counter(minutes)
    
    # Générer le graphique
    plt.figure(figsize=(10, 6))
    plt.bar(commit_count.keys(), commit_count.values())
    plt.title('Nombre de Commits par Minute')
    plt.xlabel('Minute')
    plt.ylabel('Nombre de Commits')
    plt.grid(axis='y')
    
    # Sauvegarder le graphique en base64 pour affichage dans HTML
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode('utf8')
    plt.close()

    return render_template("commits.html", graph_url=graph_url)

  
if __name__ == "__main__":
  app.run(debug=True)
