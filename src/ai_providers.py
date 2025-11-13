"""AI provider integrations for code generation."""

import logging
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List
import openai
import anthropic

from .config import settings

logger = logging.getLogger(__name__)


class AIProvider(ABC):
    """Abstract base class for AI providers."""
    
    @abstractmethod
    async def generate_code(self, prompt: str, context: Dict[str, Any] = None) -> str:
        """Generate code based on the given prompt and context."""
        pass
    
    @abstractmethod
    async def analyze_requirements(self, requirements: str) -> Dict[str, Any]:
        """Analyze requirements and extract structured information."""
        pass
    
    @abstractmethod
    async def review_code(self, code: str, requirements: str) -> Dict[str, Any]:
        """Review generated code against requirements."""
        pass


class OpenAIProvider(AIProvider):
    """OpenAI GPT provider for code generation."""
    
    def __init__(self, api_key: str = None, model: str = "gpt-4"):
        self.client = openai.AsyncOpenAI(api_key=api_key or settings.openai_api_key)
        self.model = model
    
    async def generate_code(self, prompt: str, context: Dict[str, Any] = None) -> str:
        """Generate code using OpenAI GPT."""
        try:
            system_prompt = self._build_system_prompt(context)
            
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=4000
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"OpenAI code generation failed: {e}")
            raise
    
    async def analyze_requirements(self, requirements: str) -> Dict[str, Any]:
        """Analyze requirements using OpenAI."""
        try:
            prompt = f"""
            Analyze the following requirements and extract structured information:
            
            Requirements: {requirements}
            
            Please provide a JSON response with the following structure:
            {{
                "programming_language": "detected language or null",
                "framework": "detected framework or null",
                "complexity": "low|medium|high",
                "estimated_time": "estimated time in hours",
                "key_features": ["list", "of", "features"],
                "dependencies": ["list", "of", "dependencies"],
                "file_types": ["list", "of", "file", "extensions"],
                "architecture_pattern": "detected pattern or null"
            }}
            """
            
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1
            )
            
            import json
            return json.loads(response.choices[0].message.content.strip())
            
        except Exception as e:
            logger.error(f"OpenAI requirements analysis failed: {e}")
            return {}
    
    async def review_code(self, code: str, requirements: str) -> Dict[str, Any]:
        """Review code using OpenAI."""
        try:
            prompt = f"""
            Review the following code against the requirements:
            
            Requirements: {requirements}
            
            Code:
            ```
            {code}
            ```
            
            Please provide a JSON response with:
            {{
                "quality_score": 0-100,
                "meets_requirements": true/false,
                "issues": ["list", "of", "issues"],
                "suggestions": ["list", "of", "improvements"],
                "security_concerns": ["list", "of", "security", "issues"],
                "performance_notes": ["list", "of", "performance", "observations"]
            }}
            """
            
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1
            )
            
            import json
            return json.loads(response.choices[0].message.content.strip())
            
        except Exception as e:
            logger.error(f"OpenAI code review failed: {e}")
            return {}
    
    def _build_system_prompt(self, context: Dict[str, Any] = None) -> str:
        """Build system prompt for code generation."""
        base_prompt = """
        You are an expert software engineer and code generator. Your task is to generate high-quality, 
        production-ready code based on the given requirements.
        
        Guidelines:
        - Write clean, readable, and well-documented code
        - Follow best practices and design patterns
        - Include proper error handling
        - Add meaningful comments where necessary
        - Ensure code is secure and performant
        - Use appropriate naming conventions
        - Include type hints where applicable
        """
        
        if context:
            if context.get("programming_language"):
                base_prompt += f"\n- Use {context['programming_language']} as the programming language"
            if context.get("framework"):
                base_prompt += f"\n- Use {context['framework']} framework"
            if context.get("existing_code"):
                base_prompt += f"\n- Consider existing codebase context: {context['existing_code']}"
        
        return base_prompt


