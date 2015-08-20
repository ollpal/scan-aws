#!/usr/bin/env python3

import boto3

if __name__ == '__main__':
    
    """
    s3 = boto3.resource('s3')
    for bucket in s3.buckets.all():
        print(bucket.name)
    """

    elb = boto3.client('elb')

    response = elb.describe_load_balancers()
    elbs = response["LoadBalancerDescriptions"];
    while "NextMarker" in response:
        response = elb.describe_load_balancers(Marker=response["NextMarker"])
        elbs += response["LoadBalancerDescriptions"];

    ec2 = boto3.resource("ec2")
    for vpc in ec2.vpcs.all():
        print("vpc: {}".format(vpc.id))
        for subnet in vpc.subnets.all():
            print("subnet: {} ({})".format(subnet.id, subnet.availability_zone))
            for instance in subnet.instances.all():
                print("instance: {}".format(instance.id))
        for elb in [elb for elb in elbs if elb["VPCId"] == vpc.id]:
            print("ELB: {}".format(elb["LoadBalancerName"]))
            print("instances:")
            for instance in elb["Instances"]:
                print(" - {}".format(instance["InstanceId"])) 
                
