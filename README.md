# elasticsearch-get-features
Provide packages and versions, and get back features and bugs.

# Build and test process
docker build --file BuildtestDockerfile --tag ironsalsa/get-features:latest .

docker run --mount type=bind,source="$(pwd)",target=/testapp ironsalsa/get-features:latest

# Input format

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