import toolz as t

from app.db.models.device import Device
from app.db.models.interaction import Interaction
from app.db.repository.device_repository import insert_device
from app.db.repository.interaction_repository import create_interactions_connection


def flow_of_insert_devices(data):
    devices_models = t.pipe(
         data,
         t.partial(map, lambda d: insert_device(Device(**d))),
         list
      )
    return devices_models



def flow_of_connect_devices(data, devices_id):
    from_device = devices_id[0].value_or(None)
    to_device = devices_id[1].value_or(None)
    print(from_device)
    print(to_device)
    interaction_model = t.pipe(
        data,
        lambda i: create_interactions_connection(from_device, to_device, Interaction(**i)),
        list
    )
    return interaction_model
