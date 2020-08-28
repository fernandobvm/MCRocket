import zipfile
import os
import math
import shutil
import subprocess
import numpy as np
import pandas as pd
import statistics as s
from datetime import datetime
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import xml.etree.ElementTree as ET

def unzip_rocket(file_path):
    path = os.path.dirname(file_path)
    #path = "D:/Documentos/lib/UnB/4Semestre/Capital/ORSimulations"
    try:
        os.remove(path+'/rocket.ork')
        print("Arquivo pré-existente removido!")
    except FileNotFoundError:
        a = 0#print("Iniciando a descompactação do arquivo!")

    unzip = zipfile.ZipFile(file_path)
    unzip.extractall(path)
    unzip.close()
    print("Arquivo extraído com sucesso!")

def rename_rocket(name, new_name):
    os.rename(name,new_name)

def ListConversor(string,delimeter):
    li = list(string.split(delimeter))
    return li