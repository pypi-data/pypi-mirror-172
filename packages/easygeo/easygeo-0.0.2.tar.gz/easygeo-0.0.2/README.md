# Geocoding
 Geocoding library that makes geocodification easier (and possibly cheaper). 
 It's a wrapper for geopy geocoding tools. And at the moment it allows to use Google's V3 or Nominatim API.

## Instalation:

You can install this package using pip.

```python
pip install simplegeo
```

## Usage:

```python
from simplegeo import GeoCode

g = GeoCode(method="Nominatim", domain="nominatim.openstreetmap.org")

g.geocode("Beauchef 850, Santiago, RM, Chile")

# You can also bulk use this library
df["Address"].apply(g.geocode)

# This function allows to save the cached addresses into a file.
g.save_cache()
```

## Development:

In case you want to install simplegeo along with the tools you need to develop and run the tests, run the following in your virtualenv.

```bash
$ pip install -e .[dev]
```




