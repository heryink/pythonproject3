from pydantic import BaseModel

from typing import List,Optional
import requests

class HTTPClient:

    def __init__(self, base_url):
        self.base_url = base_url.rstrip("/")


    class request(BaseModel):
        method: str
        path: str
        query: Optional[dict[str,str]] = None


    def get(self, **request):
        """get client request"""
        path = request.get("path").lstrip("/")
        url = f"{self.base_url}/{path}"
        if request.get("query") != None:
            response = requests.get(url,params=request.get("query"))
        else:
            response = requests.get(url)

        return response

client = HTTPClient("https://jsonplaceholder.typicode.com")
searchh = client.request(method="method",path="/user")
print(client.get(searchh.dict()))






