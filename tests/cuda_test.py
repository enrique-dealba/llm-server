import torch

"""
CUDA Debugging:
11.6 -- 11.6.r11.6

"""

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using {device}")

x = torch.rand(5, 5, device=device)
y = torch.rand(5, 5, device=device)
z = x + y
print(z)
