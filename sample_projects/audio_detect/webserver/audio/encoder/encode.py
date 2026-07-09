import librosa
import panns_inference
from panns_inference import AudioTagging, SoundEventDetection, labels
from milvus import Milvus, DataType
import os
from audio.indexer.logs import write_log
import numpy as np
import torch


def get_audio_embedding(path):
    try:
        audio, _ = librosa.core.load(path, sr=32000, mono=True)
        audio = audio[None, :]
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        at = AudioTagging(checkpoint_path=None, device=device)
        _, embedding = at.inference(audio)
        embedding = embedding/np.linalg.norm(embedding)
        embedding = embedding.tolist()[0]
        return path, embedding
    except Exception as e:
        print("error with embedding:", path)
        write_log(e, 1)
        return path, None
