file_template = '''from nba_api.stats.endpoints._base import Endpoint
from nba_api.stats.library.http import NBAStatsHTTP{imports}


class {endpoint}(Endpoint):
    endpoint = '{endpoint_lowercase}'
    expected_data = {data_sets}

    nba_response = None
    data_sets = None
    player_stats = None
    team_stats = None
    headers = None

    def __init__(self,
{arguments},
                 proxy=None,
                 headers=None,
                 timeout=30,
                 get_request=True):
        self.proxy = proxy
        if headers is not None:
            self.headers = headers
        self.timeout = timeout
        self.parameters = {{
{parameters}
        }}
        if get_request:
            self.get_request()
    
    def get_request(self):
        self.nba_response = NBAStatsHTTP().send_api_request(
            endpoint=self.endpoint,
            parameters=self.parameters,
            proxy=self.proxy,
            headers=self.headers,
            timeout=self.timeout,
        )
        self.load_response()
        
    def load_response(self):
        data_sets = self.nba_response.get_data_sets()
        self.data_sets = [Endpoint.DataSet(data=data_set) for data_set_name, data_set in data_sets.items()]
{data_set_variables}
'''

data_set_template = '''        self.{variable_name} = Endpoint.DataSet(data=data_sets['{key_name}'])'''

imports_template = '''\nfrom nba_api.stats.library.parameters import {imports_list}'''

function_template = '''    def {function_name}(self):
        return self.get_normalized_dict()['{data_header}']
'''

parameter_template = '''                '{nba_parameter}': {python_variable}'''

argument_template = '''                 {python_variable}={default_value}'''
no_default_argument_template = '''                 {python_variable}'''
