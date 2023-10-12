# Description

This is an aws event-driven microservices example



## Useful commands for infra

* `npm run build`   compile typescript to js
* `npm run watch`   watch for changes and compile
* `npm run test`    perform the jest unit tests
* `cdk bootstrap`   deploy usually named CDKToolkit, which contains resources that the CDK CLI and constructs use during the deployment process
* `cdk deploy`      deploy this stack to your default AWS account/region
* `cdk diff`        compare deployed stack with current state
* `cdk synth`       emits the synthesized CloudFormation template

## Tests
### Unit tests
### Integration tests
Run tests from tests directory. API should be deployed before you can run integration tests.
Pass api url of newly deployed API to tests:
pytest integration/test_basket.py --api_url https://tv12345.execute-api.eu-west-1.amazonaws.com/prod/


## Nice to have
* separate databases for tests