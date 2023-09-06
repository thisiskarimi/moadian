import uuid


class Packet():
    def __init__(self, packet_type, fiscal_id, data=None):
        self.uid = str(uuid.uuid4())
        self.packetType = packet_type
        self.retry = False
        self.data = data
        self.encryptionKeyId = None
        self.symmetricKey = None
        self.iv = None
        self.fiscalId = fiscal_id
        self.dataSignature = None
        self.signatureKeyId = None

    def to_dict(self):
        serialized = self.__dict__
        if not self.signatureKeyId:
            del serialized["signatureKeyId"]
        return serialized
