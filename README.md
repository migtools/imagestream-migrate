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

### 2. Automation prerequisites

#### Virtualenv 
 * Installing Virtualenv
    ```
    python3 -m pip install --user virtualenv
    python3 -m venv env
    ```

 * Activate Virtualenv and install requirements
    ```
    source env/bin/activate
    pip install -r requirements.txt
    ```

 * Install selinux dependency if selinux is enabled
    ```
    pip install selinux
    ```

 * To update any requirements
    ```
    pip freeze &> requirements.txt
    ``` 

#### Without Virtualenv

```
pip3 install ansible==2.9.7 --user      # ansible 2.9
pip3 install kubernetes==11.0.0 --user  # kubernetes module for ansible
pip3 install openshift==0.11.2 --user   # openshift module for ansible
pip3 install PyYAML==5.1.1 --user       # pyyaml module for python
```

### 3. Set cluster authentication details
**Copy source and destination cluster KUBECONFIG files authenticated with  *cluster-admin* privileges to `auth` \
directory**
   1. Create `auth` directory inside of repository root:  `mkdir auth`
   1. Copy source cluster kubeconfig to `auth/KUBECONFIG_SRC`
   1. Copy destination cluster kubeconfig to `auth/KUBECONFIG_TARGET`
   
### 4. Set list of namespaces to migrate PVC data for
   1. Copy sample config file as starting point: 
      `cp 
      1_imagestream_data_gen/vars/imagestream-data-gen.yml.example 1_imagestream_data_gen/vars/imagestream-data-gen.yml`
   1. Edit `1_imagestream_data_gen/vars/imagestream-data-gen.yml`, adding list of namespaces for which ImageStream data 
       should be migrated
   
```
namespaces_to_migrate:
  - image-benchmark
  - image-playground
```
 
### 5. Familiarize with ImageStream migration automation

The `imagestream-migrate` tooling is designed to work in 2 stages :    

#### Stage 1 - Detect source cluster info (ImageStreams, Images) ([Stage 1 README](1_imagestream_data_gen))
```
1_imagestream_data_gen
````
This preliminary stage collects information about imageStreams, images and tags from the Source cluster. It creates a 
JSON report of collected data which will be consumed by the subsequent stage. 

**Note**: changes to the source cluster after completion of Stage 1 will not be considered by next stages. You can 
re-run stage 1 to refresh data as needed before running Stage 2.

#### Stage 2 - Migrate ImageStreams to destination cluster ([Stage 2 README](2_imagestream_copy))
```
2_imagestream_copy
````
Before running this stage please make sure both the source and the destination registries are accessible. Follow the 
stage documentation more details on how to run the stage.

If for some reason certain images failed to copy, they will be connected in `<output_dir>/failed-tags.json` file. In 
order to retry, send this file as input to stage 2 and try again.

**Note**: after completion of this stage, you will have ImageStreams created on the destination cluster.

### 6. Running the ImageStream migration
1. Run steps in: [1_imagestream_data_gen/README.md](1_imagestream_data_gen)
1. Run steps in: [2_imagestream_copy/README.md](2_imagestream_copy)
   
   
### 7. Run CAM in "no ImageStream migration" mode
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
 
  3. Create a MigPlan and MigMigration covering the same namespaces migrated with `pvc-migrate`.
 

   
