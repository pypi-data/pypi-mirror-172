import os
import boto3
import botocore

import pandas as pd
import awswrangler as wr

from functools import partial, reduce

#####################

def session_from_credentials(creds, region):
    try:
        return boto3.session.Session(
            region_name=region,
            aws_access_key_id=creds["AccessKeyId"],
            aws_secret_access_key=creds["SecretAccessKey"],
            aws_session_token=creds["SessionToken"]
        )
    except:
        return None

#####################

def assume_role(**params):

    region = params.get('region', 'us-east-1')
    access_key_id = params.get('access_key_id')
    secret_access_key = params.get('secret_access_key')

    account_id = params.get('accountId')
    role_name = params.get('roleName')
    session_name = params.get('sessionName')
    role_arn = f'arn:aws:iam::{account_id}:role/{role_name}'
    
    try:
        if access_key_id:
            sts = boto3.client('sts',
                               region_name=region,
                               aws_access_key_id=access_key_id,
                               aws_secret_access_key=secret_access_key)
        else:
            sts = boto3.client('sts')
        assumed_role = sts.assume_role(RoleArn=role_arn,
                                       RoleSessionName=session_name)
        credentials = assumed_role.get('Credentials')
    except:
        print(account_id, 'Assume error')
        credentials = None

    return session_from_credentials(credentials, region)

#####################

def athena(session, db, query):
    return partial(wr.athena.read_sql_query,
                   database=db,
                   boto3_session=session)(query)
