# server.py

from ciferai import get_eval_fn, set_initial_parameters, get_parameters, set_parameters, create_cifer_client
import torch
import torchvision
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

# Model and data setup
model = torchvision.models.resnet18(pretrained=False, num_classes=10)
trainloader = DataLoader(datasets.MNIST('.', train=True, download=True, transform=transforms.ToTensor()), batch_size=32, shuffle=True)
testloader = DataLoader(datasets.MNIST('.', train=False, transform=transforms.ToTensor()), batch_size=32, shuffle=False)

# Creating a client for cifer
cifer_client = create_cifer_client(model, trainloader, testloader)

# Testing the imported function usage
params = get_parameters(model)
print("Model parameters:", params)

# Assigning new parameters to the model
new_params = params  # Suppose you have new parameters to set
set_parameters(model, new_params)

# Calling the evaluation function
eval_fn = get_eval_fn(model, testloader)
loss, accuracy = eval_fn()
print(f"Loss: {loss}, Accuracy: {accuracy}")
