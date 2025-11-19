import sys
import os

# Adiciona o src ao PYTHONPATH para resolver imports relativos
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))