class AnthropicProvider(AIProvider):
    """Anthropic Claude provider for code generation."""
    
    def __init__(self, api_key: str = None, model: str = "claude-3-sonnet-20240229"):
        self.client = anthropic.AsyncAnthropic(api_key=api_key or settings.anthropic_api_key)
        self.model = model
    
    async def generate_code(self, prompt: str, context: Dict[str, Any] = None) -> str:
        """Generate code using Anthropic Claude."""
        try:
            system_prompt = self._build_system_prompt(context)
            
            response = await self.client.messages.create(
                model=self.model,
                max_tokens=4000,
                temperature=0.1,
                system=system_prompt,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return response.content[0].text.strip()
            
        except Exception as e:
            logger.error(f"Anthropic code generation failed: {e}")
            raise
    
    async def analyze_requirements(self, requirements: str) -> Dict[str, Any]:
        """Analyze requirements using Anthropic Claude."""
        try:
            prompt = f"""
            Analyze the following requirements and extract structured information:
            
            Requirements: {requirements}
            
            Please provide a JSON response with the following structure:
            {{
                "programming_language": "detected language or null",
                "framework": "detected framework or null",
                "complexity": "low|medium|high",
                "estimated_time": "estimated time in hours",
                "key_features": ["list", "of", "features"],
                "dependencies": ["list", "of", "dependencies"],
                "file_types": ["list", "of", "file", "extensions"],
                "architecture_pattern": "detected pattern or null"
            }}
            """
            
            response = await self.client.messages.create(
                model=self.model,
                max_tokens=1000,
                temperature=0.1,
                messages=[{"role": "user", "content": prompt}]
            )
            
            import json
            return json.loads(response.content[0].text.strip())
            
        except Exception as e:
            logger.error(f"Anthropic requirements analysis failed: {e}")
            return {}
    
    async def review_code(self, code: str, requirements: str) -> Dict[str, Any]:
        """Review code using Anthropic Claude."""
        try:
            prompt = f"""
            Review the following code against the requirements:
            
            Requirements: {requirements}
            
            Code:
            ```
            {code}
            ```
            
            Please provide a JSON response with:
            {{
                "quality_score": 0-100,
                "meets_requirements": true/false,
                "issues": ["list", "of", "issues"],
                "suggestions": ["list", "of", "improvements"],
                "security_concerns": ["list", "of", "security", "issues"],
                "performance_notes": ["list", "of", "performance", "observations"]
            }}
            """
            
            response = await self.client.messages.create(
                model=self.model,
                max_tokens=1000,
                temperature=0.1,
                messages=[{"role": "user", "content": prompt}]
            )
            
            import json
            return json.loads(response.content[0].text.strip())
            
        except Exception as e:
            logger.error(f"Anthropic code review failed: {e}")
            return {}
    
    def _build_system_prompt(self, context: Dict[str, Any] = None) -> str:
        """Build system prompt for code generation."""
        base_prompt = """
        You are an expert software engineer and code generator. Your task is to generate high-quality, 
        production-ready code based on the given requirements.
        
        Guidelines:
        - Write clean, readable, and well-documented code
        - Follow best practices and design patterns
        - Include proper error handling
        - Add meaningful comments where necessary
        - Ensure code is secure and performant
        - Use appropriate naming conventions
        - Include type hints where applicable
        """
        
        if context:
            if context.get("programming_language"):
                base_prompt += f"\n- Use {context['programming_language']} as the programming language"
            if context.get("framework"):
                base_prompt += f"\n- Use {context['framework']} framework"
            if context.get("existing_code"):
                base_prompt += f"\n- Consider existing codebase context: {context['existing_code']}"
        
        return base_prompt


class AIProviderFactory:
    """Factory for creating AI provider instances."""
    
    @staticmethod
    def create_provider(provider_type: str = "auto") -> AIProvider:
        """Create an AI provider instance."""
        if provider_type == "auto":
            # Auto-detect based on available API keys
            if settings.openai_api_key:
                return OpenAIProvider()
            elif settings.anthropic_api_key:
                return AnthropicProvider()
            else:
                raise ValueError("No AI provider API key configured")
        
        elif provider_type == "openai":
            if not settings.openai_api_key:
                raise ValueError("OpenAI API key not configured")
            return OpenAIProvider()
        
        elif provider_type == "anthropic":
            if not settings.anthropic_api_key:
                raise ValueError("Anthropic API key not configured")
            return AnthropicProvider()
        
        else:
            raise ValueError(f"Unknown provider type: {provider_type}")
