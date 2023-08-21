from dotenv import load_dotenv
import os

import boto3
import pandas as pd


class S3Connection(object):
    def __init__(self):
        load_dotenv()

        # use in dev environment
        # self._AWS_S3_BUCKET = os.getenv("AWS_S3_BUCKET")
        # self._AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY")
        # self._AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

        # use in production
        self._AWS_S3_BUCKET = str(os.environ['AWS_S3_BUCKET'])
        self._AWS_ACCESS_KEY_ID = str(os.environ['AWS_ACCESS_KEY'])
        self._AWS_SECRET_ACCESS_KEY = str(os.environ['AWS_SECRET_ACCESS_KEY'])

        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=self._AWS_ACCESS_KEY_ID,
            aws_secret_access_key=self._AWS_SECRET_ACCESS_KEY,
        )

    def read_df_cnel_latlong(self):
        response = self.s3_client.get_object(Bucket=self._AWS_S3_BUCKET, Key="files/df_gye.csv")

        status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")

        if status == 200:
            print(f"Successful S3 get_object response. Status - {status}")
            df_cnel_latlong = pd.read_csv(response.get("Body"))
        else:
            print(f"Unsuccessful S3 get_object response. Status - {status}")

        df_cnel_latlong['cluster_2d'] = df_cnel_latlong['cluster_2d'].astype("string")
        df_cnel_latlong['cluster'] = df_cnel_latlong['cluster'].astype("string")
        df_cnel_latlong['cluster_dbscan_2d'] = df_cnel_latlong['cluster_dbscan_2d'].astype("string")
        df_cnel_latlong['estrato'] = df_cnel_latlong['estrato'].astype("string")
        
        return df_cnel_latlong
