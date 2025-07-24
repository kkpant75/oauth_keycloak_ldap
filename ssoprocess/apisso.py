from flask import Flask, jsonify
from flask_oidc import OpenIDConnect
from oauth2client.client import OAuth2Credentials

app = Flask(__name__)

# OIDC configuration (adjust for your Keycloak realm)
app.config.update({
    'SECRET_KEY': 'some-random-secret',
    'OIDC_CLIENT_SECRETS': 'client_secrets.json',
    'OIDC_SCOPES': ['openid', 'email', 'profile'],
    'OIDC_INTROSPECTION_AUTH_METHOD': 'client_secret_post',
    'OIDC_RESOURCE_SERVER_ONLY': True,
})

oidc = OpenIDConnect(app)

@app.route('/private')
@oidc.accept_token('openid')
def private():
    return jsonify({'message': 'Welcome! You are authenticated via SSO.'})

if __name__ == '__main__':
    app.run(debug=True)
