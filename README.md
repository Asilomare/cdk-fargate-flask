bash $
Deploy Application:
clone repo
  - git clone https://github.com/Asilomare/cdk-fargate-flask ./
 move directories <br />
  - cd kube_stack
 activate virtual env
  - source .venv/bin/activate
 install dependancies_
  - pip install -r requirements.txt
  - npm install
 deploy application
  - cdk deploy

Test Application:
  find the output of the stack
  - aws cloudformation describe-stacks --stack-name KubeStackStack --query 'Stacks[0].Outputs' 
  open source load generator
  - docker run -it --rm ddosify/ddosify
  - ddosify -t <put the output link here> -n <request_number>
  
Modify Application:
  on line 37 of /kube_stack/kube_stack_stack.py, change desired_count to the number of instances required
  then deploy changes
  -cdk deploy
