import asyncio
import argparse
from pathlib import Path
from assistant import AICodeAssistant, TaskType, CodeContext
from ollama_client import OllamaClient
from context_manager import ContextManager

class CLIInterface:
    def __init__(self):
        self.client = OllamaClient()
        self.context_manager = ContextManager()
        self.assistant = AICodeAssistant(self.client, self.context_manager)
        
    async def run(self):
        """Main CLI loop"""
        print("AI Coding Assistant CLI")
        print("Type 'help' for commands, 'quit' to exit")
        
        while True:
            try:
                command = input("\n> ").strip()
                
                if command.lower() in ['quit', 'exit']:
                    break
                elif command.lower() == 'help':
                    self.show_help()
                elif command.startswith('review'):
                    await self.handle_review(command)
                elif command.startswith('complete'):
                    await self.handle_completion(command)
                elif command.startswith('debug'):
                    await self.handle_debug(command)
                elif command.startswith('explain'):
                    await self.handle_explain(command)
                elif command.startswith('models'):
                    self.show_models()
                else:
                    await self.handle_general_query(command)
                    
            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except Exception as e:
                print(f"Error: {e}")
    
    def show_help(self):
        """Show help message"""
        help_text = """
Available commands:
  review <file>     - Review code in file
  complete <file>   - Code completion for file
  debug <file>      - Debug code in file
  explain <file>    - Explain code in file
  models            - List available models
  help              - Show this help
  quit/exit         - Exit the assistant
        """
        print(help_text)
    
    async def handle_review(self, command: str):
        """Handle code review command"""
        parts = command.split(' ', 1)
        if len(parts) < 2:
            print("Usage: review <file>")
            return
        
        file_path = parts[1]
        if not Path(file_path).exists():
            print(f"File not found: {file_path}")
            return
        
        content = self.context_manager.read_file(file_path)
        if not content:
            print(f"Could not read file: {file_path}")
            return
        
        context = CodeContext(
            file_path=file_path,
            content=content,
            language=self.context_manager._detect_language(file_path),
            cursor_position=0
        )
        
        print("Reviewing code...")
        result = await self.assistant.process_request(
            TaskType.CODE_REVIEW, context, "Please review this code"
        )
        
        print(f"\nCode Review Results:\n{result['response']}")
    
    async def handle_completion(self, command: str):
        """Handle code completion command"""
        parts = command.split(' ', 1)
        if len(parts) < 2:
            print("Usage: complete <file>")
            return
        
        file_path = parts[1]
        if not Path(file_path).exists():
            print(f"File not found: {file_path}")
            return
        
        content = self.context_manager.read_file(file_path)
        cursor_pos = len(content)  # Default to end of file
        
        context = CodeContext(
            file_path=file_path,
            content=content,
            language=self.context_manager._detect_language(file_path),
            cursor_position=cursor_pos
        )
        
        print("Generating completion...")
        result = await self.assistant.process_request(
            TaskType.CODE_COMPLETION, context, "Complete this code"
        )
        
        print(f"\nCompletion:\n{result.get('completion', result['response'])}")
    
    async def handle_debug(self, command: str):
        """Handle debugging command"""
        parts = command.split(' ', 1)
        if len(parts) < 2:
            print("Usage: debug <file>")
            return
        
        file_path = parts[1]
        if not Path(file_path).exists():
            print(f"File not found: {file_path}")
            return
        
        content = self.context_manager.read_file(file_path)
        
        context = CodeContext(
            file_path=file_path,
            content=content,
            language=self.context_manager._detect_language(file_path),
            cursor_position=0
        )
        
        print("Debugging code...")
        result = await self.assistant.process_request(
            TaskType.DEBUGGING, context, "Help debug this code"
        )
        
        print(f"\nDebugging Results:\n{result['response']}")
    
    async def handle_explain(self, command: str):
        """Handle code explanation command"""
        parts = command.split(' ', 1)
        if len(parts) < 2:
            print("Usage: explain <file>")
            return
        
        file_path = parts[1]
        if not Path(file_path).exists():
            print(f"File not found: {file_path}")
            return
        
        content = self.context_manager.read_file(file_path)
        
        context = CodeContext(
            file_path=file_path,
            content=content,
            language=self.context_manager._detect_language(file_path),
            cursor_position=0
        )
        
        print("Explaining code...")
        result = await self.assistant.process_request(
            TaskType.EXPLANATION, context, "Explain this code"
        )
        
        print(f"\nExplanation:\n{result['response']}")
    
    def show_models(self):
        """Show available models"""
        models = self.client.list_models()
        if models:
            print("Available models:")
            for model in models:
                print(f"  - {model}")
        else:
            print("No models available or Ollama not running")
    
    async def handle_general_query(self, query: str):
        """Handle general coding questions"""
        context = CodeContext(
            file_path="",
            content="",
            language="text",
            cursor_position=0
        )
        
        result = await self.assistant.process_request(
            TaskType.EXPLANATION, context, query
        )
        
        print(f"\nResponse:\n{result['response']}")

def main():
    parser = argparse.ArgumentParser(description="AI Coding Assistant")
    parser.add_argument("--model", default="codellama:7b", help="Ollama model to use")
    parser.add_argument("--project", default=".", help="Project root directory")
    
    args = parser.parse_args()
    
    cli = CLIInterface()
    cli.client.model = args.model
    cli.context_manager.project_root = Path(args.project)
    
    asyncio.run(cli.run())

if __name__ == "__main__":
    main()