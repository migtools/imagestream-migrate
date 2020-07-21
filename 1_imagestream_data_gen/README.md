# Stage 1: imagestream-data-gen

This stage will take list of namespaces in which imagestreams are to migrated as input and output two files 
`namespace-data.json` and `image-data.json` in `../output/` directory

The `../output/image-data.json` will have the list of  imgestreams that have tags that are stored in local image 
registry. They will be migrated in order of creation, so that the order is preserved at the destination.

Steps to run:

1. point the kubeconfig to source cluster and login as admin
2. `cd 1_imagestream_data_gen` 
3. copy the vars example file `cp vars/imageestream-data-gen.yml.example vars/imageestream-data-gen.yml`
4. run the python script `python3 imagestream_data_gen.py`

Sample `../output/image-data.json` file is as follows:

```
[
    {
        "imagestream_name": "busybox",
        "imagestream_namespace": "image-benchmark",
        "tags": [
            {
                "docker_image_reference": "busybox@sha256:2131f09e4044327fd101ca1fd4043e6f3ad921ae7ee901e9142e6e36b354a907",
                "imagestream_tag": "latest",
                "image_name": "sha256:2131f09e4044327fd101ca1fd4043e6f3ad921ae7ee901e9142e6e36b354a907"
            }
        ]
    },
    {
        "imagestream_name": "dot-net-image",
        "imagestream_namespace": "image-benchmark",
        "tags": [
            {
                "docker_image_reference": "docker-registry.default.svc:5000/image-benchmark/dot-net-image@sha256:cbd85abc68e79996913a90459c9ad6ff09e0151ba0a96bbe5fdcd6e5c340375d",
                "imagestream_tag": "latest",
                "image_name": "sha256:cbd85abc68e79996913a90459c9ad6ff09e0151ba0a96bbe5fdcd6e5c340375d"
            }
        ]
    },
    {
        "imagestream_name": "musicstore",
        "imagestream_namespace": "image-benchmark",
        "tags": [
            {
                "docker_image_reference": "docker-registry.default.svc:5000/image-benchmark/musicstore@sha256:2554658657b8deb9aea4381986e49a88c163dabe38930b8777822024ce162fb7",
                "imagestream_tag": "latest",
                "image_name": "sha256:2554658657b8deb9aea4381986e49a88c163dabe38930b8777822024ce162fb7"
            }
        ]
    },
    {
        "imagestream_name": "origin-control-plane",
        "imagestream_namespace": "image-benchmark",
        "tags": [
            {
                "docker_image_reference": "openshift/origin-control-plane:latest",
                "imagestream_tag": "latest",
                "image_name": ""
            }
        ]
    },
    {
        "imagestream_name": "python36-image",
        "imagestream_namespace": "image-benchmark",
        "tags": [
            {
                "docker_image_reference": "docker-registry.default.svc:5000/image-benchmark/python36-image@sha256:bfb24b961c46e5de9fd0f902085950ebb9eeb0533a06d4eec9113d4d7e1c7841",
                "imagestream_tag": "latest",
                "image_name": "sha256:bfb24b961c46e5de9fd0f902085950ebb9eeb0533a06d4eec9113d4d7e1c7841"
            }
        ]
    },
    {
        "imagestream_name": "time",
        "imagestream_namespace": "image-benchmark",
        "tags": [
            {
                "docker_image_reference": "docker-registry.default.svc:5000/image-benchmark/time@sha256:1196a003994e28d84dd5504bf865cb411bcef1ff9f962146dd2c991f6673cbd8",
                "imagestream_tag": "latest",
                "image_name": "sha256:1196a003994e28d84dd5504bf865cb411bcef1ff9f962146dd2c991f6673cbd8"
            },
            {
                "docker_image_reference": "docker-registry.default.svc:5000/image-benchmark/time@sha256:e657280d6bb690c4eb2e1384598cba802fe29a77bacea86889194ac1cc4d4be3",
                "imagestream_tag": "latest",
                "image_name": "sha256:e657280d6bb690c4eb2e1384598cba802fe29a77bacea86889194ac1cc4d4be3"
            },
            {
                "docker_image_reference": "docker-registry.default.svc:5000/image-benchmark/time@sha256:253c98ed23b04b7062b5fabea19ecff1808ae0f74da6b05d6979fc179bbf6f09",
                "imagestream_tag": "latest",
                "image_name": "sha256:253c98ed23b04b7062b5fabea19ecff1808ae0f74da6b05d6979fc179bbf6f09"
            }
        ]
    }
]
```
