from graphene import Connection, Int

class ConnectionWithTotalCount(Connection):
    class Meta:
        abstract = True

    total_count = Int()

    @staticmethod
    def resolve_total_count(root, info, **kwargs):
        return root.length
