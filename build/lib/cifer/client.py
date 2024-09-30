import models as aux
import sys
import grpc
import fed_grpc_pb2_grpc
import fed_grpc_pb2
from sklearn.model_selection import train_test_split
from keras.utils import to_categorical
import os
import signal
from concurrent import futures


class FedClient(fed_grpc_pb2_grpc.FederatedServiceServicer):
    def __init__(self, cid, x_train, x_test, y_train, y_test, model, server_adress, client_ip):
        self.cid = cid
        self.x_train = x_train
        self.x_test = x_test
        self.y_train = y_train
        self.y_test = y_test
        self.model = model
        self.server_adress = server_adress
        self.client_ip = client_ip
    
    def __setClientChannel(self,client_channel):
        self.client_channel = client_channel

    
    def __waitingForServer(self,port):
        client_channel = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
        self.__setClientChannel(client_channel)
        fed_grpc_pb2_grpc.add_FederatedServiceServicer_to_server(self, client_channel)

        client_ip = self.client_ip + ':' + port

        client_channel.add_insecure_port(client_ip)
        client_channel.start()
        client_channel.wait_for_termination()

    
    def sendRound(self, request, context):
        ac_round = request.round
        print()
        print(f"Starting {ac_round} round")
        return fed_grpc_pb2.void()

    
    def startLearning(self, request, context):
        self.model.fit(self.x_train, self.y_train, epochs=1, verbose=2)

        weights_list = aux.setWeightSingleList(self.model.get_weights())

        return fed_grpc_pb2.weightList(weight = (weights_list))
    
 
    def getSampleSize(self, request, context):
        return fed_grpc_pb2.sampleSize(size = (len(self.x_train)))

   
    def modelValidation(self, request, context):
        server_weight = request.weight
        self.model.set_weights(aux.reshapeWeight(server_weight, self.model.get_weights()))
        accuracy = self.model.evaluate(self.x_test, self.y_test, verbose=0)[1]

        print(f"Local accuracy with global weights: {accuracy}")

        return fed_grpc_pb2.accuracy(acc = (accuracy))
    
 
    def killClient(self, request, context):
        print()
        print(f"Call for closing channel - Killing Client {self.cid}")
        self.client_channel.stop(0)

        return fed_grpc_pb2.void()
    
    def runClient(self):

        server_channel = grpc.insecure_channel(self.server_adress)
        client = fed_grpc_pb2_grpc.FederatedServiceStub(server_channel)


        port = self.server_adress.split(':')[1]
        port = str(30000 + int(self.cid))

        register_out = client.clientRegister(fed_grpc_pb2.registerArgs(ip=self.client_ip, port=port, cid=self.cid))

        if register_out.connectedClient:
            print(f"Client Connected at round {register_out.round}, waiting for server commands...")
            self.__waitingForServer(port)
        else:
            print("This client couldn't connect with the server")


if __name__ == '__main__':
    cid = -1
    input_shape = (28, 28, 1)
    num_classes = 10
    server_adress = 'localhost:8080'
    client_ip = '[::]'

    try:
        cid = sys.argv[1]
    except IndexError:
        print("Missing argument! You need to pass: ClientId")
        exit()


    x_train, y_train = aux.load_mnist_byCid(cid)
    x_train, x_test, y_train, y_test = train_test_split(x_train, y_train, test_size=0.2, random_state=42)

    y_train = to_categorical(y_train, num_classes)
    y_test = to_categorical(y_test, num_classes)

    model = aux.define_model(input_shape,num_classes)

    fed_client = FedClient(cid, x_train, x_test, y_train, y_test, model, server_adress, client_ip)
    fed_client.runClient()
