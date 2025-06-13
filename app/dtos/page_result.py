from typing import TypeVar

T = TypeVar("T")

class PageResult:
    def __init__(self, data: T, page: int, page_size: int, total_count: int, pages: int):
        self.data = data
        self.page = page
        self.page_size = page_size
        self.total_count = total_count
        self.pages = pages