import tiktoken

def count_tokens(text, model="gpt-4-1106-preview"):
    enc = tiktoken.encoding_for_model(model)
    return len(enc.encode(text))
    print()