import asyncio
import json
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum

class TaskType(Enum):
    CODE_COMPLETION = "code_completion"
    CODE_REVIEW = "code_review"
    DEBUGGING = "debugging"
    EXPLANATION = "explanation"
    REFACTORING = "refactoring"
    DOCUMENTATION = "documentation"

@dataclass
class CodeContext:
    file_path: str
    content: str
    language: str
    cursor_position: int
    selected_text: Optional[str] = None

class AICodeAssistant:
    def __init__(self, model_client, context_manager):
        self.model_client = model_client
        self.context_manager = context_manager
        self.conversation_history = []
        
    async def process_request(self, task_type: TaskType, context: CodeContext, 
                            user_input: str) -> Dict[str, Any]:
        """Main method to process coding assistance requests"""
        
        # Build context-aware prompt
        prompt = self._build_prompt(task_type, context, user_input)
        
        # Get response from AI model
        response = await self.model_client.generate_response(prompt)
        
        # Process and format response
        result = self._process_response(response, task_type, context)
        
        # Update conversation history
        self._update_history(user_input, result)
        
        return result
    
    def _build_prompt(self, task_type: TaskType, context: CodeContext, 
                     user_input: str) -> str:
        """Build context-aware prompts for different task types"""
        
        base_context = f"""
File: {context.file_path}
Language: {context.language}
Current code:
```{context.language}
{context.content}
"""
        if context.selected_text:
            base_context += f"\nSelected text: {context.selected_text}"
    
        prompt_templates = {
            TaskType.CODE_COMPLETION: f"""
{base_context}
Cursor position: {context.cursor_position}
Complete the code at the cursor position. Provide only the completion text.
User request: {user_input}
""",
TaskType.CODE_REVIEW: f"""
{base_context}
Please review this code for:

Potential bugs
Performance issues
Best practices
Code quality

User request: {user_input}
""",
TaskType.DEBUGGING: f"""
{base_context}
Help debug this code. Analyze for:

Syntax errors
Logic errors
Common pitfalls
Suggested fixes

User request: {user_input}
""",
TaskType.EXPLANATION: f"""
{base_context}
Explain this code in detail:

What it does
How it works
Key concepts used

User request: {user_input}
""",
TaskType.REFACTORING: f"""
{base_context}
Suggest refactoring improvements:

Code structure
Performance optimizations
Readability improvements
Design patterns

User request: {user_input}
""",
TaskType.DOCUMENTATION: f"""
{base_context}
Generate documentation for this code:

Function/class descriptions
Parameter explanations
Usage examples
Return value descriptions

User request: {user_input}
"""
}
        return prompt_templates.get(task_type, f"{base_context}\n{user_input}")

def _process_response(self, response: str, task_type: TaskType, 
                     context: CodeContext) -> Dict[str, Any]:
    """Process AI response based on task type"""
    
    result = {
        "task_type": task_type.value,
        "response": response,
        "context": context,
        "timestamp": asyncio.get_event_loop().time()
    }
    
    # Add task-specific processing
    if task_type == TaskType.CODE_COMPLETION:
        result["completion"] = self._extract_code_completion(response)
    elif task_type == TaskType.CODE_REVIEW:
        result["issues"] = self._extract_code_issues(response)
    elif task_type == TaskType.DEBUGGING:
        result["fixes"] = self._extract_debug_fixes(response)
    
    return result

def _extract_code_completion(self, response: str) -> str:
    """Extract code completion from response"""
    # Simple extraction - can be enhanced with regex
    lines = response.split('\n')
    code_lines = []
    in_code_block = False
    
    for line in lines:
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            code_lines.append(line)
    
    return '\n'.join(code_lines) if code_lines else response

def _extract_code_issues(self, response: str) -> List[Dict[str, str]]:
    """Extract code issues from review response"""
    # Enhanced parsing can be added here
    return [{"issue": response, "severity": "info"}]

def _extract_debug_fixes(self, response: str) -> List[Dict[str, str]]:
    """Extract debugging fixes from response"""
    return [{"fix": response, "confidence": "medium"}]

def _update_history(self, user_input: str, result: Dict[str, Any]):
    """Update conversation history"""
    self.conversation_history.append({
        "user_input": user_input,
        "assistant_response": result,
        "timestamp": result["timestamp"]
    })
    
    # Keep only last 10 interactions
    if len(self.conversation_history) > 10:
        self.conversation_history = self.conversation_history[-10:]