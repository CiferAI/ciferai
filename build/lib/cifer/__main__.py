import requests
from clint.textui import puts, colored, indent 
from pyfiglet import Figlet
import os
import re
import sys
from pprint import pprint
sys.path.append(os.path.realpath("."))
import inquirer  # noqa

result = Figlet(font='slant')
print(colored.blue(result.renderText("CIFER.AI") ))
print("Decentralized Machine Learning")

print("Building the Future of AI with Leading ML Frameworks and Libraries Accelerate Your AI Innovation with Cifer's Seamless Integration of TensorFlow, PyTorch, NumPy, and Jupyter Notebook ")


print("\n")


sys.path.append(os.path.realpath("."))
import inquirer  # noqa

main_menu = [
    inquirer.Checkbox(
        "Traning",
        message="Menu",
        choices=["Traning Data", "ML Algorithm", "New Data to pidic", "Download Model"],
        default=["Traning Data"],
    ),
]


answers = inquirer.prompt(main_menu)

pprint(answers)


