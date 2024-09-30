import grpc
import fed_grpc_pb2
import fed_grpc_pb2_grpc
import threading
from concurrent import futures
import queue
import models as aux
import time
import sys
import json  # For reading the config file

class FedServer(fed_grpc_pb2_grpc.FederatedServiceServicer):
    def __init__(self):
        self.clients = {}
        self.round = 0
        self.avalable_for_register = True

    def sendChunk(self, request_iterator, context):
        for chunk in request_iterator:
            print(f"Received chunk of size: {len(chunk.data)} bytes")
        return fed_grpc_pb2.Response(message="All chunks received successfully.")

    def __sendRound(self):
        for cid in self.clients:
            channel = grpc.insecure_channel(self.clients[cid])
            client = fed_grpc_pb2_grpc.FederatedServiceStub(channel)
            client.sendRound(fed_grpc_pb2.currentRound(round=self.round))

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
            acc_list.append(client.modelValidation(fed_grpc_pb2.weightList(weight=aggregated_weights)).acc)
        return acc_list

    def __FedAvg(self, n_clients, weights_clients_list, sample_size_list):
        if not weights_clients_list or len(weights_clients_list) == 0:
            print("No weights received from clients.")
            return []
        aggregated_weights = []
        for j in range(len(weights_clients_list[0])):
            element = 0.0
            sample_sum = 0.0
            for i in range(n_clients):
                sample_sum += sample_size_list[i]
                element += weights_clients_list[i][j] * sample_size_list[i]
            aggregated_weights.append(element / sample_sum)
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
        while self.avalable_for_register == False:
            continue
        if cid in self.clients:
            print(f"Could not register Client with ID {cid} - Duplicated Id")
            return fed_grpc_pb2.registerOut(connectedClient=False, round=self.round)
        self.clients[cid] = ip + ":" + port
        print(f"Client {cid} registered!")
        return fed_grpc_pb2.registerOut(connectedClient=True, round=self.round)

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
    # Load config from JSON file
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)

    n_round_clients = config["n_round_clients"]
    min_clients = config["min_clients"]
    max_rounds = config["max_rounds"]
    acc_target = config["acc_target"]

    grpc_config = config["grpc_config"]
    ip_address = grpc_config["ip_address"]
    port = grpc_config["port"]
    max_receive_message_length = grpc_config["max_receive_message_length"]

    fed_server = FedServer()

    grpc_server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10),
        options=[
            ('grpc.max_receive_message_length', max_receive_message_length)
        ]
    )
    
    grpc_address = f'{ip_address}:{port}'
    fed_grpc_pb2_grpc.add_FederatedServiceServicer_to_server(fed_server, grpc_server)
    grpc_server.add_insecure_port(grpc_address)
    grpc_server.start()

    print(f"GRPC server is running on {grpc_address}")

    fed_server.startServer(n_round_clients, min_clients, max_rounds, acc_target)
    fed_server.killClients()