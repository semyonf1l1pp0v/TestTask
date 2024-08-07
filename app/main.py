from typing import Optional

from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
import bcrypt
import sqlite3

app = FastAPI()


def open_html(filename):
    with open(filename) as file:
        html_response = file.read()
    return HTMLResponse(content=html_response)


@app.get("/", response_class=HTMLResponse)
def homepage():
    return open_html("app/templates/homepage.html")


@app.get("/login", response_class=HTMLResponse)
def authpage():
    return open_html("app/templates/authform.html")


@app.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    connection = sqlite3.connect("app/databases/TestTask.db")
    cursor = connection.cursor()
    cursor.execute("SELECT hashed_password from USERS where username = ?", [username])
    fetch_result = cursor.fetchall()
    if not fetch_result:
        return open_html("app/templates/incorrect_cred.html")
    password_from_db = fetch_result[0][0]
    if bcrypt.checkpw(password.encode(), password_from_db):
        return open_html("app/templates/correct_cred.html")
    else:
        return open_html("app/templates/incorrect_cred.html")


@app.get("/appsec")
def get_practice(key: Optional[str] = None):
    if not key:
        return open_html("app/templates/appsec.html")
    connection = sqlite3.connect("app/databases/TestTask.db")
    cursor = connection.cursor()
    cursor.execute("SELECT description from APPSEC where acronym = ?", [key.upper()])
    fetch_result = cursor.fetchall()
    if not fetch_result:
        return {"error": "key not found"}
    else:
        return {key.upper(): fetch_result[0][0]}


@app.get("/appsec/all")
def get_all_practices():
    connection = sqlite3.connect("app/databases/TestTask.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * from APPSEC")
    fetch_result = cursor.fetchall()
    return {el[0]: el[1] for el in fetch_result}
