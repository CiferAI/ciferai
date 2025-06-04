import asyncio
import websockets
import json
import ssl
import numpy as np
import jwt
from cifer.training import train_custom_model
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64

SECRET_KEY = "your_jwt_secret_key"

class FederatedServer:
    def __init__(self, ip_address='127.0.0.1', port=8765, n_round_clients=3, use_homomorphic=False, use_secure=True, certfile='certificate.pem', keyfile='private_key.pem'):
        self.ip_address = ip_address
        self.port = port
        self.n_round_clients = n_round_clients
        self.use_homomorphic = use_homomorphic
        self.use_secure = use_secure
        self.connected_clients = set()
        self.model_weights_list = []

        # Create SSL context for WSS if secure is enabled
        if self.use_secure:
            self.ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            self.ssl_context.load_cert_chain(certfile=certfile, keyfile=keyfile)
        else:
            self.ssl_context = None

        if self.use_homomorphic:
            self.private_key = RSA.generate(3072)
            self.public_key = self.private_key.publickey()

    def decrypt_data(self, encrypted_data):
        cipher = PKCS1_OAEP.new(self.private_key)
        decrypted_data = [np.frombuffer(cipher.decrypt(base64.b64decode(d)), dtype=np.float32) for d in encrypted_data]
        return decrypted_data

    async def authenticate_client(self, websocket):
        token = await websocket.recv()
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            print(f"Authenticated user: {payload['user_id']}")
            return True
        except jwt.InvalidTokenError:
            print("Invalid token, closing connection.")
            await websocket.close()
            return False

    async def receive_message(self, websocket, path):
        # Authenticate client before allowing connection
        if not await self.authenticate_client(websocket):
            return

        self.connected_clients.add(websocket)

        if len(self.connected_clients) == self.n_round_clients:
            print("All clients connected. Ready to receive models.")
            for client in list(self.connected_clients):
                try:
                    if client.open:
                        await client.send(json.dumps({"status": "ready", "message": "Server is ready. Send your model."}))
                except websockets.exceptions.ConnectionClosedError:
                    print("A client disconnected before readiness notification.")
                    self.connected_clients.remove(client)

        try:
            async for message in websocket:
                data = json.loads(message)
                if data['type'] == 'request_public_key' and self.use_homomorphic:
                    await websocket.send(self.public_key.export_key().decode())
                elif data['type'] == 'send_model':
                    await self.handle_model_data(data, websocket)
        except websockets.exceptions.ConnectionClosedError as e:
            print(f"Connection closed unexpectedly: {e}")
        finally:
            self.connected_clients.remove(websocket)

    async def handle_model_data(self, data, websocket):
        try:
            if self.use_homomorphic:
                encrypted_weights = data['weights']
                model_weights = self.decrypt_data(encrypted_weights)
            else:
                model_weights = [np.array(w) for w in data['weights']]

            self.model_weights_list.append(model_weights)

            if len(self.model_weights_list) == self.n_round_clients:
                print("Aggregating model weights...")
                aggregated_weights = [np.mean([client_weights[i] for client_weights in self.model_weights_list], axis=0) 
                                      for i in range(len(self.model_weights_list[0]))]
                print("Aggregated model weights.")
                self.model_weights_list = []

                print("Training model on server...")
                # Example of training the model on the server
                x_train, y_train = np.random.rand(1000, 28, 28), np.random.randint(0, 10, 1000)
                train_custom_model(self.custom_model, x_train, y_train, epochs=10)

                for client in list(self.connected_clients):
                    try:
                        if client.open:
                            await client.send(json.dumps({
                                "status": "success",
                                "message": "Model aggregated and trained successfully"
                            }))
                    except websockets.exceptions.ConnectionClosedError:
                        print("A client disconnected during aggregation result sending.")
                        self.connected_clients.remove(client)
        except Exception as e:
            await websocket.send(json.dumps({
                "status": "error",
                "message": f"Failed to process model weights: {str(e)}"
            }))

    def set_custom_model(self, model):
        self.custom_model = model

    async def start_server(self):
        protocol = "wss" if self.use_secure else "ws"
        async with websockets.serve(self.receive_message, self.ip_address, self.port, ssl=self.ssl_context, max_size=None, max_queue=10):
            print(f"{protocol} server started on {protocol}://{self.ip_address}:{self.port}")
            await asyncio.Future()  # Run forever

def run_federated_server(ip_address='127.0.0.1', port=8765, n_round_clients=3, custom_model=None, use_homomorphic=False, use_secure=True, certfile='certificate.pem', keyfile='private_key.pem'):
    server = FederatedServer(ip_address, port, n_round_clients, use_homomorphic, use_secure, certfile, keyfile)
    server.set_custom_model(custom_model)
    asyncio.run(server.start_server())
