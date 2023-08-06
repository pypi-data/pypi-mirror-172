# nitor-devel-backend

Utility to easily run a proxy to unite local development and dev/prod nitor apis

# Overview

![Architecture overview](nitor-devel-backend.png)

# Installation

`pip install nitor-devel-backend`

# Usage

```bash
usage: nitor-devel-backend [-h] (--port PORT | --directory DIRECTORY | --service SERVICE | --file FILE) [--impersonate IMPERSONATE] {dev,prod}

Run a nitor backend locally to enable serving nitor data backends and your development server resources from the same port. Proxy is available on https://localhost:8443 and can not
be changed because it is configured as a redirect url for the authentication provider.

positional arguments:
  {dev,prod}            Run agains dev or prod data resources

optional arguments:
  -h, --help            show this help message and exit
  --port PORT, -p PORT  The port your local dev server is listening to
  --directory DIRECTORY, -d DIRECTORY
                        The directory holding your created site static artifacts
  --service SERVICE, -s SERVICE
                        Give dev service backend configuration as json on the command line in case you want to for example mix a local dynamic server with local static resources.
                        Needs to be an array of service configraion elements. See https://github.com/NitorCreations/nitor-backend for available services.
  --file FILE, -f FILE  Give dev service backend configuration as json in a file. See above.
  --impersonate IMPERSONATE, -i IMPERSONATE
                        Impersonate a virtualhost service in the existing configuration by forwarding any proxy subservices with the target in the internal ALB to the ssh tunnel and
                        forwarding s3 traffic to the local development backend.
```

Typical use would be to start a local development server on say `localhost:3000` and then put nitor-devel-backend in front of that to provide production apis thusly:
`nitor-devel-backend -p 3000 prod`

## Coniguring Vite to work behind reverse proxy

In your `vite.config.ts` add the following:
```
export default defineConfig({
  server: {
    host: true,
    port: 3000,
    strictPort: true,
    origin: 'https://localhost:8443'
  },
})
```


# Releasing a new version

## With new nitor-backend code

If nitor-backend needs to be updated, first build a new release of it. Using `release-podman.sh` and optionally push it also to `aws-infra` project.

Then run jenkins build of  [awsdev-devel-backend-docker-bake-proxy](https://amibakery.nitor.zone/view/all/job/awsdev-devel-backend-docker-bake-proxy/).

Then edit the [nitor_devel_backend/cli.py](nitor_devel_backend/cli.py) to point the docker image devel-backend/dev-proxy version to the latest jenkins build number of the previous task.

## Actual release of nitor-devel-backend

Run `./dist.sh [new-version] "What has changed"`. You will need to have _bumpversion_ and _twine_ python tools installed and set up to push to the nitor-devel-backend pypi project.
