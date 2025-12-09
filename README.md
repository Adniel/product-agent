# Product AI Agent (MVP)

Detta projekt är en **AI-driven integrationsagent** byggd med **Azure Functions (Python)**. Syftet är att automatisera publicering av innehåll (nyheter, dokumentation, changelogs) till en SharePoint-produktsite baserat på händelser i externa system.

I denna första version (MVP) fungerar agenten som en brygga mellan **GitHub** och **SharePoint**. Vid en `git push` skapar agenten automatiskt ett utkast till en nyhetsartikel på en specifik SharePoint-site.

## Funktioner

  * **Trigger:** Lyssnar på HTTP-anrop (Webhooks) från GitHub.
  * **Autentisering:** Använder MSAL för säker inloggning mot Microsoft Graph via en Azure App Registration.
  * **Publicering:** Skapar moderna "News Pages" i SharePoint Online.
  * **Infrastruktur:** Serverless arkitektur via Azure Functions (V2 Model).

## Förutsättningar

För att köra detta projekt behöver du:

1.  **Azure Subscription** (för att hosta funktionen).
2.  **SharePoint Site** (som agenten ska publicera till).
3.  **Python 3.8+** installerat.
4.  **Azure Functions Core Tools** (`func`-kommandot).

## Installation & Lokal Setup

1.  **Klona repot:**

    ```bash
    git clone <din-repo-url>
    cd sharepoint-ai-agent
    ```

2.  **Skapa virtuell miljö (rekommenderas):**

    ```bash
    python -m venv .venv
    source .venv/bin/activate  # Mac/Linux
    # .venv\Scripts\activate   # Windows
    ```

3.  **Installera beroenden:**

    ```bash
    pip install -r requirements.txt
    ```

## Konfiguration (Azure AD & Environment)

För att agenten ska kunna prata med SharePoint måste du registrera en app i Azure AD.

1.  Skapa en **App Registration** i Azure Portal.
2.  Ge API Permission: `Sites.ReadWrite.All` (Type: *Application*) och bevilja **Admin Consent**.
3.  Skapa en **Client Secret**.

### Lokal konfigurationsfil

Skapa en fil som heter `local.settings.json` i roten av projektet. **OBS:** Denna fil ska *inte* versionshanteras (den är med i `.gitignore`).

Kopiera in följande och fyll i dina värden:

```json
{
  "IsEncrypted": false,
  "Values": {
    "AzureWebJobsStorage": "UseDevelopmentStorage=true",
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "SP_CLIENT_ID": "ditt-client-id-från-azure",
    "SP_CLIENT_SECRET": "din-client-secret",
    "SP_TENANT_ID": "ditt-tenant-id",
    "SP_SITE_ID": "ditt-sharepoint-site-id"
  }
}
```

*Tips: Site ID hämtas enklast via [Graph Explorer](https://developer.microsoft.com/en-us/graph/graph-explorer) med anropet `GET https://graph.microsoft.com/v1.0/sites/dindomän.sharepoint.com:/sites/dinsite`.*

## ▶️ Kör agenten lokalt

Starta funktionen med Core Tools:

```bash
func start
```

Funktionen kommer nu att lyssna på: `http://localhost:7071/api/UpdateSharePoint`

### Testa anrop

Du kan testa funktionen med `curl` eller Postman genom att skicka en POST-request som simulerar en GitHub-payload:

```bash
curl -X POST http://localhost:7071/api/UpdateSharePoint \
     -H "Content-Type: application/json" \
     -d '{"head_commit": {"message": "Testar SharePoint Agent", "author": {"name": "Dev"}}}'
```

Om allt fungerar ska du få tillbaka status 200 och se en ny sida skapad på din SharePoint-site.

## ☁️ Deployment

För att deploya till Azure:

1.  Skapa en Function App i Azure (Python).
2.  Lägg in variablerna från `local.settings.json` i Function Appens **Environment Variables** (Settings -\> Configuration).
3.  Deploya koden:
    ```bash
    func azure functionapp publish <namn-på-din-function-app>
    ```

-----

*Detta projekt är under utveckling. Nästa steg inkluderar integration med Azure OpenAI för innehållsgenerering.*

-----

### Nästa steg för dig

Kopiera texten ovan, skapa filen `README.md` i din mapp och spara.

**Vill du att jag visar hur du hittar ditt `SP_SITE_ID` via Graph Explorer?** Det är ofta det klurigaste steget i konfigurationen.

Hello Sharepoint Cloud!