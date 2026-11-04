import os, datetime
import boto3

rds = boto3.client("rds")
sns = boto3.client("sns")

def lambda_handler(event, context):
    db = os.environ["DB_ID"]
    keep = int(os.environ.get("KEEP", "3"))
    topic = os.environ["TOPIC_ARN"]

    ts = datetime.datetime.utcnow().strftime("%Y-%m-%d-%H-%M")
    name = f"{db}-auto-{ts}"
    rds.create_db_snapshot(DBInstanceIdentifier=db, DBSnapshotIdentifier=name)

    snaps = rds.describe_db_snapshots(
        DBInstanceIdentifier=db, SnapshotType="manual"
    )["DBSnapshots"]
    mine = sorted(
        [s["DBSnapshotIdentifier"] for s in snaps
         if s["DBSnapshotIdentifier"].startswith(f"{db}-auto-")],
        reverse=True,
    )
    deleted = mine[keep:]
    for old in deleted:
        rds.delete_db_snapshot(DBSnapshotIdentifier=old)

    msg = f"Created snapshot {name}. Deleted old snapshots: {deleted or 'none'}"
    sns.publish(TopicArn=topic, Subject="RDS snapshot completed", Message=msg)
    return {"created": name, "deleted": deleted}