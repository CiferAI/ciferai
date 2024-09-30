import grpc
import fed_grpc_pb2
import fed_grpc_pb2_grpc
import threading
from concurrent import futures
import queue
import models as aux
import time
import sys
from phe import paillier  # Import Paillier for homomorphic encryption

class FedServer(fed_grpc_pb2_grpc.FederatedServiceServicer):
    def __init__(self):
        self.clients = {}
        self.round = 0
        self.avalable_for_register = True
        self.pub_key = None  # Store the public key from the client

    def __sendRound(self):
        for cid in self.clients:
            channel = grpc.insecure_channel(self.clients[cid])
            client = fed_grpc_pb2_grpc.FederatedServiceStub(channel)
            client.sendRound(fed_grpc_pb2.currentRound(round=(self.round)))

    def __callClientLearning(self, client_ip, q):
        channel = grpc.insecure_channel(client_ip)
        client = fed_grpc_pb2_grpc.FederatedServiceStub(channel)
        weight_list = client.startLearning(fed_grpc_pb2.void()).weight
        sample_size = client.getSampleSize(fed_grpc_pb2.void()).size
        q.put([weight_list, sample_size])

    def __callModelValidation(self, aggregated_weights):
        acc_list = []
        for cid in self.clients:
            channel = grpc.insecure_channel(self.clients[cid])
            client = fed_grpc_pb2_grpc.FederatedServiceStub(channel)
            acc_list.append(client.modelValidation(fed_grpc_pb2.weightList(weight=(aggregated_weights))).acc)
        return acc_list

    def __FedAvg(self, n_clients, weights_clients_list, sample_size_list):
        if not weights_clients_list or len(weights_clients_list) == 0:
            print("No weights received from clients.")
            return []

        aggregated_weights = []
        for j in range(len(weights_clients_list[0])):
            element = None
            sample_sum = 0.0
            for i in range(n_clients):
                sample_sum += sample_size_list[i]
                # Aggregate encrypted weights without decrypting
                if element is None:
                    element = paillier.EncryptedNumber(self.pub_key, int(weights_clients_list[i][j])) * sample_size_list[i]
                else:
                    element += paillier.EncryptedNumber(self.pub_key, int(weights_clients_list[i][j])) * sample_size_list[i]
            element /= sample_sum
            aggregated_weights.append(str(element.ciphertext()))

        return aggregated_weights

    def killClients(self):
        for cid in self.clients:
            channel = grpc.insecure_channel(self.clients[cid])
            client = fed_grpc_pb2_grpc.FederatedServiceStub(channel)
            client.killClient(fed_grpc_pb2.void())

    def clientRegister(self, request, context):
        ip = request.ip
        port = request.port
        cid = int(request.cid)
        pub_key = request.pub_key  # Receive public key from client
        if self.pub_key is None:
            self.pub_key = paillier.PaillierPublicKey(int(pub_key))

        while self.avalable_for_register == False:
            continue

        if cid in self.clients:
            print(f"Could not register Client with ID {cid} - Duplicated Id")
            return fed_grpc_pb2.registerOut(connectedClient=(False), round=(self.round))
        self.clients[cid] = ip + ":" + port
        print(f"Client {cid} registered!")
        return fed_grpc_pb2.registerOut(connectedClient=(True), round=(self.round))

    def startServer(self, n_round_clients, min_clients, max_rounds, acc_target):
        while self.round < max_rounds:
            if len(self.clients) < min_clients:
                print("Waiting for the minimum number of clients to connect...")
                while len(self.clients) < min_clients:
                    continue
                print("The minimum number of clients has been reached.")
            self.avalable_for_register = True
            time.sleep(0.5)
            self.round += 1
            self.avalable_for_register = False

            # Check if n_round_clients is greater than available clients
            if n_round_clients > len(self.clients):
                print(f"Reducing n_round_clients to {len(self.clients)} due to limited available clients.")
                n_round_clients = len(self.clients)

            self.__sendRound()
            cid_targets = aux.createRandomClientList(self.clients, n_round_clients)

            thread_list = []
            q = queue.Queue()
            for i in range(n_round_clients):
                thread = threading.Thread(target=self.__callClientLearning, args=(self.clients[cid_targets[i]], q))
                thread_list.append(thread)
                thread.start()
            for thread in thread_list:
                thread.join()

            weights_clients_list = []
            sample_size_list = []
            while not q.empty():
                thread_results = q.get()
                weights_clients_list.append(thread_results[0])
                sample_size_list.append(thread_results[1])

            aggregated_weights = self.__FedAvg(n_round_clients, weights_clients_list, sample_size_list)
            acc_list = self.__callModelValidation(aggregated_weights)
            if not acc_list:
                print("No accuracies to calculate the global accuracy.")
                return
            acc_global = sum(acc_list) / len(acc_list)
            print(f"Round: {self.round} / Accuracy Mean: {acc_global}")
            if acc_global >= acc_target:
                print("Accuracy Target has been achieved! Ending process")
                break

if __name__ == "__main__":
    try:
        n_round_clients = int(sys.argv[1])
        min_clients = int(sys.argv[2])
        max_rounds = int(sys.argv[3])
        acc_target = float(sys.argv[4])
    except IndexError:
        print("Missing argument! You need to pass: (clientsRound, minClients, maxRounds, accuracyTarget)")
        exit()
    fed_server = FedServer()
    grpc_server = grpc.server(futures.ThreadPoolExecutor(max_workers=10), options=[('grpc.max_receive_message_length', 1024 * 1024 * 1000)])  # 100 MB
    fed_grpc_pb2_grpc.add_FederatedServiceServicer_to_server(fed_server, grpc_server)
    grpc_server.add_insecure_port('[::]:8082')
    grpc_server.start()
    fed_server.startServer(n_round_clients, min_clients, max_rounds, acc_target)
    fed_server.killClients()
