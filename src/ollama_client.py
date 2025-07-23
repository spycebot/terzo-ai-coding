import json
import requests
import asyncio
from typing import Dict, Optional, List

class OllamaClient:
    def __init__(self, base_url: str = "http://localhost:11434", 
                 model: str = "codellama:7b"):
        self.base_url = base_url
        self.model = model
        self.session = requests.Session()
        
    async def generate_response(self, prompt: str, 
                              temperature: float = 0.7,
                              max_tokens: int = 2000) -> str:
        """Generate response using Ollama"""
        
        url = f"{self.base_url}/api/generate"
        
        payload = {
            "model": self.model,
            "prompt": prompt,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": False
        }
        
        try:
            response = self.session.post(url, json=payload, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            return result.get("response", "")
            
        except requests.exceptions.RequestException as e:
            return f"Error communicating with Ollama: {str(e)}"
    
    async def stream_response(self, prompt: str) -> asyncio.Generator[str, None, None]:
        """Stream response from Ollama"""
        url = f"{self.base_url}/api/generate"
        
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": True
        }
        
        try:
            response = self.session.post(url, json=payload, stream=True)
            response.raise_for_status()
            
            for line in response.iter_lines():
                if line:
                    data = json.loads(line.decode('utf-8'))
                    if 'response' in data:
                        yield data['response']
                        
        except requests.exceptions.RequestException as e:
            yield f"Error: {str(e)}"
    
    def list_models(self) -> List[str]:
        """List available models"""
        try:
            response = self.session.get(f"{self.base_url}/api/tags")
            response.raise_for_status()
            
            models = response.json().get("models", [])
            return [model["name"] for model in models]
            
        except requests.exceptions.RequestException:
            return []
    
    def switch_model(self, model_name: str) -> bool:
        """Switch to a different model"""
        available_models = self.list_models()
        if model_name in available_models:
            self.model = model_name
            return True
        return False