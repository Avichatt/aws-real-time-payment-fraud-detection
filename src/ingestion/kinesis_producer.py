import os
import json
import boto3
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

AWS_REGION = os.getenv("AWS_REGION", "ap-south-1")
STREAM_NAME = os.getenv(
    "KINESIS_STREAM_NAME",
    "payment-transactions-stream"
)

INPUT_FILE = "data/raw/transactions.csv"

kinesis = boto3.client(
    "kinesis",
    region_name=AWS_REGION
)


def send_transaction(transaction):
    response = kinesis.put_record(
        StreamName=STREAM_NAME,
        Data=json.dumps(transaction),
        PartitionKey=str(transaction["customer_id"])
    )

    print(
        f"Sent {transaction['transaction_id']} "
        f"to shard {response['ShardId']}"
    )


def stream_transactions():
    df = pd.read_csv(INPUT_FILE)

    for _, row in df.iterrows():
        transaction = row.to_dict()
        send_transaction(transaction)


if __name__ == "__main__":
    stream_transactions()
    print("All transactions sent to Kinesis.")