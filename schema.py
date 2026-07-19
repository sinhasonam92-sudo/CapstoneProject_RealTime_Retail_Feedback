from pydantic import BaseModel, Field


class ReviewAnalysis(BaseModel):

    estimated_rating: int = Field(
        description="Estimated rating from 1-5"
    )

    product: str

    category: str

    department: str

    urgency: str

    summary: str

    recommended_action: str