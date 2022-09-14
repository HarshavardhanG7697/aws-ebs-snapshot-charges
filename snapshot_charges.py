from asyncio.log import logger
import main
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s[%(funcName)s][%(levelname)s]:%(message)s"
)

volume_id = input("Enter volume id: ")
snapshots = main.get_ebs_snapshots(volume_id)

snapshot_count = 1
snapshot_list = []
next_token = ""
for snapshot in snapshots:
    snapshot_id = main.get_snapshot_id(snapshot)
    snapshot_list.append(snapshot_id)
    logger.info(f"Snapshot {snapshot_count}: {snapshot_id}")
    snapshot_name = main.get_snapshot_name(snapshot)
    if snapshot_name:
        logger.info(f"Snapshot Name: {snapshot_name}")
    snapshot_age = main.time_since_snapshot(snapshot)
    logger.info(f"Snapshot Age: {snapshot_age} hours")
    snapshot_count += 1

first_snapshot = int(0)
second_snapshot = int(1)

diff_in_size = []
for i in range(len(snapshot_list)-1):
    changed_blocks = main.snapshot_changed_blocks(snapshot_list[first_snapshot], snapshot_list[second_snapshot])
    diff_in_size.append(round(changed_blocks,2))
    first_snapshot += 1
    second_snapshot += 1
    logger.info(diff_in_size)
