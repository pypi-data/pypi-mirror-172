# m360.mw.python

The M360 Python Middleware is a dependency that gets consumed by a Python Web Server built using one of these frameworks [Django](https://www.djangoproject.com/) and [Flask](https://flask.palletsprojects.com/en/2.0.x/).

The middleware is developed using native Python and includes interfaces that facilitate using it with the above mentioned frameworks.

---

## Installation ##
```commandline
pip install m360-middleware
```

---

## Usage ##
### Django ###
In your settings.py file, include the middleware and its configuration:
```python
import os
# ...
MIDDLEWARE = [
   # ...
   # -------------------- M360 Middleware Setup --------------------
   'm360.frameworks.django.middleware.DjangoMiddleware',
   # ...
]
# ...
M360 = {
    "contract": os.path.join(os.path.dirname(__file__), "./contract.json"),
    "ip":  os.environ.get('APP_IP') or "127.0.0.1",
    "type": "django",
    "platform": "manual"
}
```
In your **views**, import and use the middleware:
```python
from django.http import JsonResponse

# the sdk is initialized using the middleware when Django starts
from m360 import sdk
M360 = sdk.instance()

def get_settings(request):
    return JsonResponse(M360.registry.get(), status=200, safe=False)
```

### Flask ###
In your settings.py file, include the middleware and its configuration:
```python
import os
# ...
app = Flask(__name__)

from m360.frameworks.flask.middleware import FlaskMiddleware
app.wsgi_app = FlaskMiddleware(app.wsgi_app, {
    "contract": os.path.join(os.path.dirname(__file__), "./contract.json"),
    "ip": os.environ.get('APP_IP') or "127.0.0.1",
    "type": "flask",
    "platform": "manual"
})
```
In your **views**, import and use the middleware:
```python
# the sdk is initialized using the middleware when Flask starts
import json
from m360 import sdk
M360 = sdk.instance()

@app.route('/m360/settings', methods=['GET', 'POST'])
def m360_settings():
    return json.dumps(M360.registry.get())
```

## Containerized Deployment ##

---

### Deploying on Docker ###

When deploying on Docker, please provide the extra options below.
Without these options, the handshake between the middleware and the gateway will fail, 
along with any maintenance operation that gets triggered from the console onto this microservice.

Replace the `platform:manual` with `platform:docker` and add the below.

Option | Data Type | Mandatory | Description
--- | --- | --- | ---
platform | String | YES | value equals 'docker'
network | String | YES | value equals the docker network attached to this docker service
service | String | YES | value equals the name of the docker service
containerIP | String | NO | value is the internal IP address of the docker container in the docker service

**Example**
```javascript
'platform': 'docker',
'platformOptions': {
    'network': 'mike',
    'service': 'service-express',
    'containerIP': '127.0.0.1'
}
```
### Deploying on Kubernetes ###

When deploying on Kubernetes, please provide the extra options below.
Without these options, the handshake between the middleware and the gateway will fail,
along with any maintenance operation that gets triggered from the console onto this microservice.

Replace the `platform:manual` with `platform:kubernetes` and add the below.

Option | Data Type | Mandatory | Description
--- | --- | --- | ---
platform | String | YES | value equals 'kubernetes'
namespace | String | YES | value equals the kubernetes namespace where your deployment will run
service | String | YES | value equals the name of the kubernetes service that is attached to the your deployment
exposedPort | String | YES | value equals the exposed port kubernetes service

```javascript
'platform': 'kubernetes',
'platformOptions": {
    'namespace': 'mike',
    'service': 'service-express',
    'exposedPort': 30402
}
```
---

## Notes ##
The Middleware includes samples on how you can consume it with both Django and Flask.

These sample apps are located inside the **examples** folder in this repository.

Reference: [M360 Middleware Official Documentation](https://corsairm360.atlassian.net/servicedesk/customer/portal/4/topic/419cca91-5815-447b-abde-8455ae8a1717)