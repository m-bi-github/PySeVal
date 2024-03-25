# pyseval

pyseval stands for PYthon SEmantiv model VALidations.  
It is a python package and cli app that allows the user to validate power bi semantic models by specifying validation specs in json files consisting of dax queries and their expected results.  
pyseval will execute the dax queries against the specified semantic model and compare the resulting table with the expected table provided in the validations spec file.

## Validations Spec Json File

The application uses a so-called validations spec file in json format as input.  
This file has a corresponding json schema as defined in this github repo [pyseval_json_schema](https://github.com/m-bi-github/pyseval_json_schema).

## Authentication

 The app authenticates using [DefaultAzureCredential](https://learn.microsoft.com/en-us/python/api/overview/azure/identity-readme?view=azure-python#defaultazurecredential).  
 This means you have multiple options depending on your use case. I suggest to use the azure cli login for interactive usage and a service principal with the corresponding environment variables when usage is in an automated e.g. CI/CD case.
