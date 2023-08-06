from easygeo import GeoCode
import geopy

def test_constructor():
    # Nominatim constructor
    g = GeoCode(method="Nominatim", domain="nominatim.openstreetmap.org", cache_file="./test/cache.json", min_delay = 2)
    assert(g.cache==dict())
    assert(g.api_key == None)
    assert(g.cache_file == "./test/cache.json")
    assert(g.domain == "nominatim.openstreetmap.org")
    assert(g.geocoder.__class__ == geopy.extra.rate_limiter.RateLimiter)
    assert(g.geolocator.__class__ == geopy.geocoders.nominatim.Nominatim)
    assert(g.min_delay_seconds == 2)
    assert(g.method == "Nominatim")
    # GoogleV3 constructor
    g2 = GeoCode(method="GoogleV3", api_key="aaa", cache_file="./test/cache_g.json")
    assert(g2.method == "GoogleV3")
    assert(g2.domain == "maps.google.cl")
    assert(g2.api_key == "aaa")
    assert(g2.cache_file == "./test/cache_g.json")
    assert(g2.min_delay_seconds == 0.02)
    # Initializing geocode with GoogleV3 api, will result in error.
    try:
        g3 = GeoCode()
    except:
        pass

def test_geolocator():
    g = GeoCode(method="Nominatim", domain="nominatim.openstreetmap.org", cache_file="./test/cache.json", min_delay = 2)
    geocoded_example = g.geocode("Beauchef 850, Santiago, RM, Chile")

    assert(list(geocoded_example.keys()) == ['formatted_address', "location"])
    assert(geocoded_example['formatted_address'] == "Escuela de Ingeniería Universidad de Chile, 850, Beauchef, Barrio República, Santiago, Provincia de Santiago, Región Metropolitana de Santiago, 8370456, Chile")
    assert(list(geocoded_example['location'].keys()) == ["lat", "long"])

def test_cache_load():
    g = GeoCode(method="Nominatim", domain="nominatim.openstreetmap.org", cache_file="./test/cache_test.json", min_delay = 2)
    geocoded_example = g.geocode("Beauchef 851, Santiago, RM, Chile", save = True)
    # New instance
    g2 = GeoCode(method="Nominatim", domain="nominatim.openstreetmap.org", cache_file="./test/cache_test.json", min_delay = 2)
    #g.load_cache()
    assert(len(g2.cache) == 1)
    geocoded_example = g.geocode("Beauchef 851, Santiago, RM, Chile")
    assert(len(g.cache) == 1)
    g.cache_file = "./test/cache.json"
    old_cache = g.cache 
    g.load_cache()
    assert(g.cache != old_cache)


#def 