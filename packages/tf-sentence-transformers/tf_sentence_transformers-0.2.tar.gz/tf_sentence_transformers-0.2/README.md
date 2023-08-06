# tf-sentence-transformers

A simple tensorflow/keras wrapper around `sentence-transformers`. The main class is `SentenceTransformer`, a `keras.Layer` that can be constructed from a pretrained checkpoint in huggingface model hub.

Example usage:

```
from tf_sentence_transformers import SentenceTransformer

layer = SentenceTransformer.from_pretrained(
    "sentence-transformers/all-MiniLM-L6-v2"
)
inputs = [
    ["This is a test sentence."],
    ["This is another test sentence."],
]
embedding = layer(inputs)
# assert embedding.shape == (2, 384)
```
