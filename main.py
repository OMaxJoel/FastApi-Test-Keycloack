from fastapi import FastAPI
import requests
import uvicorn

app = FastAPI()

# Informations de configuration pour Keycloak
keycloak_base_url = "http://10.10.140.79:8080/"
client_id = "test"
client_secret = "PgBkocPcPw7MhFdk3H98atACIBf1FlXQ"
username = "max"
password = "12345"
realm1_name = "realm1"
realm2_name = "realm2"

# Fonction pour obtenir le jeton d'accès à partir de Keycloak
def get_access_token(realm_name):
    token_url = f"{keycloak_base_url}/realms/{realm_name}/protocol/openid-connect/token"
    payload = {
        "client_id": client_id,
        "client_secret": client_secret,
        "username": username,
        "password": password,
        "grant_type": "password"
    }
    response = requests.post(token_url, data=payload)
    return response.json().get("access_token")

# Fonction pour effectuer une requête protégée avec un jeton d'accès
def perform_protected_request(realm_name, access_token):
    api_url = f"{keycloak_base_url}/realms/{realm_name}/protocol/openid-connect/userinfo"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(api_url, headers=headers)
    return response.json()

# Routes API
@app.get("/test-realms")
async def test_user_access_to_realms():
    access_token_realm1 = get_access_token(realm1_name)
    access_token_realm2 = get_access_token(realm2_name)

    # Vérifier l'accès à la première realm
    response_realm1 = perform_protected_request(realm1_name, access_token_realm1)

    # Vérifier l'accès à la deuxième realm
    response_realm2 = perform_protected_request(realm2_name, access_token_realm2)

    return {"realm1_access": response_realm1, "realm2_access": response_realm2}
