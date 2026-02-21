"""Base agent class."""
from abc import ABC, abstractmethod
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel
from .llm_factory import create_llm
import json


class BaseAgent(ABC):
    """Base class for all agents."""
    
    def __init__(self, model_name: str = None, temperature: float = None):
        self.llm = create_llm(model_name=model_name, temperature=temperature)
    
    @abstractmethod
    def get_prompt(self) -> ChatPromptTemplate:
        """Return the agent's prompt template."""
        pass
    
    @abstractmethod
    def get_output_schema(self) -> type[BaseModel]:
        """Return the Pydantic schema for structured output."""
        pass
    
    def run(self, **kwargs) -> BaseModel:
        """Execute the agent with fallback for structured output."""
        prompt = self.get_prompt()
        schema = self.get_output_schema()
        
        try:
            # Try structured output first (works with OpenAI, some others)
            structured_llm = self.llm.with_structured_output(schema)
            chain = prompt | structured_llm
            result = chain.invoke(kwargs)
            return result
        except (AttributeError, NotImplementedError) as e:
            # Fallback: Use JSON parsing for providers that don't support structured output
            print(f"⚠️ Structured output not supported, using JSON parsing fallback")
            
            # Add JSON instructions to prompt
            json_prompt = prompt.format(**kwargs)
            json_prompt += f"\n\nIMPORTANT: Respond ONLY with valid JSON matching this schema:\n{schema.model_json_schema()}"
            
            # Get response
            response = self.llm.invoke(json_prompt)
            
            # Extract content
            if hasattr(response, 'content'):
                content = response.content
            else:
                content = str(response)
            
            # Try to parse JSON from response
            try:
                # Find JSON in response (might have extra text)
                start = content.find('{')
                end = content.rfind('}') + 1
                if start >= 0 and end > start:
                    json_str = content[start:end]
                    data = json.loads(json_str)
                    return schema(**data)
                else:
                    raise ValueError("No JSON found in response")
            except Exception as parse_error:
                raise ValueError(
                    f"Failed to parse response as JSON: {parse_error}\n"
                    f"Response: {content[:500]}"
                )
