import azure.functions as func
import logging
import json
import msal
import requests
import os

app = func.FunctionApp()

@app.route(route="UpdateSharePoint", auth_level=func.AuthLevel.FUNCTION)
def UpdateSharePoint(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('SharePoint Agent triggad.')

    # Hämta konfiguration från miljövariabler (funkar både lokalt och i Azure)
    CLIENT_ID = os.environ.get("SP_CLIENT_ID")
    CLIENT_SECRET = os.environ.get("SP_CLIENT_SECRET")
    TENANT_ID = os.environ.get("SP_TENANT_ID")
    SITE_ID = os.environ.get("SP_SITE_ID")
    
    if not all([CLIENT_ID, CLIENT_SECRET, TENANT_ID, SITE_ID]):
        return func.HttpResponse("Server Configuration Error: Missing environment variables.", status_code=500)

    AUTHORITY_URL = f"https://login.microsoftonline.com/{TENANT_ID}"

    try:
        # 1. Hämta data (Här förbereder vi för GitHub Webhook payload)
        req_body = req.get_json()
        # Fallback om vi testar manuellt och inte skickar full payload
        message = req_body.get('head_commit', {}).get('message', 'Manuell testkörning')
    except ValueError:
        message = "Ingen data mottagen"

    # 2. MSAL Auth logic...
    # (Här lägger du in auth-koden från tidigare exempel)
    
    return func.HttpResponse(f"Agent körd. Meddelande: {message}", status_code=200)