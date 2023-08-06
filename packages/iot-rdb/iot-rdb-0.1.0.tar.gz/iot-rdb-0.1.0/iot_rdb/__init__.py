# Parsing every util class for redis connection
from iot_rdb.util import IotRedisBasic
from iot_rdb.util import IotRedisPublisher
from iot_rdb.util import IotRedisSubscriber
from iot_rdb.util import IotRedisPubSub


class IotRedisCommon:
    """Common variable to all containers

    This standard is for defining all PubSub clients
    in every container to be created.

    class CrossConnection:
        "container_name" = (tuple with channels to listen)
        "container_name2" = ()
        ...
    }

    Channels publishing now:
        - CONTROLLER : control_input
        - OPCUA: raw_outputs
        - AUTOENCODER: filtered_outputs
        - DB:
        - DBDRIVER:
        - MANAGER:
    """

    class CrossConnection:
        OPCUA = ("control_input")
        CONTROLLER = ("raw_outputs", "filtered_outputs")
        AUTOENCODER = ("raw_outputs")
        DB = ("raw_outputs", "filtered_outputs")
        DBDRIVER = ("raw_outputs", "filtered_outputs")
