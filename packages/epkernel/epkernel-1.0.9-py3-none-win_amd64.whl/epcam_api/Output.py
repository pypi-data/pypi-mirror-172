import os, sys, json
from epcam_api import epcam, BASE

def save_eps(job:str, path:str):
    BASE.setJobParameter(job, job)
    return BASE.save_eps(job, path)