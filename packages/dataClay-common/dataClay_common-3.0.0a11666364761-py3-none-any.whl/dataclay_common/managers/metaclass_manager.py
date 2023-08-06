import json
import uuid

from dataclay_common.exceptions.exceptions import *
from dataclay_common.protos import common_messages_pb2
from dataclay_common.protos.common_messages_pb2 import LANG_NONE
from dataclay_common.utils.json import UUIDEncoder, uuid_parser


class Metaclass:
    def __init__(self, id, namespace, class_name):
        self.id = id
        self.namespace = namespace
        self.class_name = class_name

    def key(self):
        return f"/metaclass/{self.id}"

    def value(self):
        return json.dumps(self.__dict__, cls=UUIDEncoder)

    @classmethod
    def from_json(cls, s):
        return cls(**json.loads(s))


class MetaclassManager:

    lock = "lock_metaclass"

    def __init__(self, etcd_client):
        self.etcd_client = etcd_client

    def get_metaclass(self, metaclass_id):
        key = f"/metaclass/{metaclass_id}"
        value = self.etcd_client.get(key)[0]
        if value is None:
            raise MetaclassDoesNotExistError(metaclass_id)
        return Metaclass.from_json(value)
