
# Python Wrapper for WeatherBit API

![Latest PyPI version](https://img.shields.io/pypi/v/pyweatherbitdata) ![Supported Python](https://img.shields.io/pypi/pyversions/pyweatherbitdata)

This module communicates with WeatherBit.io using [their REST API](https://www.weatherbit.io/api). The module is only supporting the Free Tier API's, for which there is more information [here](https://www.weatherbit.io/pricing).

For the Free Tier, data can be retrieved for the following:

* Current Conditions
* Forecast Data - Daily data.
* Severe Weather Alerts

It will require an API Key to work, which can be retrieved for free at [Weatherbit](https://www.weatherbit.io/account/create)

The module is primarily written for the purpose of being used in Home Assistant for the Custom Integration called `weatherbit` but might be used for other purposes also.

## Install

`pyweatherbitdata` is avaible on PyPi:

```bash
pip install pyweatherbitdata
```

## Usage

This library is primarily designed to be used in an async context.

The main interface for the library is the `pyweatherbitdata.WeatherBitApiClient`. This interface takes 7 options:

* `api_key`: (required) A Personal API Key retrieved from WeatherBit (See above).
* `latitude`: (required) Latitude of the location needing data from.
* `longitude`: (required) Longitude of the location needing data from.
* `units`: (optional) Valid options here are *metric* or *imperial*. This module is set to always retrieve data in *metric* units, so conversion of values will only take place if if metric is not selected. Default value is **metric**
* `language`: (optional) The language for all text values retrieved from WeatherBit. Default is **en**
* `homeassistant`: (optional) Valid options are *True* or *False*. If set to True, there will be some unit types that will not be converted, as Home Assistant will take care of that. Default value is **True**

### Example program

```python
"""Test Program."""
from __future__ import annotations

import asyncio
import logging
import time

from pyweatherbitdata.api import WeatherBitApiClient
from pyweatherbitdata.data import (
    ObservationDescription,
    BaseDataDescription,
    ForecastDescription
)
from pyweatherbitdata.exceptions import (
    InvalidApiKey,
    RequestError,
    ResultError,
)

_LOGGER = logging.getLogger(__name__)

async def main() -> None:
    logging.basicConfig(level=logging.DEBUG)
    start = time.time()

    weatherbit = WeatherBitApiClient(
        "YOU_API_KEY",
        55.625053,
        12.136619,
        language="da",
    )
    try:
        await weatherbit.initialize()

    except InvalidApiKey as err:
        _LOGGER.debug(err)
    except RequestError as err:
        _LOGGER.debug(err)
    except ResultError as err:
        _LOGGER.debug(err)

    data: BaseDataDescription = weatherbit.station_data
    if data is not None:
        for field in data.__dataclass_fields__:
            value = getattr(data, field)
            print(field, "-", value)

    data: ObservationDescription = await weatherbit.update_sensors()
    if data is not None:
        for field in data.__dataclass_fields__:
            value = getattr(data, field)
            print(field, "-", value)

    data: ForecastDescription = await weatherbit.update_forecast()
    if data is not None:
        for field in data.__dataclass_fields__:
            value = getattr(data, field)
            print(field, "-", value)

    end = time.time()

    await weatherbit.req.close()

    _LOGGER.info("Execution time: %s seconds", end - start)

asyncio.run(main())
```
