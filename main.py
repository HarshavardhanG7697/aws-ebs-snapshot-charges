from asyncio.log import logger
import boto3
import logging

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


def get_snapshot_name(snapshot):
    for tag in snapshot["Tags"]:
        if tag["Key"] == "Name":
            return tag["Value"]
    raise Exception(
        f"{snapshot['SnapshotId']} does not have a Name tag.\n \
        But it has the following tags: {snapshot['Tags']}"
    )


volumes = ["vol-029cbf276b7f62071", "vol-099624baeb6ddac32"]
logger.info(f"Looking for snapshots of volumes: {volumes}")
for volume in volumes:
    snapshots = get_ebs_snapshots(volume)
    if not snapshots:
        logger.warning(f"There are no snapshots found for volume: {volume}")
    else:
        for snapshot in snapshots:
            logger.info(f"Snapshot ID: {snapshot['SnapshotId']}")
            logger.info(f"{snapshot['SnapshotId']} created on: {snapshot['StartTime']}")
            try:
                logger.info(f"Name of the snapshot: {get_snapshot_name(snapshot)}")
            except Exception as e:
                logger.error(e)
