import logging
from flask import render_template, request, redirect, url_for, flash
from app import app
from app.forms import ContactForm

# Налаштування логера для контактної форми
logger = logging.getLogger("contact_logger")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("logs/contact_messages.log", encoding="utf-8")
file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
if not logger.handlers:
    logger.addHandler(file_handler)

@app.route('/')
def main():
    return render_template("index.html")

@app.route('/homepage')
def home():
    agent = request.user_agent.string
    return render_template("homepage.html", agent=agent)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        # Запис у лог-файл
        log_data = f"Name: {form.name.data} | Email: {form.email.data} | Phone: {form.phone.data} | Subject: {form.subject.data} | Message: {form.message.data}"
        logger.info(log_data)
        
        flash("Повідомлення успішно відправлено та збережено в системі!", "success")
        return redirect(url_for('contact')) # Дотримання патерну PRG
    elif request.method == 'POST':
        flash("Помилка при заповненні форми! Перевірте введені дані.", "danger")

    return render_template("contact.html", form=form)