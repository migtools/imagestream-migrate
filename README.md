# imagestream-migrate


## Overview

`imagestrem-migrate` automates migration of ImageStream resources from OCP 3.x to OCP 4.x.


### Prerequisite steps

* The registries on source and destination should be accessed from the node where this
  tool is run from

## Usage
### 1. Clone this git repo

```
git clone https://github.com/konveyor/imagestream-migrate && cd imagestream-migrate
```

### 2. Prerequisites

#### Expose registries
A route is created for image registries on OpenShift 3 by default. No further action should be required.
If for some reason the registry is no exposed instructions are provided in the [OpenShift Documentation](https://docs.openshift.com/container-platform/3.11/install_config/registry/securing_and_exposing_registry.html#exposing-the-registry)

On OpenShift 4 registries are not exposed by default. To create a route run:  
`oc patch configs.imageregistry.operator.openshift.io/cluster --patch '{"spec":{"defaultRoute":true}}' --type=merge`

#### Install required software
Options using dnf or pip are provided below.

##### dnf
`dnf install ansible python3-openshift`

##### pip

```
pip3 install ansible==2.9.7 --user      # ansible 2.9
pip3 install kubernetes==11.0.0 --user  # kubernetes module for ansible
pip3 install openshift==0.11.2 --user   # openshift module for ansible
pip3 install PyYAML==5.1.1 --user       # pyyaml module for python
```

### 3. Run the ImageStream migration

#### Generate imagestream migration data
1. `cd 1_imagestream_data_gen`
1. Run steps in the [Stage 1 README](1_imagestream_data_gen)

**Note**: This preliminary stage collects information about imageStreams, images and tags from the Source cluster. It creates a
JSON report of collected data which will be consumed by the subsequent stage. Changes to the source cluster after completion of
Stage 1 will not be considered by next stages, but you may re-run stage 1 to refresh data as needed before running Stage 2.

#### Perform the image copy
1. `cd ..\2_imagestream_copy`
1. Run the steps in the [Stage 2 README](2_imagestream_copy)

If any images fail to copy, they will be list in the `<output_dir>/failed-tags.json` file. In
order to retry, use this file as input to stage 2.


### 4. Run CAM in "no ImageStream migration" mode
   1. Your ImageStreams/Images has been migrated. You can use CAM to migrate the remaining OpenShift resources, which
      can use the ImageStreams/Images migrated by this took.
   2. To run CAM in "no ImageStream migration" mode, modify the `MigrationController` resource on the
      *destination cluster* by swapping out the mig-controller image, then execute a migration as usual.

```
oc edit MigrationController -n openshift-migration
```
```
apiVersion: migration.openshift.io/v1alpha1
kind: MigrationController
metadata:
  name: migration-controller
  namespace: openshift-migration
spec:
  [...]
  mig_controller_image_fqin: quay.io/konveyor/mig-controller:release-1.2.2-hotfix-nopvs
  [...]
 ```

  3. Create a MigPlan and MigMigration covering the same namespaces migrated with `imagestream-migrate`.
