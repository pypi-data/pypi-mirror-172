# Catapult API
A repository which contains code to interact with the Catapult API
<br>
The code is build around the [API documentation](https://docs.connect.catapultsports.com/reference/introduction). An equivalent R package has been build by the Catapult team, [catapultR](http://catapultr.catapultsports.com/)

### Usage


**Installation**
```python
pip install catapult-api
```

**Setup connection**
```python
from catapult_api.CatapultAPI import CatapultAPI

client = CatapultAPI(
    api_token="yourapi_token"
    )
teams = client.get_teams()
```
