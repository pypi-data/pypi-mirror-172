from typing import Optional, Iterable
import math

def chunk_by_num_items(l, num_items: int) -> Iterable:
    if num_items == 0:
            yield l
            return
    # [1, 2, 3, 4, 5] num_items 2 => 5/2 = 3 lists
    # 0-2, 2-4, 4-5
    start: int = 0
    while start < len(l):
        print (l[start : start + num_items])
        yield l[start : start + num_items]
        start += num_items


def chunk(l, num_chunks: Optional[int] = None, num_items: Optional[int] = None) -> Iterable:
    """
    Returns a generator that yields chunks of items.
    :param num_chunks: Number of chunks to return.
    :param num_items: Number of items to return.
    :return: Generator that yields chunks of items.
    """
    if num_items is None and num_chunks is None:
        raise ValueError("Either num_items or num_chunks must be specified.")

    if num_items is not None:
        yield from chunk_by_num_items(l, num_items)

    elif num_chunks is not None:
        if num_chunks == 0 or num_chunks == 1:
            yield l
            return
        # [1, 2, 3, 4, 5] num_chunks 2 => 5/2 = 2
        # [1, 2] [3, 4], [5, 6]
        num_items: int = int(math.ceil(len(l) / num_chunks))
        # start = 0
        # for chunk in range(chunks):
        #     yield l[start:  start + num_chunks]
        #     start += num_chunks
        yield from chunk_by_num_items(l, num_items)
    else:
        raise ValueError("No operations performed")