
**Deploy Application:**\
Clone repo
- git clone https://github.com/Asilomare/cdk-fargate-flask ./
 
Move directories
- cd kube_stack

Activate virtual env
- source .venv/bin/activate

Install dependancies
- pip install -r requirements.txt
- npm install

Deploy application
- cdk deploy

**Test Application:**\
Find the output of the stack
- aws cloudformation describe-stacks --stack-name KubeStackStack --query 'Stacks[0].Outputs' 

Open source load generator
- docker run -it --rm ddosify/ddosify
- ddosify -t <put the output link here> -n <request_number>

**Modify Application:**\
On line 37 of /kube_stack/kube_stack_stack.py, change desired_count to the number of instances required\
then deploy changes
- cdk deploy
