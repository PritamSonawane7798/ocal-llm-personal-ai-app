import os
from glob import glob
from openai import OpenAI

class PersonalKnowledgeAssistant:
    def __init__(self, model="llama2", docs_directory="./documents"):
        self.model = model
        self.docs_directory = docs_directory
        self.knowledge_base = {}
        # Initialize OpenAI client with local Ollama server
        self.client = OpenAI(
            base_url="http://localhost:11434/v1/",
            api_key="ollama",  # can be anything as Ollama doesn't check API keys
        )
        self.load_documents()
        
    def load_documents(self):
        """Load and index documents from the specified directory."""
        for file_path in glob(f"{self.docs_directory}/**/*.txt", recursive=True):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                doc_name = os.path.basename(file_path)
                self.knowledge_base[doc_name] = content
        print(f"Loaded {len(self.knowledge_base)} documents into knowledge base.")
    
    def query(self, question, context_size=3):
        """Answer a question based on the knowledge base."""
        # Simple retrieval method - in a real app, you'd use embeddings or another retrieval method
        context = ""
        for doc_name, content in self.knowledge_base.items():
            # Add content to context with document reference
            context += f"\nFrom document '{doc_name}':\n{content[:1000]}...\n"
            if len(context) > 2000 * context_size:
                break
        
        system_prompt = f"""You are a personal knowledge assistant.
Use the following information to answer the user's question.
{context}

Answer based only on the information provided. If you don't know, say so."""
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ],
        )
        
        return response.choices[0].message.content

# Example usage
if __name__ == "__main__":
    assistant = PersonalKnowledgeAssistant()
    while True:
        question = input("\nAsk a question (or type 'exit' to quit): ")
        if question.lower() == 'exit':
            break
        answer = assistant.query(question)
        print("\nAnswer:", answer)