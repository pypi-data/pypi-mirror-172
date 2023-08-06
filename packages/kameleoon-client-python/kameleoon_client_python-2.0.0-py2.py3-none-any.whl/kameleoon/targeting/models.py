from typing import Optional

from kameleoon.exceptions import NotFoundError
from kameleoon.targeting.tree_builder import create_tree


class Segment:
    def __init__(self, *args) -> None:
        if args:
            if len(args) == 1:
                if args[0] is None:
                    raise NotFoundError("arguments for segment")
                if "id" not in args[0]:
                    raise NotFoundError("id")
                self.id = int(args[0]["id"])
                if "conditionsData" not in args[0]:
                    raise NotFoundError("conditionsData")

                self.tree = create_tree(args[0]["conditionsData"])
            elif len(args) == 2:
                self.id = args[0]
                self.tree = args[1]

    def check_tree(self, get_targeting_data) -> Optional[bool]:
        if not self.tree:
            is_targeted: Optional[bool] = True
        else:
            is_targeted = self.tree.check(get_targeting_data)
        return is_targeted is True