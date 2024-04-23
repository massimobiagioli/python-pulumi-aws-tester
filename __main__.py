import pulumi
import pulumi_archive as archive
import pulumi_aws as aws
import subprocess


def cleanup():
    resources = [
        'dist',
        'layer',
        'out'
    ]

    for resource in resources:
        subprocess.check_call(f'rm -rf {resource}'.split())
        

def package_layer():
    subprocess.check_call('pip install --platform manylinux2014_x86_64 --implementation cp --only-binary=:all: --upgrade -r requirements_layer.txt -t layer/python/'.split())    


def copy_app_files():
    subprocess.check_call('mkdir dist'.split())
    subprocess.check_call('cp -r app/. dist/app'.split())


# Clean up the dist and layer directories
cleanup()

lambda_role = aws.iam.Role(
    resource_name="lambdaRole",
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
policy_attachment = aws.iam.RolePolicyAttachment(
    resource_name="lambdaRoleAttach",
    role=lambda_role.name,
    policy_arn="arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole")

# Create lambda layer
package_layer()

layer_archive = archive.get_file(
    type="zip",
    source_dir="layer",
    output_path="out/lambda_layer.zip"
)

lambda_layer = aws.lambda_.LayerVersion(
    resource_name="testerLambdaLayer",
    layer_name="testerLambdaLayer",
    description="A layer for the tester lambda function",
    code=pulumi.FileArchive("out/lambda_layer.zip"),
    source_code_hash=layer_archive.output_base64sha256,
    compatible_runtimes=["python3.12"],
)
    
# Create Lambda Archive
copy_app_files()

lambda_archive = archive.get_file(
    type="zip",    
    source_dir="dist",
    output_path="out/tester-lambda.zip",        
)

# Create the Lambda function
lambda_function = aws.lambda_.Function(
    resource_name="testerLambda",
    code=pulumi.FileArchive("out/tester-lambda.zip"),
    role=lambda_role.arn,
    handler="app.lambda.handler",
    source_code_hash=lambda_archive.output_base64sha256,
    layers=[lambda_layer.arn],
    runtime="python3.12"
)

# Create the Lambda function URL
function_url = aws.lambda_.FunctionUrl(
    resource_name="testerFunctionUrl",
    function_name=lambda_function.name,
    authorization_type="NONE",
    cors={
        "allowCredentials": False,
        # Define the specific origins and methods you want to allow
        "allowHeaders": ["*"],
        "allowMethods": ["POST", "GET"],
        "allowOrigins": ["*"],
    }
)

# Export the function URL so it can be accessed
pulumi.export('tester_lambda_function_url', function_url.function_url)
