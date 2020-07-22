# Stage 2: imagestream-coopy

Before running this the internal registry for source and desination clusters have to be exposed. For a 3.x 
cluster the registry is exposed by default. If for some reason it is not, follow the [docs](https://docs.openshift.com/container-platform/3.11/install_config/registry/securing_and_exposing_registry.html#overview) 
For a 4.x cluster please follow the docs [here](https://docs.openshift.com/container-platform/4.5/registry/securing-exposing-registry.html) 
to expose the registry.

Once both the registries are exposed, you should be able to get the registry url, username and password. Please
follow the following steps to setup vars file for stage 2.

Steps to run:

1. Get the source registry url, username and password
2. Get the destination registry url, username and password
3. `cd 2_imagestream_copy`
4. Point your kubeconfig to destination cluster or login to destination cluster 
5. copy the vars example file `cp vars/imagestream-copy.yml.example vars/imagestream-copy.yml` and edit it
   to populate the registry data
6. run the ansible playbook `ansible-playbook imagestream-copy.yml`
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
