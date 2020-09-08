Goal: Compile a list of venues for each city

There are 30,000 cities, and ~5,000 requests per hour (~100,000 per day).We have pre approve for a personal account that ups request to 50,000 a day

Solution:

1. Turn each city into a file; the file's name is a sanitized version of the city name, and the file's contents are the raw city name (from our giant JSON city file)
2. Grab a random file
3. Use Foursquare's API to turn a city name into a list of venue IDs
4. If an error was thrown, the city name is "invalid"
5. Take this list of IDs/invalid name error message & save them/it to a new file (whose name is still the sanitized city name)

This allows us to queue 30,000 requests to Foursquare & fail gracefully if there's an error

`cache/`: The directory of files representing the cities that still have to be looked up

`cache/results/`: The directory of files representing a sample of venues for the given cities (or an error message if the city name was invalid)

To run the full lookup process:

    python autosearch.py

After the process, to sort the results:

    python process_cache.py

This consolidates cities that:

- Had a non-empty list of venues (stored in `venues/`)
- Had an empty list of venues (stored in `empty_cities.json`)
- Were invalid names (stored in `invalid_cities.json`)