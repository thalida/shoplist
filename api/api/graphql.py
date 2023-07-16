from graphene import Connection, Int, relay

class ConnectionWithTotalCount(Connection):
    class Meta:
        abstract = True

    total_count = Int()

    @staticmethod
    def resolve_total_count(root, info, **kwargs):
        return root.length


class RelayUUIDNode(relay.Node):
    class Meta:
        name = 'Node'

    @staticmethod
    def to_global_id(type, id):
        return id

    @staticmethod
    def get_node_from_global_id(info, global_id, only_type=None):
        return info.return_type.graphene_type.get_node(info, global_id)
