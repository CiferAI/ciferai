import grpc
import fed_grpc_pb2
import fed_grpc_pb2_grpc
from phe import paillier


class HomomorphicEncryption:
    def __init__(self):
        # Generate Paillier key pair
        self.public_key, self.private_key = paillier.generate_paillier_keypair()

    def encrypt(self, message):
        # Encrypt message
        return self.public_key.encrypt(message)

    def decrypt(self, ciphertext):
        # Decrypt message
        return self.private_key.decrypt(ciphertext)


def run():
    # Create channel and stub
    channel = grpc.insecure_channel('localhost:50051')
    stub = fed_grpc_pb2_grpc.FederatedServiceStub(channel)

    # Create Homomorphic object Encryption
    he = HomomorphicEncryption()

    # Plaintext message to be encrypted
    message = 42  # Sample message
    encrypted_message = he.encrypt(message)

    # Convert encrypted_message to string before sending to server
    encrypted_message_str = str(encrypted_message.ciphertext())

    print("Sending encrypted data to server")

    # Send encrypted data to the server
    response = stub.sendEncryptedData(fed_grpc_pb2.EncryptionArgs(
        encryptedData=fed_grpc_pb2.EncryptedData(encrypted_data=encrypted_message_str.encode('utf-8'))
    ))

    print(f"Response from server: {response.message}")


if __name__ == "__main__":
    run()
