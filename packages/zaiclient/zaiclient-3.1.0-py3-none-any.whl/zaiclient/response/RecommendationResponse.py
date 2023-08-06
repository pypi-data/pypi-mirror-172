from typing import List
from pydantic import BaseModel, confloat, conint

class RecommendationResponse(BaseModel):

    items: List[str]
    count: conint(ge=0, le=1_000_000)
    metadata: dict
    timestamp: confloat(ge=1_648_871_097., le=2_147_483_647.)

    class Config:

        schema_extra = {
            'example': {
                'items': ["1234", "1232"],
                'count': 4,
                'metadata': {
                    'recommendation_type': 'homepage'
                },
                'timestamp': 1648835666.825221,
            }
        }