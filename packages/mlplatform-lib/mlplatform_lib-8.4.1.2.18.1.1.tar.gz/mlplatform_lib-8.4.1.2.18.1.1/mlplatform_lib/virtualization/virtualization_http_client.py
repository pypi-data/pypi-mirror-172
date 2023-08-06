from dataclasses import dataclass
from enum import Enum
import json
import requests
from mlplatform_lib.auth import Auth
from typing import Optional, Dict, List, Union, Tuple
from mlplatform_lib.utils.dataclass_utils import from_dict, to_dict
from mlplatform_lib.api_client import ApiClient
import zipfile
import io
import os

class VirtualizationRequestException(Exception):
    status_code = 200

    def __init__(self, message, status_code=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code

class VirtualizationRequestType(Enum):
    CREATE = 0
    READ = 1
    UPDATE = 2
    DELETE = 3
    DOWNLOAD = 4
    READ_WITH_FORM_DATA = 5

@dataclass
class VirtualizationRequestResult:
    data: Optional[Union[Dict, List[Dict], bytes]]
    content: Optional[str]
    status_code: Optional[int]

class VirtualizationHttpClient:
    def __init__(self, virtualization_addr, api_client: ApiClient):
        self.base_url = virtualization_addr + "/hyperdata20"
        self.api_client = api_client

    def send_request(
        self,
        service: str,
        rest: Optional[dict],
        query: Optional[dict],
        data: Optional[dict],
        request_type: VirtualizationRequestType,
    ) -> VirtualizationRequestResult:
        auth = Auth(api_client=self.api_client)
        headers = {
            "Content-Type": "application/json",
            "Authorization": auth.authorization,
            "userId": auth.userId,
        }

        if rest is None:
            rest = {}

        if query is None:
            query = {}

        if data is None:
            data = {}

        if request_type == VirtualizationRequestType.DOWNLOAD:
            headers["Content-Type"] = "application/octet-stream"

        url = self.base_url
        for key, val in rest.items():
            url = url + "/" + str(key) + "/" + str(val)
        if service != "" and service is not None:
            url = url + "/" + service

        if len(query) != 0:
            url += "?"
            for idx, (key, val) in enumerate(query.items()):
                if idx != 0:
                    url += "&"
                url = url + str(key) + "=" + str(val)

        if request_type == VirtualizationRequestType.READ or request_type == VirtualizationRequestType.DOWNLOAD:
            response = requests.get(url, headers=headers, data=json.dumps(data), verify=False)
        elif request_type == VirtualizationRequestType.CREATE:
            response = requests.post(url, headers=headers, data=json.dumps(data), verify=False)
        elif request_type == VirtualizationRequestType.UPDATE:
            response = requests.put(url, headers=headers, data=json.dumps(data), verify=False)
        elif request_type == VirtualizationRequestType.DELETE:
            response = requests.delete(url, headers=headers, data=json.dumps(data), verify=False)
        elif request_type == VirtualizationRequestType.READ_WITH_FORM_DATA:
            response = requests.get(url, headers=headers, data=json.dumps(data), verify=False)
        else:
            return VirtualizationRequestResult(None, None, None)

        if response.status_code == 200:
            if VirtualizationRequestType.READ or request_type == VirtualizationRequestType.DOWNLOAD :
                return VirtualizationRequestResult(response.content, None, response.status_code)
            else:
                return VirtualizationRequestResult(
                    response.json(), response.content.decode(), response.status_code
                )
        else:
            print(response.content.decode())
            print(
                (
                    f"cannot connect to {url}. "
                    f"virtualization server returns status code {response.status_code}"
                )
            )
            raise VirtualizationRequestException(response.content.decode(), response.status_code)

    def download_unstructured(self, do_id:str) :
        result = self.send_request(
            "download/ozone/unstructured",
            {"dataobjects": do_id},
            {"fileName":"do"+do_id,"regex":"","dateStart":"","dateEnd":""},
            {},
            VirtualizationRequestType.READ,
        )
        zip_file = zipfile.ZipFile(io.BytesIO(result.data),"r")

        if len(zip_file.namelist())==1:
            with zip_file as zip:
                zip.extractall("/home/jovyan/data")
        elif len(zip_file.namelist())>1:
            if not os.path.isdir("/home/jovyan/data/"+do_id):
                os.makedirs("/home/jovyan/data/"+do_id)
            with zip_file as zip:
                zip.extractall("/home/jovyan/data/"+do_id)
        return zip_file.namelist()
        
        
            
            
