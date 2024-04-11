import ruclip
import warnings

warnings.filterwarnings("ignore", category=UserWarning)
#you can change device to "cpu", if it doesn't start like that
model, processor = ruclip.load("ruclip-vit-base-patch32-384")

import torch
import base64
import requests
# import matplotlib.pyplot as plt
from PIL import Image
import PIL
from io import BytesIO
import pandas as pd

import numpy as np
import torch

def softmax(image_latents, text_latents):
    """
    Calculate the similarity between image and text latents using softmax.

    Parameters:
        image_latents (torch.Tensor): Latent representations of images. Shape: (num_images, latent_dim)
        text_latents (torch.Tensor): Latent representations of texts. Shape: (num_texts, latent_dim)

    Returns:
        numpy.ndarray: Similarity scores between each image and text pair. Shape: (num_images, num_texts)
    """
    # Move tensors to CPU if they are on CUDA devices
    if image_latents.is_cuda:
        image_latents = image_latents.cpu()
    if text_latents.is_cuda:
        text_latents = text_latents.cpu()

    # Convert tensors to numpy arrays
    image_latents_np = image_latents.numpy()
    text_latents_np = text_latents.numpy()

    # Calculate dot product between image and text latents
    dot_product = np.dot(image_latents_np, text_latents_np.T)

    # Apply softmax function to the dot product
    softmax_scores = np.exp(dot_product) / np.sum(np.exp(dot_product), axis=1, keepdims=True)

    return softmax_scores


bs4_urls = requests.get('https://raw.githubusercontent.com/ai-forever/ru-dolph/master/pics/pipelines/cats_vs_dogs_bs4.json').json()

# bs4_urls = df['image'].tolist()
images = [Image.open(BytesIO(base64.b64decode(bs4_url))) for bs4_url in bs4_urls]

# prepare classes
# classes = df['name'].unique()
classes = ['одно животное', "много животных"]
templates = ['{}', 'это {}', 'на картинке {}']

# predict
#you can change device to "cpu", if it doesn't start like that
predictor = ruclip.Predictor(model, processor, 'cpu', bs=8, templates=templates)
with torch.no_grad():
    text_latents = predictor.get_text_latents(classes).cpu()
    pred_labels = predictor.run(images, text_latents)

    image_latents = predictor.get_image_latents(images).cpu()
    probs = softmax(image_latents, text_latents)