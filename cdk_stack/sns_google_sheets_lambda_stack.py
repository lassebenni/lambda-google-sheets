import os
from aws_cdk import (
    core,
    aws_lambda as _lambda,
    aws_sns as _sns,
    aws_sns_subscriptions as _subscriptions,
    aws_ecr,
    aws_iam as _iam
)


class SNSGoogleSheetsLambdaStack(core.Stack):
    use_pre_existing_image = False

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        func = self.create_google_sheets_lambda()
        topic = self.create_sns_google_sheets_topic()
        topic.add_subscription(_subscriptions.LambdaSubscription(func))

    def build_or_reuse_container_image(self, image_name: str):
        ##
        # If use_pre_existing_image is True
        # then use an image that already exists in ECR.
        # Otherwise, build a new image
        ##

        ##
        # ECR
        ##
        if (self.use_pre_existing_image):
            ##
            # Container was build previously, or elsewhere.
            # Use the pre-existing container
            ##
            ecr_repository = aws_ecr.Repository.from_repository_attributes(
                self,
                id="ECR",
                repository_arn='arn:aws:ecr:{0}:{1}'.format(
                    core.Aws.REGION, core.Aws.ACCOUNT_ID),
                repository_name=image_name
            )  # aws_ecr.Repository.from_repository_attributes

            ##
            # Container Image.
            # Pulled from the ECR repository.
            ##
            ecr_image = _lambda.EcrImageCode(
                repository=ecr_repository
            )  # aws_lambda.EcrImageCode

        else:
            ##
            # Create new Container Image.
            ##
            ecr_image = _lambda.EcrImageCode.from_asset_image(
                directory=os.path.join(os.getcwd(), image_name)
            )

        return ecr_image

    def create_lambda_function(self, image_name: str, env={}):
        ecr_image = self.build_or_reuse_container_image(image_name)

        return _lambda.Function(
            self,
            id=image_name,
            description=image_name,
            code=ecr_image,
            ##
            # Handler and Runtime must be *FROM_IMAGE*
            # when provisioning Lambda from Container.
            ##
            handler=_lambda.Handler.FROM_IMAGE,
            runtime=_lambda.Runtime.FROM_IMAGE,
            function_name=image_name,
            memory_size=128,
            reserved_concurrent_executions=10,
            timeout=core.Duration.minutes(15),
            environment=env
        )

    def create_google_sheets_lambda(self):
        env_vars = dict(
            GOOGLE_CLIENT_EMAIL=os.getenv('GOOGLE_CLIENT_EMAIL', ''),
            GOOGLE_CLIENT_ID=os.getenv('GOOGLE_CLIENT_ID', ''),
            GOOGLE_PRIVATE_KEY=os.getenv('GOOGLE_PRIVATE_KEY', ''),
            GOOGLE_PRIVATE_KEY_ID=os.getenv('GOOGLE_PRIVATE_KEY_ID', ''),
            GOOGLE_PROJECT_ID=os.getenv('GOOGLE_PROJECT_ID', '')
        )
        return self.create_lambda_function(
            'lambda_sns_google_sheets', env=env_vars)

    def create_sns_google_sheets_topic(self):
        return _sns.Topic(
            self,
            id='sns_google_sheets_topic',
            name='sns_google_sheets_topic',
            topic_name='sns_google_sheets_topic',
            display_name='sns_google_sheets_topic',
        )
