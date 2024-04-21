import pulumi
import pulumi_archive as archive
import pulumi_aws as aws

# Create an IAM role that will be used by the Lambda function
lambda_role = aws.iam.Role("lambdaRole",
    assume_role_policy="""{
        "Version": "2012-10-17",
        "Statement": [{
            "Action": "sts:AssumeRole",
            "Principal": {
                "Service": "lambda.amazonaws.com"
            },
            "Effect": "Allow",
            "Sid": ""
        }]
    }""")

# Attach a policy to the IAM role that grants the Lambda function the
# necessary execution rights
policy_attachment = aws.iam.RolePolicyAttachment("lambdaRoleAttach",
    role=lambda_role.name,
    policy_arn="arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole")

# Create Lambda Archive
lambda_archive = archive.get_file(type="zip",
    source_file="app/lambda.py",
    output_path="dist/tester-lambda.zip")

# Create the Lambda function
lambda_function = aws.lambda_.Function("testerLambda",
    code=pulumi.FileArchive("dist/tester-lambda.zip"),
    role=lambda_role.arn,
    handler="lambda.handler",
    source_code_hash=lambda_archive.output_base64sha256,
    runtime="python3.12")

# Create the Lambda function URL
function_url = aws.lambda_.FunctionUrl("testerFunctionUrl",
    function_name=lambda_function.name,
    authorization_type="NONE",
    cors={
        "allowCredentials": False,
        # Define the specific origins and methods you want to allow
        "allowHeaders": ["*"],
        "allowMethods": ["POST", "GET"],
        "allowOrigins": ["*"],
    })

# Export the function URL so it can be accessed
pulumi.export('tester_lambda_function_url', function_url.function_url)
