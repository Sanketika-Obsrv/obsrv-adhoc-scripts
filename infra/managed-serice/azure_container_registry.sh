#!/bin/bash

#####################################################################
# PREREQUISITES:
#
# You must be logged into sanketikahub docker account to pull 
# Sanketika's private images
#
# You must be logged into obsrvms.azurecr.io docker account to pull 
# Azure ACR private images
#
#####################################################################

usage() {                                 # Function: Print a help message.
  echo "Usage: azure_container_registry.sh [ -i --imagename ] [ -t --imagetag ]" 1>&2
}

while getopts :i:t:h: option
do
    case "${option}" in
    	h|--help) 
		  usage
		  exit
		  ;;
    	i|--imagename)
		  imagename=${OPTARG}
		  ;;
		t|--imagetag) 
		  imagetag=${OPTARG}
		  ;;
    esac
done

if [ -z $imagename ];then
	echo "Image name is a required parameter..."
	exit 1
fi

if [ -z $imagetag ];then
	echo "Image tag is a required parameter..."
	exit 1
fi

obsrv_azure_acr_url="obsrvms.azurecr.io"

docker_registry="docker.io"
quay_registry="quay.io"
k8s_registry="registry.k8s.io"

image_to_registry_mapping=(
"kube-state-metrics|$k8s_registry/kube-state-metrics"
"kube-webhook-certgen|$k8s_registry/ingress-nginx"
"cert-manager-cainjector|$quay_registry/jetstack"
"cert-manager-controller|$quay_registry/jetstack"
"cert-manager-ctl|$quay_registry/jetstack"
"cert_manager_ctl|$quay_registry/jetstack"
"kube_rbac_proxy|$quay_registry/brancz"
"prometheus_config_reloader|$quay_registry/prometheus-operator"
)

image_registry="$docker_registry/sanketikahub"

for ind in "${!image_to_registry_mapping[@]}"; do
	if [[ $(echo ${image_to_registry_mapping[$ind]} | fgrep -w "$imagename") ]]; then
		image_registry=$(echo "${image_to_registry_mapping[$ind]}" | awk -F'|' '{print $2}')
		break
	fi
done

echo "$image_registry/$imagename:$imagetag"
docker pull "$image_registry/$imagename:$imagetag"
if [ $? -ne 0 ]; then
	echo "Pulling image $image_registry/$imagename:$imagetag failed..."
	exit 1
fi

# docker images --no-trunc --quiet $image_registry/$imagename:$imagetag

docker tag "$image_registry/$imagename:$imagetag" "$obsrv_azure_acr_url/$imagename:$imagetag"
if [ $? -ne 0 ]; then
	echo "Docker tag command failed for image $image_registry/$imagename:$imagetag ..."
	exit 1
fi

docker push "$obsrv_azure_acr_url/$imagename:$imagetag"
if [ $? -ne 0 ]; then
	echo "Pushing image $obsrv_azure_acr_url/$imagename:$imagetag failed..."
	exit 1
fi