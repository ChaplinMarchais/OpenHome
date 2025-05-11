import json
import uuid
from os import environ as env
from urllib.parse import quote_plus, urlencode

from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv
from flask import Flask, redirect, render_template, session, url_for, request
from flask_sock import Sock, ConnectionClosed
from helpers import *
from database import *

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

app = Flask(__name__)
app.secret_key = env.get("APP_SECRET_KEY")
sock = Sock(app)

db = env.get("DB_CONNECTION")
connections = {}

oauth = OAuth(app)

oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration',
)

# WS Controllers
@sock.route('/connect')
def connect(ws):
    data = {}
    device_id = ""
    connectionOpen = True
    while connectionOpen:
        try:
            data = json.loads(ws.receive())

            match data["action"]:
                case "connect":
                    device_id = generate_device_id(db, data["device_code"])
                    connections[device_id] = ws
                    connect_device(db, data["device_code"], data["name"])
                    print(f"Device {device_id} CONNECTED")

        except ConnectionClosed:
            connections[device_id] = None
            connectionOpen = False
            disconnect_device(db, data["device_code"], data["name"])
            print(f"Device {device_id} DISCONNECTED")
            pass

# Controllers API
@app.route("/")
def home():
    return render_template(
        "home.html",
        session=session.get("user"),
        pretty=json.dumps(session.get("user"), indent=4),
    )

@app.route("/devices", methods=["GET", "POST"])
@login_required
def devices():
    if request.method == "GET":
        return render_template("devices.html", devices = get_devices(db, session.get("user")))


@app.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    openid_sub = str(session["user"]["userinfo"]["sub"])

    # If user does not exist in users table then create an entry and generate a device registration code
    user = query(db, 'SELECT * FROM Users WHERE openid_sub = ?', params = (openid_sub,))
    if len(user) == 0:
        device_code = str(uuid.uuid4())
        query(db, "INSERT INTO Users (openid_sub, email, device_code) VALUES (?, ?, ?)", (openid_sub, session["user"]["userinfo"]["email"], device_code))
    else:
        session["user"]["userinfo"]["device_code"] = user[0]["device_code"]

    return redirect("/")


@app.route("/login")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )


@app.route("/logout")
@login_required
def logout():
    session.clear()
    return redirect(
        "https://"
        + env.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("home", _external=True),
                "client_id": env.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=env.get("PORT", 3000))
