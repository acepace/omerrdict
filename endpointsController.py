import endpoints

from rpc import wordAPI
from rpc import helloworld_api
package = 'omerrdict'

APPLICATION = endpoints.api_server([wordAPI.WordAPIApi,helloworld_api.HelloWorldApi])