# elasticsearch-get-features
Provide packages and versions, and get back features and bugs.

# Usage
Example command:

python ./tryodaf --name Appname --packageorapp App --version 1.0.1 --commitdate "April 23 2018" /
    --commitmessage "This is a commit message --prmessage test.txt --json packageversions.json /
    --index featuretrackingexample --url "https://nbcs-log.realeyes.cloud/" --doctype doc --outputfile output.json

python ./tryodaf.py --help
```
usage: tryodaf.py [-h] --name NAME --packageorapp PACKAGEORAPP --version
                  VERSION --commitdate COMMITDATE --commitmessage
                  COMMITMESSAGE --prmessage PRMESSAGE --json JSON --index
                  INDEX -u URL [--doctype DOCTYPE] [--outputfile OUTPUTFILE]

optional arguments:
  -h, --help            show this help message and exit
  --name NAME           Name of this package or app
  --packageorapp PACKAGEORAPP
                        Is this a package or app?
  --version VERSION     The version of this package or app
  --commitdate COMMITDATE
                        Date of this commit
  --commitmessage COMMITMESSAGE
                        Message of this commit
  --prmessage PRMESSAGE
                        File path to a newline separated PR description
  --json JSON           Path to JSON file with package:version list
  --index INDEX         ElasticSearch index to search
  -u URL, --url URL     URL for ElasticSearch server to query
  --doctype DOCTYPE     ElasticSearch doc type to search. (default: doc)
  --outputfile OUTPUTFILE
                        Name of JSON file to output results
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
