from graphene import (Interface, Int)


class TotalCount(Interface):
    total_count = Int()

    def resolve_total_count(self, info):
        return self.length