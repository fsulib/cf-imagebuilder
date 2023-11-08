# Testing Components

1. Have docker installed.
2. Run `build.sh` to create images for focal and mantic (22.10.3) that include the necessary components.
3. Output images: `focal_awstoe:version` and `mantic_awstoe:version`
3. Run each container. The default command for each container simply runs `bash`. The `WORKDIR` is `/root/components`.

Example invocation:
```bash
docker run -it --rm --mount type=bind,source="${PWD}/components",destination=/root/components focal_awstoe:1.0
```

4. Test components.

Example invocation:
```bash
awstoe run --trace --parameters ParamName=ParamValue --documents component-awstools-installation-focal.yaml,component-docker-installation.yaml
```

5. Help with AWSTOE: `awstoe run --help`
