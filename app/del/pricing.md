https://openai.com/api/pricing/

https://cloud.google.com/vertex-ai/generative-ai/pricing

https://ai.google.dev/gemini-api/docs/get-started/python#use_embeddings


## Model versioning

https://cloud.google.com/vertex-ai/generative-ai/docs/learn/model-versioning#latest-version


# embed 

https://ai.google.dev/gemini-api/docs/get-started/python#use_embeddings

result = genai.embed_content(
    model="models/embedding-001",
    content=[
      'What is the meaning of life?',
      'How much wood would a woodchuck chuck?',
      'How does the brain work?'],
    task_type="retrieval_document",
    title="Embedding of list of strings")

# A list of inputs > A list of vectors output
for v in result['embedding']:
  print(str(v)[:50], '... TRIMMED ...')