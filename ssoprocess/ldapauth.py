from flask import Flask, request, jsonify
from ldap3 import Server, Connection, ALL, NTLM, ALL_ATTRIBUTES, SUBTREE

app = Flask(__name__)

LDAP_SERVER = 'ldap://localhost'   # e.g. ldap://ldap.myorg.local
BASE_DN = 'dc=myorg,dc=local'

@app.route('/auth', methods=['POST'])
def ldap_auth():
    data = request.json
    username = data.get('username')  # e.g. 'kpant'
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400
    
    user_dn = f'uid={username},{BASE_DN}'

    server = Server(LDAP_SERVER, get_info=ALL)
    print(server)
    try:
        # Attempt to bind with user credentials
        conn = Connection(server, user=user_dn, password=password, auto_bind=True)
        # If bind successful, user authenticated
        print("before...",conn)
        conn.unbind()
        print(conn)
        return jsonify({'status': 'success', 'message': 'Authenticated'})
    except Exception as e:
        return jsonify({'status': 'fail', 'message': 'Authentication failed', 'error': str(e)}), 401

if __name__ == '__main__':
    app.run(debug=True)
