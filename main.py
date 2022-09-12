from asyncio.log import logger
import boto3
import logging
import datetime
from dateutil.tz import tzlocal

logging.basicConfig(
    level=logging.INFO, format="pid=%(process)d[%(levelname)s]:%(message)s"
)


def get_ebs_snapshots(volume_id):
    client = boto3.client("ec2", region_name="ap-south-1")
    logger.info(f"Getting snapshots for volume: {volume_id}")
    try:
        snapshots_list = client.describe_snapshots(
            Filters=[
                {
                    "Name": "volume-id",
                    "Values": [
                        volume_id,
                    ],
                },
            ],
        )
    except Exception as e:
        logger.error(f"Error while getting snapshots for volume: {volume_id}")
        logger.error(e)
        return None
    return snapshots_list["Snapshots"]


def get_snapshot_id(snapshot):
    return snapshot["SnapshotId"]


def get_snapshot_name(snapshot):
    logger.info(f"Retrieving snapshot name for snapshot: {snapshot['SnapshotId']}")
    for tag in snapshot["Tags"]:
        if tag["Key"] == "Name":
            logger.info(f"Name Tag present for snapshot: {snapshot['SnapshotId']}")
            return tag["Value"]
    return None


def time_since_snapshot(snapshot):
    logger.info(f"Calculating age of snapshot: {snapshot['SnapshotId']}")
    snapshot_created = snapshot["StartTime"]
    time_now = datetime.datetime.now(tzlocal())
    logger.info(f"Current time: {time_now}")
    try:
        hours = round(((time_now - snapshot_created).total_seconds()) / 3600, 2)
        return hours
    except Exception as e:
        logger.error(f"Error while calculating age of snapshot: {snapshot['SnapshotId']}")
        logger.error(e)
        return None
    

volumes = ["vol-029cbf276b7f62071", "vol-099624baeb6ddac32"]
logger.info(f"Looking for snapshots of volumes: {volumes}")
for volume in volumes:
    snapshots = get_ebs_snapshots(volume)
    if not snapshots:
        logger.warning(f"There are no snapshots found for volume: {volume}")
    else:
        for snapshot in snapshots:
            snapshot_id = get_snapshot_id(snapshot)
            logger.info(f"Snapshot id: {snapshot_id}")
            snapshot_name = get_snapshot_name(snapshot)
            if snapshot_name:
                logger.info(f"Snapshot name: {snapshot_name}")
            else:
                logger.warning(
                    f"{snapshot['SnapshotId']} does not have a Name tag.\nBut it has the following tags: {snapshot['Tags']}"
                )
            snapshot_age = time_since_snapshot(snapshot)
            if not snapshot_age:
                logger.warning(f"Unable to calculate the age of snapshot: {snapshot['SnapshotId']}")
            else:
                logger.info(f"Age of {snapshot_id}: {snapshot_age} hours")
