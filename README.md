# aws-cnf-attributes-macro

This is a sample template for aws-cnf-attributes-macro - Below is a brief explanation of what we have generated for you:

```bash
.
├── README.md                   <-- This instructions file
├── cnf_attributes_macro        <-- Source code for a lambda function
│   ├── __init__.py
│   ├── app.py                  <-- Lambda function code
│   └── requirements.txt        <-- Python dependencies
├── template.yaml               <-- SAM Template
└── tests                       <-- Unit tests
    └── unit
        ├── __init__.py
        └── test_handler.py
```

## Requirements

* AWS CLI already configured with at least PowerUser permission
* [Python 3 installed](https://www.python.org/downloads/)
* [Docker installed](https://www.docker.com/community-edition)
* [Python Virtual Environment](http://docs.python-guide.org/en/latest/dev/virtualenvs/)

## Setup process

### Building the project

[AWS Lambda requires a flat folder](https://docs.aws.amazon.com/lambda/latest/dg/lambda-python-how-to-create-deployment-package.html) with the application as well as its dependencies. When you make changes to your source code or dependency manifest,
run the following command to build your project local testing and deployment:

```bash
sam build
```

By default, this command writes built artifacts to `.aws-sam/build` folder.

## Packaging and deployment

Firstly, we need a `S3 bucket` where we can upload our Lambda functions packaged as ZIP before we deploy anything - If you don't have a S3 bucket to store code artifacts then this is a good time to create one:

```bash
aws s3 mb s3://BUCKET_NAME
```

Next, run the following command to package our Lambda function to S3:

```bash
sam package \
    --output-template-file packaged.yaml \
    --s3-bucket REPLACE_THIS_WITH_YOUR_S3_BUCKET_NAME
```

Next, the following command will create a Cloudformation Stack and deploy your SAM resources.

```bash
sam deploy \
    --template-file packaged.yaml \
    --stack-name aws-cnf-attributes-macro \
    --capabilities CAPABILITY_IAM
```

After deployment is complete you can deploy the following template to demonstrate the usage of the macro:

```bash
aws cloudformation deploy \
    --stack-name macro-example \
    --template-file bare_buckets.yaml \
    --capabilities CAPABILITY_IAM
```

To show the resulting tags, execute the following command:

```bash
aws resourcegroupstaggingapi get-resources
    --tag-filters Key=aws:cloudformation:stack-name,Values=macro-example \
    --out table
```

## Testing

We use **Pytest** and **pytest-mock** for testing our code and you can install it using pip: ``pip install pytest pytest-mock``

Next, we run `pytest` against our `tests` folder to run our initial unit tests:

```bash
python -m pytest tests/ -v
```

**NOTE**: It is recommended to use a Python Virtual environment to separate your application development from  your system Python installation.

## Appendix

### Python Virtual environment

Preparation steps for `pyenv` and `pipenv`:

1. [Install `pyenv`](https://github.com/pyenv/pyenv#installation)
1. Check out which Python version is installed (`pyenv versions`), install a `3.6` version if not present (`pyenv install 3.6.7`)
    * If the install doesn't work, possibly use `CFLAGS="-I$(brew --prefix openssl)/include -I$(xcrun --show-sdk-path)/usr/include" \\nLDFLAGS="-L$(brew --prefix openssl)/lib" \\npyenv install -v 3.6.7`
1. [Install `pipenv`](https://github.com/pypa/pipenv#installation)

Execute the following shell commands within the repository folder:

1. `export PIPENV_VENV_IN_PROJECT=1`
1. `pipenv install --dev`
1. `pipenv run pytest -v`
