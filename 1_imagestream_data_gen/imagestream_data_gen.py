import json
import os

import urllib3
import yaml
from kubernetes import config
from openshift.dynamic import DynamicClient

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

script_dir = os.path.dirname(os.path.realpath(__file__))
output_dir = os.path.join(script_dir, '../output')

try:
    k8s_client = config.new_client_from_config()
    dyn_client = DynamicClient(k8s_client)
except Exception as e:
    print("\n[!] Failed while setting up OpenShift client. Ensure KUBECONFIG is set. ")
    print(e)
    exit(1)

# Ensure KUBECONFIG is set to source cluster by checking for OpenShift v3 in version endpoint
try:
    kube_minor_version = dyn_client.version.get("kubernetes", {}).get("minor", "").split("+")[0]
    if int(kube_minor_version) > 11:
        print(
            "\n[!] [WARNING] KUBECONFIG should be set to source cluster (likely OCP 3.x) for 'Stage 1', but OCP 4.x "
            "cluster detected.")
        print("[!] [WARNING] Detected k8s version: {}\n".format(
            dyn_client.version.get("kubernetes", {}).get("gitVersion", "")))
        selection = input("[?] Press 'Enter' to quit, or type 'i' to ignore warning: ")
        if 'i' not in selection:
            print("Exiting...")
            exit(1)
except Exception as e:
    print("[!] Failed to parse OpenShift version.")
    print(e)


# Object serving as 'get' default for empty results
class EmptyK8sResult:
    __dict__ = {}


emptyDict = EmptyK8sResult()

# Make output dir if doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

with open(script_dir + '/vars/imagestream-data-gen.yml') as f:
    input_data = yaml.load(f, Loader=yaml.FullLoader)

node_list = []
output = []

for namespace in input_data['namespace_to_migrate']:
    print("Processing namespace: [{}]".format(namespace))
    v1_namespaces = dyn_client.resources.get(api_version='v1', kind='Namespace')
    try:
        ns = v1_namespaces.get(name=namespace)
        ns_out = {'namespace': namespace, 'annotations': ns.metadata.get("annotations", emptyDict).__dict__}
        output.append(ns_out)
    except Exception as e:
        # TODO: figure out a way to report the missing namespace
        print("\n[WARNING] v1/namespace not found: {}\n".format(namespace))
        print(e)

ns_data_file = os.path.join(output_dir, 'namespace-data.json')
with open(ns_data_file, 'w') as f:
    json.dump(output, f, indent=4)
    print("[!] Wrote {}".format(ns_data_file))

namespaces = output
output = []

for item in namespaces:
    namespace = item["namespace"]
    print("Processing ImageStreams for namespace: [{}]".format(namespace))

    imagestreams = dyn_client.resources.get(api_version='image.openshift.io/v1', kind='ImageStream')
    imagestreams_list = imagestreams.get(namespace=namespace)

    for imagestream in imagestreams_list.items:
        # print(imagestream)
        tags_to_process = []
        tags_to_migrate = []
        if imagestream.status.tags is None:
            continue
        if imagestream.spec.tags is None:
            for tag in imagestream.status.tags:
                tags_to_process.append(tag.name)
        else:
            for tag in imagestream.spec.tags:
                if tag.kind == "ImageStreamTag":
                    continue
                tags_to_process.append(tag.name)
        # print(imagestream.metadata.name, tags_to_process)
        source_registry_url = imagestream.status.dockerImageRepository.split("/")[0]
        for tag in imagestream.status.tags:
            for image in tag.items:
                # print(image.dockerImageReference)
                image_reference_split = image.dockerImageReference.split("/")
                if len(image_reference_split) < 3 or source_registry_url == image_reference_split[0]:
                    docker_image_reference = image.dockerImageReference
                    imagestream_tag = ""
                    if tag.tag is not None:
                        imagestream_tag = tag.tag
                    image_name = image.image
                    source_registry_in_image_tag = len(image_reference_split) == 3
                    if len(image_reference_split) >= 2:
                        destination_image_tag = imagestream.metadata.namespace + "/" + imagestream.metadata.name + "@" \
                                                + imagestream_tag
                    else:
                        destination_image_tag = image_name + "@" + imagestream_tag
                    # destination_image_tag = docker_image_reference.split("@")[0] + "@" + imagestream_tag
                    # source_registry_in_image_tag = source_registry_url == image_reference_split[0]
                    # destination_image_tag = destination_image_tag.lstrip(source_registry_url + "/")
                    tags_to_migrate.append({
                        "docker_image_reference": docker_image_reference,
                        "imagestream_tag": imagestream_tag,
                        "image_name": image_name,
                        "destination_image_tag": destination_image_tag,
                        "source_registry_in_image_tag": source_registry_in_image_tag,
                    })
                # else:
                # print(image)
        # print(tags_to_migrate)
        if len(tags_to_migrate) != 0:
            output.append({'imagestream_name': imagestream.metadata.name,
                           'imagestream_namespace': imagestream.metadata.namespace,
                           'tags': tags_to_migrate})

ns_data_file = os.path.join(output_dir, 'image-data.json')
with open(ns_data_file, 'w') as f:
    json.dump(output, f, indent=4)
    print("[!] Wrote {}".format(ns_data_file))
