import grpc
from concurrent import futures
import time
import fed_grpc_pb2
import fed_grpc_pb2_grpc
from phe import paillier


class HomomorphicEncryption:
    def __init__(self):
        # Generate Paillier key pair
        self.public_key, self.private_key = paillier.generate_paillier_keypair()

    def decrypt(self, encrypted_message_str):
        # Decrypt message
        ciphertext = paillier.EncryptedNumber(self.public_key, int(encrypted_message_str))
        return self.private_key.decrypt(ciphertext)


class FederatedServiceServicer(fed_grpc_pb2_grpc.FederatedServiceServicer):
    def __init__(self):
        self.he = HomomorphicEncryption()

    def sendEncryptedData(self, request, context):
        encrypted_data_str = request.encryptedData.encrypted_data.decode('utf-8')
        print("Received encrypted data from client")

        # Decrypt data
        decrypted_data = self.he.decrypt(encrypted_data_str)
        print(f"Decrypted data: {decrypted_data}")

        return fed_grpc_pb2.Response(message="Data received and decrypted")


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    fed_grpc_pb2_grpc.add_FederatedServiceServicer_to_server(FederatedServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started at port 50051")
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == "__main__":
    serve()
