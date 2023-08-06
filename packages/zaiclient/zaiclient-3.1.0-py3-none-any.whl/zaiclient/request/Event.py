from typing import Union
from pydantic import BaseModel, confloat, constr

class Event(BaseModel):

    user_id: constr(min_length=1, max_length=500)
    item_id: Union[constr(min_length=1, max_length=500), None]
    timestamp: confloat(ge=1_648_871_097., le=2_147_483_647.)
    event_type: constr(min_length=1, max_length=500)
    event_value: constr(min_length=1, max_length=500)
    
    class Config:

        schema_extra = {
            'example': {
                'user_id': '123456',
                'item_id': 'ABCDEF',
                'timestamp': 1_648_871_097.,
                'event_type': 'product_detail_view',
                'event_value': '1'
            }
        }