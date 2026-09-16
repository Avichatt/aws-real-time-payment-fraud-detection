import os
import boto3
from dotenv import load_dotenv

load_dotenv()

AWS_REGION = os.getenv("AWS_REGION", "ap-south-1")
BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

RAW_FILE = "data/raw/transactions.csv"
SCORED_FILE = "reports/scored_transactions.csv"

s3 = boto3.client(
    "s3",
    region_name=AWS_REGION
)


def upload_file(local_file, s3_key):
    if not os.path.exists(local_file):
        print(f"File not found: {local_file}")
        return

    s3.upload_file(
        local_file,
        BUCKET_NAME,
        s3_key
    )

    print(
        f"Uploaded {local_file} "
        f"to s3://{BUCKET_NAME}/{s3_key}"
    )


if __name__ == "__main__":
    if not BUCKET_NAME:
        raise ValueError(
            "S3_BUCKET_NAME is not configured."
        )

    upload_file(
        RAW_FILE,
        "raw/transactions.csv"
    )

    upload_file(
        SCORED_FILE,
        "scored/scored_transactions.csv"
    )