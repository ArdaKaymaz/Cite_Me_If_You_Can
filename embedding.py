# -----------------------------------------
# 1) Importing Libraries
# -----------------------------------------

from transformers import AutoTokenizer
from adapters import AutoAdapterModel
import torch

# -----------------------------------------
# 2) Model & Adapter Configuration
# -----------------------------------------
TOKENIZER_NAME = "allenai/specter2_base"
ADAPTER_NAME = "allenai/specter2"

tokenizer = AutoTokenizer.from_pretrained(TOKENIZER_NAME)
model = AutoAdapterModel.from_pretrained(TOKENIZER_NAME)
model.load_adapter(ADAPTER_NAME, source="hf", set_active=True)
model.eval()

# -----------------------------------------
# 3) Embedding Function
# -----------------------------------------
def embed_text(text: str) -> list[float]:
    inputs = tokenizer(
        text,
        padding=True,
        truncation=True,
        return_tensors="pt",
        max_length=512
    )
    with torch.no_grad():
        output = model(**inputs)
        # [CLS] tokeni embedding'i
        embedding = output.last_hidden_state[:, 0, :]
    return embedding[0].tolist()

# -----------------------------------------
# 4) Unit Test
# -----------------------------------------
if __name__ == "__main__":
    sample = "CRISPR enables site-specific genome editing by leveraging bacterial immune mechanisms."
    vec = embed_text(sample)
    print("Embedding vector size:", len(vec))