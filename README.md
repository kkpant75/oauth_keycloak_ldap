# Enable Oath Process and Single Sign On (SSO) Using Opensource KEYCLOAK and LDAP and Flask Application

## Prerequisite
- Docker
- LDAP/AD
- Oauth Process
- Postman
- Python/CURL

# Docker Compose File

### Composed With
- LDAP Server
- PHP LDAP Admin Web UI
- Keycloak (SSO Server /Session Management)

# BackeEnd Systems

### LDAP
If docker compose file successfully deployed this will create 3 containers 
- openldap
- phpldapadmin
- keycloak

![Containers](https://github.com/kkpant75/oauth_keycloak_ldap/blob/master/Images/DockerContainer.png)

### Login in LDAP Server
Open Web URL http://localhost:8080 and Login Using
```
user: cn=admin,dc=myorg,dc=local
password:admin
```
# User/Group Details For The POC
```
Logged in as: cn=admin,dc=myorg,dc=local

 +--> dc=myorg,dc=local (3)
  +--> ou=UsersKK (2)
  | ---> uid=kpant
  | ---> uid=ramesh
  | ---> Create new entry here
  ---> uid=kout
  ---> uid=kpant
  ---> Create new entry here

```
![LdapServer](https://github.com/kkpant75/oauth_keycloak_ldap/blob/master/Images/ldpaUsers.png)


#### Create New Group/User Under (Using **Create new entry here**)
Create New Group using `Generic: Posix Group` in our case it is named as 
- **UsersKK**

![Create Group](https://github.com/kkpant75/oauth_keycloak_ldap/blob/master/Images/UserGroupCreate.png)

And Users via	`Generic: Simple Security Object` in this exmaple users are created under Group **UsersKK** as well as on root Level as detailed above
- kpant
- kout
- ramesh

![Create User](https://github.com/kkpant75/oauth_keycloak_ldap/blob/master/Images/UserCreate.png)

### KEYCLOACK (SSO Server)
Login in SSO server http://localhost:8082 -Click `Administrative Console` and use below credentials for login
```
user:admin
password:admin
```
![SSO Login Screen](https://github.com/kkpant75/oauth_keycloak_ldap/blob/master/Images/KeyCloak-Screen.png)

### Create New Realm 
After Login Left Pan Click Down Arrow Button To `Create New Realm` in this POC its named as `kkrealm`
![Create Realm](https://github.com/kkpant75/oauth_keycloak_ldap/blob/master/Images/realmcreate.png)

### Once New Realm Created Configure LDAP Server for User Authorization under `User Federation` for realm `kkrealm`
```
Connection URL *        ldap://openldap:389
Bind type *             simple
Bind DN *               cn=admin,dc=myorg,dc=local 
Bind credentials *      admin
UUID LDAP attribute     uid
```
Test KEYCLOACK Connectivity with LDAP Server And Sever Access as It shown in screen by providing above credentials

![Ldap Configuration](https://github.com/kkpant75/oauth_keycloak_ldap/blob/master/Images/LdapConfigure.png)

# Create Client
To Register Your Application with OAuth Server this is important Step
Register Application(Client) by configuring below details as shown in screen below
```
Client ID * 			flask-client
Name   					${flask-client}
Valid redirect URIs 	http://localhost:5000/auth
Web origins     		http://localhost:5000
```
![Create Client](https://github.com/kkpant75/oauth_keycloak_ldap/blob/master/Images/clientCreate.png)

### Important Step To Enable Application Authentication
Turn on to this Radio Button To convert Public to `Confidential`
```
Client authentication
```
)

### Copy Client Secret by Visiting the `Credential` Tab 
Create a File as `client_secrets.json` with below details


clinet-Secret  has to be filled with this screen data 
![Client Secret](https://github.com/kkpant75/oauth_keycloak_ldap/blob/master/Images/clientSecret.png)
```{
  "web": {
    "client_id": "flask-client",
    "client_secret": "mRnGIkCPwXgvRXVMLL6qj5N5JmWaGqPI",
    "auth_uri": "http://localhost:8082/realms/kkrealm/protocol/openid-connect/auth",
    "token_uri": "http://localhost:8082/realms/kkrealm/protocol/openid-connect/token",
    "userinfo_uri": "http://localhost:8082/realms/kkrealm/protocol/openid-connect/userinfo",
    "issuer": "http://localhost:8082/realms/kkrealm",
    "redirect_uris": ["http://localhost:5000/auth"]
  }
}
This file will be used in `apisso.py` File for Token Generation and following steps are for that
```
# Execute Python Code 
- apisso.py - This python process uses GET/POST - OAUTH Porocess
```
python apisso.py
```
And Use Following Postman Activities to Get You `access_token` and User Access by passing this token as `Bearer` Token see examples down

### Generate Oauth Token -Access/Refresh Token
```
curl --location 'http://localhost:8082/realms/kkrealm/protocol/openid-connect/token' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'client_id=flask-client' \
--data-urlencode 'client_secret=mRnGIkCPwXgvRXVMLL6qj5N5JmWaGqPI' \
--data-urlencode 'username=kout' \
--data-urlencode 'password=kout' \
--data-urlencode 'grant_type=password' \
--data-urlencode 'scope=openid email profile'
```
### Response
```
{
    "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJhMWxNRU5PMWRQM0F6Q0RVME56Zm5SM0ZvcUhDSW1JX1VDNzgwa0R4Q3BZIn0.eyJleHAiOjE3NTMzNTEzMzAsImlhdCI6MTc1MzM1MTAzMCwianRpIjoiYWU3OGIwNGYtOTlmOS00MTUyLWI4ODQtNDc5ZjMwMGVlZTQwIiwiaXNzIjoiaHR0cDovL2xvY2FsaG9zdDo4MDgyL3JlYWxtcy9ra3JlYWxtIiwiYXVkIjoiYWNjb3VudCIsInN1YiI6IjhiMzI5NjZjLWMxZGEtNGE1OC1hNmQzLWU2M2ZlZDZkZjM1OCIsInR5cCI6IkJlYXJlciIsImF6cCI6ImZsYXNrLWNsaWVudCIsInNlc3Npb25fc3RhdGUiOiJmNjRmNDFiMy1kNmE5LTRkOTItODFkMC1jYjIzYTgxYzA3MmQiLCJhY3IiOiIxIiwiYWxsb3dlZC1vcmlnaW5zIjpbImh0dHA6Ly9sb2NhbGhvc3Q6NTAwMCJdLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsiZGVmYXVsdC1yb2xlcy1ra3JlYWxtIiwib2ZmbGluZV9hY2Nlc3MiLCJ1bWFfYXV0aG9yaXphdGlvbiJdfSwicmVzb3VyY2VfYWNjZXNzIjp7ImFjY291bnQiOnsicm9sZXMiOlsibWFuYWdlLWFjY291bnQiLCJtYW5hZ2UtYWNjb3VudC1saW5rcyIsInZpZXctcHJvZmlsZSJdfX0sInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJzaWQiOiJmNjRmNDFiMy1kNmE5LTRkOTItODFkMC1jYjIzYTgxYzA3MmQiLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsInByZWZlcnJlZF91c2VybmFtZSI6ImtvdXQifQ.koxVRfafd3fKPqQC9C7eNmpKgMyBUkqJfPlEin5gzbCwq57JaEP-JbiuMlRbnPiQbkqXuZcnK8i3J--Xvkei0UiQEoDSjOOesgsLbvEsrujdCAaqH74Bw9OAvA7QIAsTlXshVPrUeRtBimGz4zm5uxyNZ5ZXWlegsOBQV9NyzyudPPwQk6vNBs_ZqUCLJrr0PLQUNqneoPvDNHkZpFFkzyWgQ1sDO9bT-AxFu0K3uW9wkMY097dXkYce7eVbAboE6pOLYaGKx6XSNn-4W3S0vIoP1EZ7rBa5hFKlz_8W2UiZ-lfCvept2Qv6k_70QiRGK_tCbvn6WatIjC0dFz_fdg",
    "expires_in": 300,
    "refresh_expires_in": 1800,
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICI0ZmUyMTdhYi05YTVlLTRhMWYtOWI3OC0xMTQ2MjA5ZGVhYzcifQ.eyJleHAiOjE3NTMzNTI4MzAsImlhdCI6MTc1MzM1MTAzMCwianRpIjoiMWRkYmQzYjctZDc1NS00ZmE5LWExNzAtMGY0MmYxMjFjMzcwIiwiaXNzIjoiaHR0cDovL2xvY2FsaG9zdDo4MDgyL3JlYWxtcy9ra3JlYWxtIiwiYXVkIjoiaHR0cDovL2xvY2FsaG9zdDo4MDgyL3JlYWxtcy9ra3JlYWxtIiwic3ViIjoiOGIzMjk2NmMtYzFkYS00YTU4LWE2ZDMtZTYzZmVkNmRmMzU4IiwidHlwIjoiUmVmcmVzaCIsImF6cCI6ImZsYXNrLWNsaWVudCIsInNlc3Npb25fc3RhdGUiOiJmNjRmNDFiMy1kNmE5LTRkOTItODFkMC1jYjIzYTgxYzA3MmQiLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwic2lkIjoiZjY0ZjQxYjMtZDZhOS00ZDkyLTgxZDAtY2IyM2E4MWMwNzJkIn0.cScaJfo5K6bk_5-hGopReAo90KF-HKe1o7_ctdXYO_Y",
    "token_type": "Bearer",
    "id_token": "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJhMWxNRU5PMWRQM0F6Q0RVME56Zm5SM0ZvcUhDSW1JX1VDNzgwa0R4Q3BZIn0.eyJleHAiOjE3NTMzNTEzMzAsImlhdCI6MTc1MzM1MTAzMCwiYXV0aF90aW1lIjowLCJqdGkiOiIzODYwOTNkZS0zYzI5LTQ0ODQtYTNhZC01MDFjODg3ODU4MjgiLCJpc3MiOiJodHRwOi8vbG9jYWxob3N0OjgwODIvcmVhbG1zL2trcmVhbG0iLCJhdWQiOiJmbGFzay1jbGllbnQiLCJzdWIiOiI4YjMyOTY2Yy1jMWRhLTRhNTgtYTZkMy1lNjNmZWQ2ZGYzNTgiLCJ0eXAiOiJJRCIsImF6cCI6ImZsYXNrLWNsaWVudCIsInNlc3Npb25fc3RhdGUiOiJmNjRmNDFiMy1kNmE5LTRkOTItODFkMC1jYjIzYTgxYzA3MmQiLCJhdF9oYXNoIjoicU11eXRnZDd6WENiZWdONE5ZYjEzQSIsImFjciI6IjEiLCJzaWQiOiJmNjRmNDFiMy1kNmE5LTRkOTItODFkMC1jYjIzYTgxYzA3MmQiLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsInByZWZlcnJlZF91c2VybmFtZSI6ImtvdXQifQ.faxZlQpwgs-lXZXivTv9gsOGc-yYOY03E_ZfiZAXe5AOYugw2aAedv8sfkf0hUVv6cvWVTUh0wUKdydrdAfUflZilVNwDF_-YmZhl6hMYzKKluKCuUCP0VQIp5VoOy6ahStsedlZ17vA5G2CSyTh6dXq-TqrerCjSDdux70CYx_fWHuuRrY-P7ZUY-gMJ67_T6PdoIExPbb2zPp6PodjxJH4ewpuQuk88yyoVOSJVNZX_aDWOI3RrmyH69JemU_CasD-YY9lHSYngjq0vM27oSAXgOYEgp8T02fi4HLcKUbls8koqc2p2i-c4YzHiliudTo1ZNazFKrHiGBrGTkvkQ",
    "not-before-policy": 0,
    "session_state": "f64f41b3-d6a9-4d92-81d0-cb23a81c072d",
    "scope": "openid profile email"
}
```

### Use Access Token To Get Authorised and Access To The Target Server
```
curl --location 'http://localhost:5000/private' \
--header 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJhMWxNRU5PMWRQM0F6Q0RVME56Zm5SM0ZvcUhDSW1JX1VDNzgwa0R4Q3BZIn0.eyJleHAiOjE3NTMzNDUxOTcsImlhdCI6MTc1MzM0NDg5NywianRpIjoiMzcyNDFlMDQtOTc0Ny00MzZmLTg0MGQtOGIzMWUxNjFjMWFhIiwiaXNzIjoiaHR0cDovL2xvY2FsaG9zdDo4MDgyL3JlYWxtcy9ra3JlYWxtIiwiYXVkIjoiYWNjb3VudCIsInN1YiI6IjEwMDZmNzM0LTIxN2UtNGMzOC04MTA5LTI0ZTYyZWEwZTNmYiIsInR5cCI6IkJlYXJlciIsImF6cCI6ImZsYXNrLWNsaWVudCIsInNlc3Npb25fc3RhdGUiOiI5YzNmYzc3Ni0wOTIzLTRjZDctOTFmMC1lMjFlYjE3YWE3ZDgiLCJhY3IiOiIxIiwiYWxsb3dlZC1vcmlnaW5zIjpbImh0dHA6Ly9sb2NhbGhvc3Q6NTAwMCJdLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsiZGVmYXVsdC1yb2xlcy1ra3JlYWxtIiwib2ZmbGluZV9hY2Nlc3MiLCJ1bWFfYXV0aG9yaXphdGlvbiJdfSwicmVzb3VyY2VfYWNjZXNzIjp7ImFjY291bnQiOnsicm9sZXMiOlsibWFuYWdlLWFjY291bnQiLCJtYW5hZ2UtYWNjb3VudC1saW5rcyIsInZpZXctcHJvZmlsZSJdfX0sInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJzaWQiOiI5YzNmYzc3Ni0wOTIzLTRjZDctOTFmMC1lMjFlYjE3YWE3ZDgiLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsInByZWZlcnJlZF91c2VybmFtZSI6ImtwYW50In0.HlcY2dvk5kKv-Y8E3KLWSsSUTbJNIIkxE9y9Z5ym-YWJiwk3L8HVCOEnewbyjIlU9dNSP8Xb0FPQut6EXZHKr0tpTEY7Ef-SPUZBTEP4SB1IgNfbFEyGOEdneIUfLyvfH9HkX8BO4cAmc135kTAIq94TXTijWbieLU8hfd7SFpesaOpChwpjT3x3CNArVx5h5rbAko6TL3__1TUxZ_IybXcuCiLRvo2Pg8ih1tKgrf5ZxBrTL1B3A0sjLvbeljZECKobUuUBslyGeKb8uDBFnCnrDXMp4nPeiuR6jJF6S3Xi022eB2W-BkgxoC8RHzRtz04pMhhG6acAY3iZcWdS6w' \
--data ''
```
### Response
```
{
    "message": "Welcome! You are authenticated via SSO."
}
```
# Python Code
- loginsso.py - This Python Code enables SSO for web based applications
```
python loginsso.py 
```
# Open http://localhost:5000/login
On Successful Login Screen with appear as per this 
![Web Screen](https://github.com/kkpant75/oauth_keycloak_ldap/blob/master/Images/loginSuccess.png)
```
Hello Kpant
```