import urllib.request
import os
import gzip
from PIL import Image
import numpy as np
import random
import shutil
import sys

def deleteAllFolder(path):
    for file_name in os.listdir(path):
        file_path = os.path.join(path, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)

def downloadSaveData():
   
    train_data_url = 'http://yann.lecun.com/exdb/mnist/train-images-idx3-ubyte.gz'
    train_labels_url = 'http://yann.lecun.com/exdb/mnist/train-labels-idx1-ubyte.gz'

   
    train_data_file = 'train-images-idx3-ubyte.gz'
    train_labels_file = 'train-labels-idx1-ubyte.gz'

   
    data_dir = 'data'

   
    if os.path.exists(data_dir):
        deleteAllFolder(data_dir)
    else:
        
        os.makedirs(data_dir)

   
    urllib.request.urlretrieve(train_data_url, os.path.join(data_dir, train_data_file))
    urllib.request.urlretrieve(train_labels_url, os.path.join(data_dir, train_labels_file))

  
    with gzip.open(os.path.join(data_dir, train_data_file), 'rb') as f:
        train_images = np.frombuffer(f.read(), dtype=np.uint8, offset=16).reshape((-1, 28, 28))
    with gzip.open(os.path.join(data_dir, train_labels_file), 'rb') as f:
        train_labels = np.frombuffer(f.read(), dtype=np.uint8, offset=8)

   
    out_dir = 'data/images'

    for i, (img, label) in enumerate(zip(train_images, train_labels)):
        img = Image.fromarray(img, mode='L')
        label_dir = os.path.join(out_dir, str(label))
        os.makedirs(label_dir, exist_ok=True)
        os.makedirs(label_dir, exist_ok=True)
        img.save(os.path.join(label_dir, f'{i}.jpg'))

def split_data(input_dir, output_dir, n_clients):
   
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for label in range(10):
       
        file_names = os.listdir(input_dir+'/'+str(label))
        
       
        random.shuffle(file_names)
        
       
        num_files_per_partition = len(file_names) // n_clients
        
        for i in range(n_clients):
          
            start_index = i * num_files_per_partition
            end_index = start_index + num_files_per_partition
            
          
            if i == n_clients - 1:
                end_index = len(file_names)
            
            
            if label == 0:
                client_dir = os.path.join(output_dir, f'client_{i}')
                os.makedirs(client_dir, exist_ok=True)

            client_dir_label = os.path.join(output_dir, f'client_{i}/{label}')
            os.makedirs(client_dir_label, exist_ok=True)
            
            
            for file_name in file_names[start_index:end_index]:
                src_path = os.path.join(input_dir+'/'+str(label), file_name)
                dst_path = os.path.join(client_dir_label, file_name)
                shutil.copy(src_path, dst_path)

    deleteAllFolder(input_dir)

if __name__ == '__main__':
    try:
        n_clients = int(sys.argv[1])
    except IOError:
        print("Missing argument! Number of clients...")
        exit()

    downloadSaveData()
    split_data("data/images", "data", n_clients)