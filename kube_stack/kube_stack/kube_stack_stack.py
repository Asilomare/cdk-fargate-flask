# Import the required libraries
from aws_cdk import (
    aws_ecs as ecs,
    aws_ecs_patterns as ecs_patterns,
    aws_ec2 as ec2,
    aws_rds as rds,
    aws_elasticloadbalancingv2 as elbv2,
    Stack, App
)
from constructs import Construct

# Create the CDK stack
class KubeStackStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        #create a VPC
        vpc = ec2.Vpc(self, "MyVpc",
            nat_gateways=1
            )
        # Create an ECS cluster
        cluster = ecs.Cluster(self, "Cluster", vpc=vpc)
       
        # Define a Fargate task
        task = ecs.FargateTaskDefinition(self, "Task", memory_limit_mib=1024, cpu=512)
        
        # Add the Flask container to the Fargate task
        container = task.add_container("FlaskContainer", image=ecs.ContainerImage.from_asset("kube_stack/app"),
            logging=ecs.AwsLogDriver(stream_prefix="EventLogsContainer", mode=ecs.AwsLogDriverMode.NON_BLOCKING),
            port_mappings=[ecs.PortMapping(container_port=80)]
            )
        
        fargate_service = ecs_patterns.ApplicationLoadBalancedFargateService(
            self, "Service",
            cluster=cluster,
            desired_count=3,
            task_definition=task,
            public_load_balancer=True,
        )
        
# Create the CDK app and deploy the stack
app = App()
KubeStackStack (app, "MyStack")
app.synth()
