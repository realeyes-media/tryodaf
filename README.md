# elasticsearch-get-features
Provide packages and versions, and get back features and bugs.

# Build and test process
docker build --file BuildtestDockerfile --tag ironsalsa/get-features:latest .

docker run --mount type=bind,source="$(pwd)",target=/testapp ironsalsa/get-features:latest