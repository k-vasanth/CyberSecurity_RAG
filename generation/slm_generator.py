import ollama

class SLMGenerator:
    def __init__(self,model="qwen2.5:0.5b"):
        self.model = model

    def generate(self, query, context):
        prompt = f"""
You are a cybersecurity expert.

Rules:
1. Answer ONLY from the provided context.
2. Do NOT repeat yourself.
3. Keep the answer  concise and to the point.
4. Use only english language.
5. If the answer is not present in the context, reply exactly: "I don't have information about that."

CONTEXT:
{context}

QUESTION:
{query}

FINAL ANSWER:
"""
        
        response=ollama.chat(
            model=self.model,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return response['message']['content']


