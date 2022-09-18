import threading
from concurrent.futures import ThreadPoolExecutor
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

from intuitlib.client import AuthClient
from intuitlib.enums import Scopes


class Authenticator:
    # valid options: sandbox, production
    ENVIRONMENT = "production"
    REDIRECT_URI = "http://localhost:8000"
    HOST_NAME = "localhost"
    SOCKET_NUMBER = 8000

    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret

    class CallbackHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            url_components = parse_qs(urlparse(self.requestline).query)
            print(url_components)
            self.server.auth_code = url_components['code'][0]
            self.server.auth_client = AuthClient(
                client_id=self.server.client_id,
                client_secret=self.server.client_secret,
                redirect_uri=Authenticator.REDIRECT_URI,
                environment=Authenticator.ENVIRONMENT,
                state_token=url_components["state"][0],
                realm_id=url_components["realmId"][0]
            )

        def do_POST(self):
            self.do_GET()

    def authenticate(self) -> AuthClient:
        # get auth client
        auth_client = AuthClient(
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=self.REDIRECT_URI,
            environment=self.ENVIRONMENT
        )
        # get authorization url
        auth_url = auth_client.get_authorization_url([Scopes.ACCOUNTING])
        # launch server to listen for responses
        server_address = (self.HOST_NAME, self.SOCKET_NUMBER)
        server = HTTPServer(server_address=server_address, RequestHandlerClass=self.CallbackHandler)
        server.auth_client = None
        server.client_id = self.client_id
        server.client_secret = self.client_secret
        server_daemon = threading.Thread(target=server.serve_forever)
        server_daemon.daemon = True
        server_daemon.start()
        print(auth_url)
        while True:
            if server.auth_client is not None:
                break
        print(server.auth_client)
        try:
            server.auth_client.get_bearer_token(auth_code=server.auth_code, realm_id=server.auth_client.realm_id)
        except Exception as e:
            print(e)
            raise e
        return server.auth_client
