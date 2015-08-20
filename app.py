#!/usr/bin/env python3

import boto3
import pygraphviz as pgv

def check_vpcs(ec2, vpc):
    print(vpc.vpc_id)


if __name__ == '__main__':
    
    g = pgv.AGraph(directed=True)

    """
    print("-----------------")
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
        g.add_node(vpc.id, kind="VPC")
        for subnet in vpc.subnets.all():
            g.add_node(subnet.id, kind="subnet", az=subnet.availability_zone)
            g.add_edge(vpc.id, subnet.id)

            for instance in subnet.instances.all():
                g.add_node(instance.id, kind=instance)
                g.add_edge(subnet.id, instance.id)

        for elb in [elb for elb in elbs if elb["VPCId"] == vpc.id]:
            g.add_node(elb["LoadBalancerName"], kind="ELB")
            for instance in elb["Instances"]:
                g.add_edge(elb["LoadBalancerName"], instance["InstanceId"])
                
    g.draw("ttt.png", prog="dot")

    
