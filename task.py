import boto3
import logging
import sys
from pprint import pprint

def describe_public_buckets():
    public_buckets = []
    try:
        s3client = boto3.client('s3')
        list_bucket_response = s3client.list_buckets()

        for bucket_dictionary in list_bucket_response['Buckets']:
            bucket_acl_response = s3client.get_bucket_acl(Bucket=bucket_dictionary['Name'])
            for grant in bucket_acl_response['Grants']:
                try:  
                    if grant['Grantee']['URI']:
                        demo = str(grant['Grantee']['URI'])
                        if demo.endswith('global/AllUsers'):
                            public_buckets.append(bucket_dictionary['Name'])
                except KeyError:
                    pass
        return list(set(public_buckets))
    except:
        err = 'describe_public_buckets Failed! '
        for e in sys.exc_info():
            err += str(e)
            print(err)

if __name__ == '__main__':
    print(describe_public_buckets())
