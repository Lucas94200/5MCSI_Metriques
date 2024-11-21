from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
                                                                                                                                       
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
def commits():
  
    repo_url = "https://api.github.com/repos/Lucas94200/5MCSI_Metriques/commits"
    response = requests.get(repo_url)
    
    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch commits from GitHub."})

    commits_data = response.json()
    results = {}

    for commit in commits_data:
     
        commit_date = commit['commit']['author']['date']
      
        date_object = datetime.strptime(commit_date, '%Y-%m-%dT%H:%M:%SZ')
        hour = date_object.strftime('%H:00')  # Grouper par heure
        
        if hour in results:
            results[hour] += 1
        else:
            results[hour] = 1

    chart_data = [{"hour": hour, "count": count} for hour, count in results.items()]
    return jsonify(chart_data)
  
if __name__ == "__main__":
  app.run(debug=True)
