### Pushing a image to ACR
#### Pre-reqs
```
####################################################################
# You must be logged into sanketikahub docker account to pull 
# Sanketika's private images
#
# You must be logged into obsrvms.azurecr.io docker account to pull 
# Azure ACR private images
#
#####################################################################
```
* Using the following command to tag the image and push to ACR
```
azure_container_registry.sh [ -i --imagename ] [ -t --imagetag ]
```