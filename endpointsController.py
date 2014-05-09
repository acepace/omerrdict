import endpoints

from rpc import wordAPI
package = 'omerrdict'

APPLICATION = endpoints.api_server([wordAPI.WordAPIApi])