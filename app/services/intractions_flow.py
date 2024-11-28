import toolz as t
from returns.result import Result
from app.db.models.device import Device
from app.db.models.interaction import Interaction
from app.db.repository.device_repository import insert_device
from app.db.repository.interaction_repository import create_interactions_connection


def check_if_got_same_ids(data):
    return data['devices'][0]['id'] == data['devices'][1]['id']







def flow_of_connect_devices(data) -> Result[str, str]:
    t.pipe(
        data['devices'],
        t.partial(map, lambda d: insert_device(Device(**d))),
        list
    )
    interaction_model = t.pipe(
        data['interaction'],
        lambda i: create_interactions_connection(Interaction(**i))
    )
    return interaction_model
