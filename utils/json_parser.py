"""
Robust JSON parsing utilities
Handles various JSON formats including markdown-wrapped content
"""

import json
import re
from typing import Any, Dict, List, Optional, Union
import logging

logger = logging.getLogger(__name__)

class JSONParseError(Exception):
    """Custom exception for JSON parsing errors"""
    pass

class RobustJSONParser:
    """Robust JSON parser that handles various formats"""
    
    @staticmethod
    def extract_json_from_text(text: str, expected_type: str = "any") -> Optional[Any]:
        """
        Extract JSON from text with multiple strategies
        
        Args:
            text: Input text that may contain JSON
            expected_type: Expected JSON type ("object", "array", "any")
            
        Returns:
            Parsed JSON data or None if parsing fails
        """
        # Strategy 1: Try to find JSON in markdown code blocks
        json_data = RobustJSONParser._extract_from_markdown(text)
        if json_data is not None:
            return json_data
        
        # Strategy 2: Try to find raw JSON objects/arrays
        json_data = RobustJSONParser._extract_raw_json(text, expected_type)
        if json_data is not None:
            return json_data
        
        # Strategy 3: Try to clean and parse the entire text
        json_data = RobustJSONParser._extract_cleaned_json(text)
        if json_data is not None:
            return json_data
        
        logger.warning(f"Failed to extract JSON from text: {text[:200]}...")
        return None
    
    @staticmethod
    def _extract_from_markdown(text: str) -> Optional[Any]:
        """Extract JSON from markdown code blocks"""
        # Look for ```json ... ``` or ``` ... ``` blocks
        patterns = [
            r'```json\s*\n(.*?)\n```',
            r'```\s*\n(.*?)\n```',
            r'```json(.*?)```',
            r'```(.*?)```'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
            if match:
                json_str = match.group(1).strip()
                try:
                    return json.loads(json_str)
                except json.JSONDecodeError:
                    continue
        
        return None
    
    @staticmethod
    def _extract_raw_json(text: str, expected_type: str = "any") -> Optional[Any]:
        """Extract raw JSON objects or arrays"""
        if expected_type == "array" or expected_type == "any":
            # Try to find JSON arrays
            start_idx = text.find('[')
            if start_idx != -1:
                end_idx = text.rfind(']') + 1
                if end_idx > start_idx:
                    json_str = text[start_idx:end_idx]
                    try:
                        return json.loads(json_str)
                    except json.JSONDecodeError:
                        pass
        
        if expected_type == "object" or expected_type == "any":
            # Try to find JSON objects
            start_idx = text.find('{')
            if start_idx != -1:
                end_idx = text.rfind('}') + 1
                if end_idx > start_idx:
                    json_str = text[start_idx:end_idx]
                    try:
                        return json.loads(json_str)
                    except json.JSONDecodeError:
                        pass
        
        return None
    
    @staticmethod
    def _extract_cleaned_json(text: str) -> Optional[Any]:
        """Try to parse JSON after cleaning the text"""
        # Remove common non-JSON content
        cleaned = text.strip()
        
        # Remove leading/trailing explanatory text
        lines = cleaned.split('\n')
        
        # Try to find lines that look like JSON
        json_lines = []
        in_json = False
        
        for line in lines:
            line_stripped = line.strip()
            
            # Start of JSON object or array
            if line_stripped.startswith(('{', '[')):
                in_json = True
                json_lines.append(line)
            # End of JSON object or array
            elif line_stripped.endswith(('}', ']')) and in_json:
                json_lines.append(line)
                break
            # Middle of JSON
            elif in_json:
                json_lines.append(line)
        
        if json_lines:
            json_str = '\n'.join(json_lines)
            try:
                return json.loads(json_str)
            except json.JSONDecodeError:
                pass
        
        return None
    
    @staticmethod
    def safe_parse_with_fallback(text: str, expected_type: str = "any", 
                                fallback_data: Any = None) -> Any:
        """
        Parse JSON with fallback data if parsing fails
        
        Args:
            text: Input text
            expected_type: Expected JSON type
            fallback_data: Data to return if parsing fails
            
        Returns:
            Parsed JSON or fallback data
        """
        try:
            result = RobustJSONParser.extract_json_from_text(text, expected_type)
            if result is not None:
                return result
            
            logger.warning(f"JSON parsing failed, using fallback data")
            return fallback_data
            
        except Exception as e:
            logger.error(f"Unexpected error in JSON parsing: {e}")
            return fallback_data
    
    @staticmethod
    def validate_json_structure(data: Any, required_fields: List[str] = None) -> bool:
        """
        Validate that JSON data has required structure
        
        Args:
            data: Parsed JSON data
            required_fields: List of required field names
            
        Returns:
            True if structure is valid
        """
        if not isinstance(data, dict):
            return False
        
        if required_fields:
            for field in required_fields:
                if field not in data:
                    logger.warning(f"Missing required field: {field}")
                    return False
        
        return True

# Convenience functions
def parse_json_safely(text: str, expected_type: str = "any") -> Optional[Any]:
    """Quick function to parse JSON safely"""
    return RobustJSONParser.extract_json_from_text(text, expected_type)

def parse_report_plan(text: str) -> Optional[Dict]:
    """Parse report plan JSON with validation"""
    data = RobustJSONParser.extract_json_from_text(text, "object")
    if data and RobustJSONParser.validate_json_structure(data, ["title", "sections"]):
        return data
    return None

def parse_search_queries(text: str) -> Optional[List[str]]:
    """Parse search queries JSON array"""
    data = RobustJSONParser.extract_json_from_text(text, "array")
    if data and isinstance(data, list) and all(isinstance(item, str) for item in data):
        return data
    return None 