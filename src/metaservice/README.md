
# Build

`dockerfile.test` will produce the metaservice that ready for use.

```bash
docker build -t rds_meta -f dockerfile.test .
```

During the build, docker will clone the repo from https://github.com/ouankou/rds-meta, which basically has the same content as here. Currently, RDS repository is private. To use it in the dockerfile, we have to use a public repo as alternative for now.

The docker image has been pushed to Docker Hub.
https://hub.docker.com/repository/docker/ouankou/rds
```bash
docker pull ouankou/rds:meta-test
```

# Run

```bash
docker run -d -p 5010:5000 --name meta-test ouankou/rds:meta-test
```

The server will run in the background. To check the server status, we can attach it to the foreground.

```bash
docker attach meta-test
```

# Test

```bash
curl -F 'file=@DRB095-doall2-taskloop-orig-yes.c' cci-pivo:5010/test?type=json
```

A file will be uploaded to the RDS metaservice. Then it will be sent to all four microservices for testing.
