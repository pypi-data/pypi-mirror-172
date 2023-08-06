from typing import Union
from pydantic import BaseModel, conint, conlist, constr

class RecommendationRequest(BaseModel):

    user_id: Union[constr(min_length=1, max_length=500), None]
    item_id: Union[constr(min_length=1, max_length=500), None]
    item_ids: Union[conlist(
        item_type=constr(min_length=1, max_length=500),
        min_items=0,
        max_items=10_000
    ), None]
    recommendation_type: constr(min_length=1, max_length=500)
    limit: conint(ge=0, le=10_000)
    offset: conint(ge=0, le=10_000) = 0
    options: constr(min_length=0, max_length=1000) = None
    
    
    def get_path(self, client_id: str) -> str:
        raise NotImplementedError("Should be overriden.")
