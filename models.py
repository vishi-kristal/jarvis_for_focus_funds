"""
Pydantic models for request/response validation in the FastAPI application.
"""

from pydantic import BaseModel, Field
from typing import Optional

class QuestionRequest(BaseModel):
    """Request model for asking questions to the AI assistant."""
    question: str = Field(
        ..., 
        min_length=1, 
        max_length=2000,
        description="The question to ask the AI assistant about fund documents"
    )

class AnswerResponse(BaseModel):
    """Response model for AI assistant answers."""
    answer: str = Field(
        ...,
        description="The AI-generated answer to the user's question"
    )

class ErrorResponse(BaseModel):
    """Error response model."""
    error: str = Field(
        ...,
        description="Error message describing what went wrong"
    )
    detail: Optional[str] = Field(
        None,
        description="Additional error details if available"
    )
