# elasticsearch-get-features
Provide packages and versions, and get back features and bugs.

# Usage
python ./get-features.py --help
```
usage: get-features.py [-h] [--json JSON] [--index INDEX] [-u URL]
                       [--doctype DOCTYPE] [-v]

optional arguments:
  -h, --help         show this help message and exit
  --json JSON        Path to JSON file with packages and versions
  --index INDEX      ElasticSearch index to search
  -u URL, --url URL  URL for ElasticSearch server to query
  --doctype DOCTYPE  ElasticSearch doc type to search. (default: doc)
  -v, --verbose      Give more verbose output
```

# Build and test process
docker build --file BuildtestDockerfile --tag ironsalsa/get-features:latest .

docker run --mount type=bind,source="$(pwd)",target=/testapp ironsalsa/get-features:latest

# JSON Input format

```
{
    "dependencyversions": [
        {
            "version": "2.0.3",
            "package": "@scope/packagename"
        },
        {
            "version": "2.0.24",
            "package": "unscopedpackage"
        }
    ]
}
```