import pymupdf as pydf

def extract_text_from_pdf(filepath: str) -> list[dict]:
    doc = pydf.open(filepath)
    results = []
    
    for page in doc:
        text = page.get_text()
        results.append({
            "page": page.number + 1,
            "text": text
        })
    return results

""" test extraction block
if __name__ == "__main__": 
    pages = extract_text_from_pdf("testdata\JD.pdf")
    for p in pages:
        print(f"Page {p['page']}: {len(p['text'])} characters")
"""

def chunk_text(text: str, page: int, filename: str) -> list[dict]:
    start = 0
    chunk_list = []
    chunk_index = 0
    while start < len(text):
        end = start + 512
        chunk_text = text[start:end] 
        chunk_list.append({
            "filename" : filename,
            "page" : page,
            "text" : chunk_text, 
            "chunk_index" : chunk_index        
        })
        start = start + 448 # Chunk size = 512, Overlapping = 64, next start = 512 - 64
        chunk_index += 1
    return chunk_list

def process_pdf(filepath: str) -> list[dict]:
    pages = extract_text_from_pdf(filepath)
    all_chunks = []  
    for page in pages:
        chunks = chunk_text(page["text"], page["page"], filepath)
        all_chunks.extend(chunks)
    return all_chunks

if __name__ == "__main__":
    chunks = process_pdf("testdata/JD.pdf")
    print(f"Total chunks: {len(chunks)}")
    print("Chunk 1: \n")
    print(chunks[0])
    print("Chunk 2: \n")
    print(chunks[1])