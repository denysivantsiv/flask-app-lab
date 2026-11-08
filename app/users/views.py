from flask import render_template, request, redirect, url_for, session, flash, make_response
from app.users import user_bp

# Заглушка логіна/пароля
VALID_USER = "user1"
VALID_PASS = "12345"

@user_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == VALID_USER and password == VALID_PASS:
            session["username"] = username
            flash("Успішний вхід у систему!", "success")
            return redirect(url_for("users.profile"))
        else:
            flash("Wrong data! Try again!", "danger")
            return redirect(url_for("users.login"))

    return render_template("users/login.html")

@user_bp.route("/logout")
def logout():
    session.pop("username", None)
    flash("Ви вийшли із системи.", "info")
    return redirect(url_for("users.login"))

@user_bp.route("/profile")
def profile():
    if "username" not in session:
        flash("Спочатку увійдіть у систему!", "warning")
        return redirect(url_for("users.login"))

    theme = request.cookies.get("theme", "light")
    cookies_data = request.cookies
    return render_template("users/profile.html", username=session["username"], cookies=cookies_data, theme=theme)

@user_bp.route("/add_cookie", methods=["POST"])
def add_cookie():
    if "username" not in session:
        return redirect(url_for("users.login"))

    key = request.form.get("key")
    val = request.form.get("value")
    max_age = request.form.get("max_age", type=int)

    resp = make_response(redirect(url_for("users.profile")))
    if key and val:
        resp.set_cookie(key, val, max_age=max_age if max_age else None)
        flash(f"Кукі '{key}' успішно додано!", "success")
    else:
        flash("Вкажіть ключ та значення!", "warning")
    return resp

@user_bp.route("/delete_cookie", methods=["POST"])
def delete_cookie():
    if "username" not in session:
        return redirect(url_for("users.login"))

    key = request.form.get("key")
    resp = make_response(redirect(url_for("users.profile")))
    if key:
        resp.delete_cookie(key)
        flash(f"Кукі '{key}' видалено!", "info")
    return resp

@user_bp.route("/delete_all_cookies", methods=["POST"])
def delete_all_cookies():
    if "username" not in session:
        return redirect(url_for("users.login"))

    resp = make_response(redirect(url_for("users.profile")))
    for key in request.cookies.keys():
        resp.delete_cookie(key)
    flash("Всі доступні кукі видалено!", "info")
    return resp

@user_bp.route("/set_theme/<string:theme_name>")
def set_theme(theme_name):
    resp = make_response(redirect(url_for("users.profile")))
    resp.set_cookie("theme", theme_name, max_age=60*60*24*30)
    flash(f"Встановлено {theme_name} тему!", "success")
    return resp