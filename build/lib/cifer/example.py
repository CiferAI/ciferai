import cifer
from cifer import fedlearn
print(cifer.__version__)
fedlearn.check_installation()
fedlearn.check_gpu_support()
fedlearn.check_tpu_support()


