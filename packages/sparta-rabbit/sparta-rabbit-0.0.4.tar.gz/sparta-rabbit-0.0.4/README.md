# sparta-rabbit

Sparta rabbit library.

## Usage

See [here](/USAGE.md).

## Dependency management

You need to have [virtualenv](https://docs.python.org/3/tutorial/venv.html) installed globally. In case you don't, run:

```bash
pip install virtualenv
```

Create and activate a **_virtualenv_** (name it `.venv`).

```bash
python -m venv .venv
source .venv/bin/activate
```

> You should now see the prefix `(.venv)` in your terminal prompt. This means the virtualenv is active.

## Install locally

Install default and test requirements (assure `.venv` is active).

```shell
pip install -e .[test]
```

Run tests.

```shell
python -m pytest
```

## Setup GCP Build Triggers

Run the following command to create/update GCP Build Triggers.

```shell
gcloud beta builds triggers import --source=triggers.yaml
```


## Publish to [Pypi](https://pypi.org/user/spartanapproach/)

A cloud build trigger (see [Setup GCP Build Triggers](#setup-gcp-build-triggers)) will deploy the package whenever a new
git tag is pushed to origin. If `disabled` (default), such trigger needs to be manually invoked.

![GCP Build Trigger](https://github.com/Spartan-Approach/sparta-hello/blob/main/docs/gcp-build-trigger.png)

With the following command you can roll out a new (`patch`|`minor`|`major`) version and push it, as git tag, to origin.

```shell
./scripts/rollout_version.sh [patch|minor|major]
```

> When prompt `Push changes?`, type `y` and `Enter`.

Alternatively, you can manually publish to [Pypi](https://pypi.org/user/spartanapproach/) with user credentials.

```shell
./scripts/publish.sh --username spartanaproach --password ***
```

# Setup `rabbitmq-development`

Save IP and credentials to local `.env`.

```shell
echo """
RABBIT_HOST=$(kubectl get service/rabbitmq-development-rabbitmq-svc -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
RABBIT_USER=$(kubectl get secret/rabbitmq-development-app-secret -o jsonpath='{.data.USER}'|base64 -D)
RABBIT_PASSWORD=$(kubectl get secret/rabbitmq-development-app-secret -o jsonpath='{.data.PASSWORD}'|base64 -D)
""" >> .env
```
