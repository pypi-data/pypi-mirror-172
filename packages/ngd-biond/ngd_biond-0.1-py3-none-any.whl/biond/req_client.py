import requests
from urllib3.exceptions import InsecureRequestWarning


class RequestsClient:
    def __init__(self, base_url):
        self._base_url = base_url
        self._cookies = None
        self._verify = False
        if not self._verify:
            requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

    def get(self, get_action, params=None):
        if get_action.startswith("http"):
            url = get_action
        else:
            # Remove prefix if matches the end
            if get_action.startswith("/api/"):
                get_action = get_action[len("/api/"):]
            url = self._base_url + get_action
        r = requests.get(url, params=params, cookies=self._cookies, verify=self._verify)
        if len(r.cookies.list_domains()) > 0:
            dom1 = r.cookies.list_domains()[0]
            self._cookies = r.cookies.get_dict()
        return r

    def post(self, post_action, data=None, content_type=None):
        if post_action.startswith("http"):
            url = post_action
        else:
            url = self._base_url + post_action
        if content_type:
            headers = {"Content-Type": content_type}
        else:
            headers = {}
        r = requests.post(url, data, cookies=self._cookies, headers=headers, verify=self._verify)
        if len(r.cookies.list_domains()) > 0:
            dom1 = r.cookies.list_domains()[0]
            self._cookies = r.cookies.get_dict()
        r.data = r.content
        return r

    def put(self, put_action, data: dict, params: dict, content_type: str = None, api_key: str = None):
        if put_action.startswith("http"):
            url = put_action
        else:
            url = self._base_url + put_action
        if content_type:
            headers = {"Content-Type": content_type}
        else:
            headers = {}
        if api_key is not None:
            headers["X-API-Key"] = api_key
        r = requests.put(url, data, params=params, cookies=self._cookies, headers=headers, verify=self._verify)
        if len(r.cookies.list_domains()) > 0:
            dom1 = r.cookies.list_domains()[0]
            self._cookies = r.cookies.get_dict()
        r.data = r.content
        return r

    def delete(self, delete_action):
        if delete_action.startswith("http"):
            url = delete_action
        else:
            url = self._base_url + delete_action
        r = requests.delete(url, cookies=self._cookies, verify=self._verify)
        if len(r.cookies.list_domains()) > 0:
            dom1 = r.cookies.list_domains()[0]
            self._cookies = r.cookies.get_dict()
        r.data = r.content
        return r
