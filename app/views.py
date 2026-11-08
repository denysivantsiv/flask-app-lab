from flask import render_template, request
from app import app

@app.route('/')
def main():
    return render_template("index.html")

@app.route('/homepage')
def home():
    agent = request.user_agent.string
    return render_template("homepage.html", agent=agent)