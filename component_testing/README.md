# Testing Components

'Tis possible to use the [awstoe](https://docs.aws.amazon.com/imagebuilder/latest/userguide/manage-components.html) in a containerized local environment to test ImageBuilder components.

## Steps

1. Have docker installed.
2. Set environment variables. See below.
3. Run `build.sh` to create images for focal (20.04), jammy (22.04), and mantic (23.10.3) that include the necessary components.
4. Output images: `focal_awstoe:version` and `mantic_awstoe:version`
5. Run each container. The default command for each container simply runs `bash`. The `WORKDIR` is `/root/components`.

## Environment Variables

Something like this helps:

```bash
export AWS_REGION=us-east-1
export VERSION_TAG=1.0
export DIST=focal
```

`VERSION` is the _image's_ version tag. `DIST` is the __first word__ of the __distribution's code name__, e.g. 'focal.'

## Running the Container

Example invocation:
```bash
docker run -it --rm --mount type=bind,source="${PWD}/components",destination=/root/components focal_awstoe:1.0
```

## Testing the Components

Example invocation:
```bash
awstoe run --trace --parameters ParamName=ParamValue --documents component-awstools-installation-focal.yaml,component-docker-installation.yaml
```

## Help

Help with AWSTOE: `awstoe run --help`
