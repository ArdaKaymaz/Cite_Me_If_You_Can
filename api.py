from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
import uuid
import numpy as np
from embedding import embed_text  # SPECTER2 function from embedding.py

app = FastAPI()

# Temporary vector db
vector_store = []