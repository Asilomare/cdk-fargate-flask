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
        
        # Create the RDS PostgreSQL database
        database = rds.DatabaseInstance(
            self, "Database",
            engine=rds.DatabaseInstanceEngine.POSTGRES,
            credentials=rds.Credentials.from_generated_secret("rdsCreds"),
            instance_type=ec2.InstanceType.of(
                instance_class=ec2.InstanceClass.BURSTABLE3,
                instance_size=ec2.InstanceSize.SMALL
            ),
            vpc=vpc,
            deletion_protection=False
        )
        
                # Define a Fargate task
        task = ecs.FargateTaskDefinition(self, "Task", memory_limit_mib=1024, cpu=512)
        
        # Add the Flask container to the Fargate task
        container = task.add_container("FlaskContainer", image=ecs.ContainerImage.from_asset("kube_stack/app"),
            logging=ecs.AwsLogDriver(stream_prefix="EventLogsContainer", mode=ecs.AwsLogDriverMode.NON_BLOCKING),
            port_mappings=[ecs.PortMapping(container_port=80)],
            environment={"SQLALCHEMY_DATABASE_URI": database.secret.secret_value.unsafe_unwrap()}
            )
        #container.add_port_mappings(container_port=80, protocol=ecs.Protocol.TCP)
        
        fargate_service = ecs_patterns.ApplicationLoadBalancedFargateService(
            self, "Service",
            cluster=cluster,
            desired_count=1,
            task_definition=task,
            public_load_balancer=True,
        )
        
        
        
        # Create a public load balancer that will route traffic to the Fargate task
        ##lb = elbv2.ApplicationLoadBalancer(self, "LoadBalancer", vpc=vpc, internet_facing=True)
        ##lb.connections.allow_from_any_ipv4(ec2.Port.tcp(80))
        ##listener = lb.add_listener("Listener", port=80)
        
        # Add the Fargate task as a target to the target group
       
       
       
        # Create a service that will run the Fargate task and associate it with the load balancer
        ##service = ecs.FargateService(self, "Service", cluster=cluster, task_definition=task, desired_count=1)
        ##listener.add_targets("listener_target", port=80, targets=[service])
        
        
# Create the CDK app and deploy the stack
app = App()
KubeStackStack (app, "MyStack")
app.synth()



"""
# Import the required libraries
from aws_cdk import (
    aws_ecs as ecs,
    aws_ecs_patterns as ecs_patterns,
    aws_ec2 as ec2,
    aws_rds as rds,
    Stack, App
)
from constructs import Construct

# Create the CDK stack
class KubeStackStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        vpc = ec2.Vpc(self, "MyVpc",
            nat_gateways=1
            )
        
        # Create the RDS PostgreSQL database
        database = rds.DatabaseInstance(
            self, "Database",
            engine=rds.DatabaseInstanceEngine.POSTGRES,
            credentials=rds.Credentials.from_generated_secret("rdsCreds"),
            instance_type=ec2.InstanceType.of(
                instance_class=ec2.InstanceClass.BURSTABLE3,
                instance_size=ec2.InstanceSize.SMALL
            ),
            vpc=vpc,
            deletion_protection=False
        )

        # Create an ECS cluster
        cluster = ecs.Cluster(self, "Cluster", vpc=vpc)

        # Create a Fargate service for the Flask application
        fargate_service = ecs_patterns.ApplicationLoadBalancedFargateService(
            self, "Service",
            cluster=cluster,
            task_image_options={
                "image": ecs.ContainerImage.from_asset("kube_stack/app/"),
                "container_name": "app",
                "container_port": 5000,
                "environment": {
                    "SQLALCHEMY_DATABASE_URI": database.secret.secret_value.unsafe_unwrap(),
                }
            },
            desired_count=1,
            public_load_balancer=True,
        )

# Create the CDK app and deploy the stack
app = App()
KubeStackStack (app, "MyStack")
app.synth()
"""