"""Task processing logic for the ClickUp Codegen Agent."""

import logging
import time
from typing import Dict, Any, List, Optional
from datetime import datetime

from .models import CodegenTaskRequest, CodegenTaskResponse, TaskStatus
from .ai_providers import AIProvider

logger = logging.getLogger(__name__)


class TaskProcessor:
    """Processes codegen tasks using AI providers."""
    
    def __init__(self, ai_provider: AIProvider):
        self.ai_provider = ai_provider
    
    async def process_task(self, request: CodegenTaskRequest) -> CodegenTaskResponse:
        """Process a codegen task request."""
        start_time = time.time()
        
        try:
            logger.info(f"Processing task: {request.title}")
            
            # Analyze requirements first
            analysis = await self.ai_provider.analyze_requirements(request.description)
            logger.debug(f"Requirements analysis: {analysis}")
            
            # Build context for code generation
            context = self._build_context(request, analysis)
            
            # Generate code
            prompt = self._build_prompt(request, analysis)
            generated_code = await self.ai_provider.generate_code(prompt, context)
            
            # Review the generated code
            review = await self.ai_provider.review_code(generated_code, request.description)
            
            # Create file changes
            file_changes = self._create_file_changes(generated_code, analysis, request)
            
            # Generate explanation
            explanation = self._generate_explanation(request, analysis, generated_code)
            
            # Extract suggestions from review
            suggestions = review.get("suggestions", [])
            
            # Check for errors
            errors = []
            if not review.get("meets_requirements", True):
                errors.append("Generated code may not fully meet requirements")
            
            if review.get("security_concerns"):
                errors.extend([f"Security: {concern}" for concern in review["security_concerns"]])
            
            execution_time = time.time() - start_time
            
            return CodegenTaskResponse(
                task_id=request.task_id,
                status=TaskStatus.COMPLETED if not errors else TaskStatus.FAILED,
                generated_code=generated_code,
                file_changes=file_changes,
                explanation=explanation,
                suggestions=suggestions,
                errors=errors,
                execution_time=execution_time
            )
            
        except Exception as e:
            logger.error(f"Task processing failed: {e}")
            execution_time = time.time() - start_time
            
            return CodegenTaskResponse(
                task_id=request.task_id,
                status=TaskStatus.FAILED,
                errors=[str(e)],
                execution_time=execution_time
            )
    
    def _build_context(self, request: CodegenTaskRequest, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Build context for code generation."""
        context = {
            "task_title": request.title,
            "requirements": request.requirements,
            "priority": request.priority.value,
        }
        
        # Add language and framework info
        if request.programming_language or analysis.get("programming_language"):
            context["programming_language"] = request.programming_language or analysis["programming_language"]
        
        if request.framework or analysis.get("framework"):
            context["framework"] = request.framework or analysis["framework"]
        
        # Add analysis results
        if analysis.get("architecture_pattern"):
            context["architecture_pattern"] = analysis["architecture_pattern"]
        
        if analysis.get("dependencies"):
            context["dependencies"] = analysis["dependencies"]
        
        # Add any existing context
        context.update(request.context)
        
        return context
    
    def _build_prompt(self, request: CodegenTaskRequest, analysis: Dict[str, Any]) -> str:
        """Build the prompt for code generation."""
        prompt_parts = [
            f"Task: {request.title}",
            f"Description: {request.description}",
        ]
        
        if request.requirements:
            prompt_parts.append("Requirements:")
            for i, req in enumerate(request.requirements, 1):
                prompt_parts.append(f"{i}. {req}")
        
        if analysis.get("programming_language"):
            prompt_parts.append(f"Programming Language: {analysis['programming_language']}")
        
        if analysis.get("framework"):
            prompt_parts.append(f"Framework: {analysis['framework']}")
        
        if analysis.get("architecture_pattern"):
            prompt_parts.append(f"Architecture Pattern: {analysis['architecture_pattern']}")
        
        if request.file_paths:
            prompt_parts.append(f"Target Files: {', '.join(request.file_paths)}")
        
        # Add specific instructions based on complexity
        complexity = analysis.get("complexity", "medium")
        if complexity == "high":
            prompt_parts.append("\nPlease provide a comprehensive solution with proper error handling, logging, and documentation.")
        elif complexity == "low":
            prompt_parts.append("\nPlease provide a simple, clean solution.")
        else:
            prompt_parts.append("\nPlease provide a well-structured solution with appropriate error handling.")
        
        # Add priority-based instructions
        if request.priority.value == "urgent":
            prompt_parts.append("This is an urgent task - focus on functionality over optimization.")
        elif request.priority.value == "high":
            prompt_parts.append("This is a high-priority task - ensure quality and performance.")
        
        return "\n\n".join(prompt_parts)
    
    def _create_file_changes(self, generated_code: str, analysis: Dict[str, Any], request: CodegenTaskRequest) -> List[Dict[str, str]]:
        """Create file changes from generated code."""
        file_changes = []
        
        # Determine file extension
        language = analysis.get("programming_language") or request.programming_language
        extension_map = {
            "python": ".py",
            "javascript": ".js",
            "typescript": ".ts",
            "java": ".java",
            "go": ".go",
            "rust": ".rs",
            "c++": ".cpp",
            "c": ".c",
            "php": ".php",
            "ruby": ".rb",
            "swift": ".swift",
            "kotlin": ".kt"
        }
        
        extension = extension_map.get(language, ".txt")
        
        # If specific file paths are provided, use them
        if request.file_paths:
            for file_path in request.file_paths:
                file_changes.append({
                    "filename": file_path,
                    "content": generated_code,
                    "action": "create_or_update"
                })
        else:
            # Generate filename based on task title
            filename = self._sanitize_filename(request.title) + extension
            file_changes.append({
                "filename": filename,
                "content": generated_code,
                "action": "create"
            })
        
        return file_changes
    
    def _sanitize_filename(self, title: str) -> str:
        """Sanitize a title to create a valid filename."""
        import re
        # Remove special characters and replace spaces with underscores
        sanitized = re.sub(r'[^\w\s-]', '', title)
        sanitized = re.sub(r'[-\s]+', '_', sanitized)
        return sanitized.lower()
    
    def _generate_explanation(self, request: CodegenTaskRequest, analysis: Dict[str, Any], generated_code: str) -> str:
        """Generate an explanation of the solution."""
        explanation_parts = [
            f"Generated solution for: {request.title}",
            "",
            "**Overview:**"
        ]
        
        if analysis.get("key_features"):
            explanation_parts.append("This solution implements the following key features:")
            for feature in analysis["key_features"]:
                explanation_parts.append(f"• {feature}")
            explanation_parts.append("")
        
        if analysis.get("programming_language"):
            explanation_parts.append(f"**Language:** {analysis['programming_language'].title()}")
        
        if analysis.get("framework"):
            explanation_parts.append(f"**Framework:** {analysis['framework'].title()}")
        
        if analysis.get("architecture_pattern"):
            explanation_parts.append(f"**Architecture:** {analysis['architecture_pattern']}")
        
        if analysis.get("dependencies"):
            explanation_parts.append("")
            explanation_parts.append("**Dependencies:**")
            for dep in analysis["dependencies"]:
                explanation_parts.append(f"• {dep}")
        
        # Add code structure explanation
        explanation_parts.extend([
            "",
            "**Code Structure:**",
            "The generated code follows best practices and includes:"
        ])
        
        # Analyze code structure
        if "class " in generated_code:
            explanation_parts.append("• Object-oriented design with classes")
        if "def " in generated_code or "function " in generated_code:
            explanation_parts.append("• Modular functions for better organization")
        if "try:" in generated_code or "catch" in generated_code:
            explanation_parts.append("• Error handling and exception management")
        if "import " in generated_code or "#include" in generated_code:
            explanation_parts.append("• Proper dependency imports")
        if "test" in generated_code.lower():
            explanation_parts.append("• Unit tests for validation")
        
        return "\n".join(explanation_parts)
