from pydantic import BaseModel, Field
from typing import List

class UserIDList(BaseModel):
    user_ids: List[str] = Field(..., min_length=1, max_length=100)