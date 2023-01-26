from controller.dependencies.pagination.base import Pagination


class PythonicPagination(Pagination):
    @property
    def slice(self) -> slice:
        return slice(self.offset, self.offset + self.limit)
