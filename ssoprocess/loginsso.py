from flask import Flask, session, redirect, url_for
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)
app.secret_key = 'YOUR_SECRET'

oauth = OAuth(app)

oauth.register(
    name='keycloak',
    client_id='flask-client',
    client_secret='mRnGIkCPwXgvRXVMLL6qj5N5JmWaGqPI',
    server_metadata_url='http://localhost:8082/realms/kkrealm/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid profile email'}
)

@app.route('/')
def home():
    user = session.get('user')
    if user:
        return f'Hello {user["preferred_username"]}'
    return '<a href="/login">Login</a>'

@app.route('/login')
def login():
    return oauth.keycloak.authorize_redirect(redirect_uri=url_for('auth', _external=True))

# @app.route('/auth')
# def auth():
    # token = oauth.keycloak.authorize_access_token()
    # user = oauth.keycloak.parse_id_token(token)
    # session['user'] = user
    # return redirect('/')
    
@app.route('/auth')
def auth():
    token = oauth.keycloak.authorize_access_token()
    user = oauth.keycloak.userinfo()  # ✅ no need for parse_id_token
    session['user'] = user
    return redirect('/')    

@app.route('/logout')
def logout():
    session.clear()
    return redirect('http://localhost:8082/realms/kkrealm/protocol/openid-connect/logout')

if __name__ == '__main__':
    app.run(port=5000)
