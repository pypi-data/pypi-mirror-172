from http import HTTPStatus
import json
import re
import requests
from typing import List, Union
import warnings

from zaiclient import config
from zaiclient import http
from zaiclient.auth import ZaiHmacAuth
from zaiclient.exceptions.ZaiClientException import ZaiClientException
from zaiclient.request import *
from zaiclient.response.EventLoggerResponse import EventLoggerResponse
from zaiclient.response.RecommendationResponse import RecommendationResponse

class ZaiClient(object):

    def __init__(self, client_id: str, secret: str, connect_timeout: Union[int, float] = config.CONNECT_TIMEOUT_S, read_timeout: Union[int, float] = config.READ_TIMEOUT_S, custom_endpoint: str = ""):

        if type(client_id) != str:
            raise TypeError('Client ID must be a string value.')
        if type(secret) != str:
            raise TypeError('Secret must be a string value.')
        if isinstance(connect_timeout, (int, float)) == False:
            raise TypeError('Connect Timeout must be an integer or a float value.')
        if isinstance(read_timeout, (int, float)) == False:
            raise TypeError('Read Timeout must be an integer or a float value.')
        if type(custom_endpoint) != str:
            raise TypeError('Custom Endpoint must be a string value.')
        if len(custom_endpoint) > 10:
            raise ValueError("Custom Endpoint must be less than or equal to 10.")
        if re.match('^[a-zA-Z0-9-]*$', custom_endpoint) is None:
            raise ValueError("Only alphanumeric characters are allowed for custom endpoint.")
        
        __connect_timeout = connect_timeout
        if connect_timeout <= 0:
            __connect_timeout = config.CONNECT_TIMEOUT_S
        __read_timeout = read_timeout
        if read_timeout <= 0:
            __read_timeout = config.READ_TIMEOUT_S
            
        __custom_endpoint = "" if custom_endpoint == "" else f"-{custom_endpoint}"

        self.__client_id = client_id
        self.__auth = ZaiHmacAuth(client_id, secret)
        self.__timeout = (__connect_timeout, __read_timeout)
        self.__session = requests.Session()
        self.__ml_api_endpoint = config.ML_API_ENDPOINT.format(__custom_endpoint)
        self.__events_api_endpoint = config.EVENTS_API_ENDPOINT.format(__custom_endpoint)

    def __send_request(self, method: str, url: str, payload, headers = {}) -> requests.Response:
        
        response = requests.Response()
        try:
            response = self.__session.request(
                method=method,
                url=url,
                params=None,
                data=None,
                json=payload,
                headers=headers,
                cookies=None,
                files=None,
                auth=self.__auth,
                timeout=self.__timeout,
                verify=True
            )
            response.raise_for_status()
        except requests.HTTPError as http_err:
            raise ZaiClientException(http_err)
        except Exception as err:
            raise err

        status_code = response.status_code
        headers = response.headers
        body = response.json()

        if status_code == HTTPStatus.OK and headers['Content-Type'] == 'application/json':
            return body
        else:
            return None
    
    def add_event_log(self, event: BaseEvent) -> EventLoggerResponse:
        payload = event.get_payload()
        
        response_body = self.__send_request(
            http.POST,
            self.__events_api_endpoint + config.EVENTS_API_PATH, 
            payload, 
            {config.ZAI_CALL_TYPE_HEADER: config.ZAI_CALL_TYPE}
        )

        return EventLoggerResponse(**response_body)
        
    def update_event_log(self, event: BaseEvent) -> EventLoggerResponse:
        payload = event.get_payload()
        
        if isinstance(payload, List):
            raise Exception("EventBatch instance does not support updateEventLog operation.")
        
        response_body = self.__send_request(
            http.PUT,
            self.__events_api_endpoint + config.EVENTS_API_PATH, 
            payload, 
            {config.ZAI_CALL_TYPE_HEADER: config.ZAI_CALL_TYPE}
        )

        return EventLoggerResponse(**response_body)
        
    def delete_event_log(self, event: BaseEvent) -> EventLoggerResponse:
        payload = event.get_payload()
        
        response_body = self.__send_request(
            http.DELETE,
            self.__events_api_endpoint + config.EVENTS_API_PATH, 
            payload, 
            {config.ZAI_CALL_TYPE_HEADER: config.ZAI_CALL_TYPE}
        )

        return EventLoggerResponse(**response_body)
    
    def get_recommendations(self, recommendation: RecommendationRequest) -> RecommendationResponse:
        
        response_body = self.__send_request(
            http.POST,
            self.__ml_api_endpoint + recommendation.get_path(self.__client_id),
            recommendation.__dict__
        )
        try:
            response_body['metadata'] = json.loads(response_body['metadata'])
        except Exception as error:
            warnings.warn(f"Failed to parse the metadata to object, returning an empty object. Error Message: {error}")
            response_body['metadata'] = {}
        
        return RecommendationResponse(**response_body)