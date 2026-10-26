from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def resume():
    return render_template('resume.html', title='Резюме | Денис Іванців')

@app.route('/contacts')
def contacts():
    return render_template('contacts.html', title='Контакти | Звʼязок зі мною')

if __name__ == '__main__':
    app.run(debug=True)