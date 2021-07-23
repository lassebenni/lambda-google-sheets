from cdk_stack.sns_google_sheets_lambda_stack import SNSGoogleSheetsLambdaStack
from aws_cdk import (
    core
)

app = core.App()
env = {'region': 'eu-west-1'}
SNSGoogleSheetsLambdaStack(app, "SNSGoogleSheetsLambdaStack", env=env)
app.synth()
