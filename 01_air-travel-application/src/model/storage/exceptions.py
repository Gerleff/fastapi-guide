class EntityNotFoundError(Exception):
    def __init_(self, table: str, _id: int):
        super(self).__init__(table, _id)

    @property
    def description(self):
        return "In table {} entity with id {} is not found ".format(*self.args)
