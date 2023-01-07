
#ran into a problem involving fargate profiles in the deletion process, wrote this script to delete the eks cluster and its stack
#assumes already configured aws cli

#chmod +x deletion_script.sh
#bash deletion_script.sh

# Get the name of the cluster to delete from the command line argument
cluster_name=$1

# Get a list of all EKS clusters
clusters=$(aws eks list-clusters --output text | cut -f2)

# Iterate through the list of clusters
for cluster in $clusters
do
    # Check if the current cluster is the one specified by the command line argument
    if [ "$cluster" == "$cluster_name" ]
    then
        # Get a list of Fargate profiles for the cluster
        profiles=$(aws eks list-fargate-profiles --cluster-name $cluster --output text | cut -f2)

        # Iterate through the list of profiles
        for profile in $profiles
        do
            # Delete the Fargate profile
            aws eks delete-fargate-profile --cluster-name $cluster --fargate-profile-name $profile

            # Wait until the Fargate profile is in DELETE_COMPLETE state
            while true
            do
                status=$(aws eks describe-fargate-profile --cluster-name $cluster --fargate-profile-name $profile --output json | jq -r '.fargateProfile.status')
                if [ "$status" == "DELETE_COMPLETE" ]
                then
                    break
                fi
                sleep 10
            done
        done

        # Get the CloudFormation stack name for the cluster
        stack_name=$(aws eks describe-cluster --name $cluster --output json | jq -r '.ResourcesVpcConfig.StackName')

        # Delete the CloudFormation stack
        aws cloudformation delete-stack --stack-name $stack_name

    fi
done
