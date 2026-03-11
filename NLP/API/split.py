from deep_translator import GoogleTranslator

def chunk(text,max=5000):
    while len(text) > max:
        index = text.rfind(" " , 0 , max)
        if index == -1:
            index = max
        yield text[:index].strip()
        text = text[index:].strip()
    yield text.strip()

def long(text,source="en",target="id"):
    trans = GoogleTranslator(source=source , target=target)
    if isinstance(text,list):
        text = " ".join(map(str,text))

    
    chunks = list(chunk(text))
    return " ".join(trans.translate(c)for c in chunks if c)