# Stage 2: imagestream-copy
Steps to run:

1. Get the source registry url, username and password
2. Get the destination registry url, username and password
4. Log into the destination cluster as admin
5. Copy the vars example file `cp vars/imagestream-copy.yml.example vars/imagestream-copy.yml` and populate the registry data
6. Run `ansible-playbook imagestream-copy.yml`
7. the above run will produce a JSON file with failures, inspect and re-run stage 2 if need be.

Sample `../output/failed-tags.json` file is as follows:

```
[
  {
    "docker_image_reference": "openshift/origin-control-plane:latest",
    "imagestream_tag": "latest",
    "image_name": "",
    "destination_image": "image-benchmark/origin-control-plane:latest",
    "source_registry_in_image_tag": false,
    "source_image": "openshift/origin-control-plane:latest",
    "stderr": "time=\"2020-07-22T12:04:28-04:00\" level=fatal msg=\"Error initializing source docker://docker-registry-default.apps.alpatel-image-3110.mg.dog8code.com/openshift/origin-control-plane:latest: Error reading manifest latest in docker-registry-default.apps.alpatel-image-3110.mg.dog8code.com/openshift/origin-control-plane: name unknown\" ",
    "rc": 1
  }
]
```
