#!/bin/bash
# Copyright (C) 2018-2021 Intel Corporation
# SPDX-License-Identifier: Apache-2.0

#Checking kubernetes is installed or not
echo "Checking Kuberentes is installed or not"

if [[ $(which kubectl) && $(kubectl version) ]]; then
         echo "Kubernetes is installed"

	 echo "Creating Namespace monitoring"
	 
	 kubectl create namespace monitoring
	 
	 echo "checking the namespace"
	 
	 kubectl get namespace
	 
	 echo "Creating prometheus and grafana"
	 
	 kubectl create -f .
     else
         echo "Install Kubernetes from devtool"
fi

