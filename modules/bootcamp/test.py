import torch
print("CUDA available:", torch.cuda.is_available())

print("Number of GPUs:", torch.cuda.device_count())

test_tuple =(1,2,2)
(x, y, z) = test_tuple
print(x)