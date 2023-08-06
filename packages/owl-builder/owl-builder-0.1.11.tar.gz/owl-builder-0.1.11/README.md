# Ontology Builder (owl-builder)

##

## Key Term Extraction
```python
from owl_builder import keyterms

input_text = """
A local area network (LAN) is a computer network that interconnects computers within a limited area such as a residence, school, laboratory, university campus or office building.

By contrast, a wide area network (WAN) not only covers a larger geographic distance, but also generally involves leased telecommunication circuits.

Ethernet and Wi-Fi are the two most common technologies in use for local area networks.

Historical network technologies include ARCNET, Token Ring, and AppleTalk.
"""

results = keyterms(
    input_text=input_text,
    use_terms=True,
    use_keyterms=True,
    use_ngrams=False,
    use_nounchunks=False)
```

The results are
```json
[
   "leased telecommunication circuit",
   "historical network technology",
   "large geographic distance",
   "interconnects computer",
   "local area network",
   "university campus",
   "common technology",
   "wide area network",
   "computer network",
   "office building",
   "include arcnet",
   "limited area",
   "token ring"
]
```