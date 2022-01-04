class Node:
    def __init__(self, value):
        self.red = False
        self.parent = None
        self.value = value
        self.left = None
        self.right = None


class RedBlackTree:
    def __init__(self):
        self.nil = Node(None)
        self.root = self.nil

    def insert(self, value):
        new_node = Node(value)
        new_node.left = self.nil
        new_node.right = self.nil
        new_node.red = True

        parent_node = None
        current_node = self.root
        while current_node != self.nil:
            parent_node = current_node
            if new_node.value < current_node.value:
                current_node = current_node.left
            elif new_node.value > current_node.value:
                current_node = current_node.right
            else:
                return

        new_node.parent = parent_node
        if parent_node is None:
            self.root = new_node
        elif new_node.value < parent_node.value:
            parent_node.left = new_node
        else:
            parent_node.right = new_node

        self.balance_after_insert(new_node)

    #   X                y
    #  / \              / \
    # A   y     =>     x   C
    #    / \          / \
    #   B   C        A   B
    def left_rotate(self, x_node):
        y_node = x_node.right
        x_node.right = y_node.left
        if y_node.left != self.nil:
            y_node.left.parent = x_node
        y_node.parent = x_node.parent
        if x_node.parent is None:
            self.root = y_node
        elif x_node == x_node.parent.left:
            x_node.parent.left = y_node
        elif x_node == x_node.parent.right:
            x_node.parent.right = y_node
        y_node.left = x_node
        x_node.parent = y_node

    #      x             y
    #     / \           / \
    #    y   C   =>    A   x
    #   / \               / \
    #  A   B             B   C
    def right_rotate(self, x_node):
        y_node = x_node.left
        x_node.left = y_node.right
        if y_node != self.nil:
            y_node.right.parent = x_node
        y_node.parent = x_node.parent
        if x_node.parent is None:
            self.root = y_node
        elif x_node == x_node.parent.right:
            x_node.parent.right = y_node
        else:
            x_node.parent.left = y_node
        y_node.right = x_node
        x_node.parent = y_node

    def balance_after_insert(self, current_node):
        while current_node != self.root and current_node.parent.red:
            if current_node.parent == current_node.parent.parent.right:
                uncle = current_node.parent.parent.left
                # red uncle case
                if uncle.red:
                    uncle.red = False
                    current_node.parent.red = False
                    current_node.parent.parent.red = True
                    current_node = current_node.parent.parent
                else:
                    # triangle case(current node, parent and grandparent form a triangle)(right left case)
                    if current_node == current_node.parent.left:
                        current_node = current_node.parent
                        self.right_rotate(current_node)
                    # line case(current node, parent and grandparent form a line)(right right case)
                    # after triangle case we always get the line case
                    current_node.parent.red = False
                    current_node.parent.parent.red = True
                    self.left_rotate(current_node.parent.parent)
            else:
                uncle = current_node.parent.parent.right
                # red uncle case
                if uncle.red:
                    uncle.red = False
                    current_node.parent.red = False
                    current_node.parent.parent.red = True
                    current_node = current_node.parent.parent
                else:
                    # triangle case(current node, parent and grandparent form a triangle)(left right case)
                    if current_node == current_node.parent.right:
                        current_node = current_node.parent
                        self.left_rotate(current_node)
                    # line case(current node, parent and grandparent form a line)(left left case)
                    # after triangle case we always get the line case
                    current_node.parent.red = False
                    current_node.parent.parent.red = True
                    self.right_rotate(current_node.parent.parent)
        self.root.red = False

    def transplant(self, u, v):
        if u.parent is None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def delete(self, value):
        self._delete(self.root, value)

    def _delete(self, node, key):
        node_to_delete = self.nil
        while node != self.nil:
            if node.value == key:
                node_to_delete = node

            if node.value <= key:
                node = node.right
            else:
                node = node.left

        if node_to_delete == self.nil:
            print("Cannot find key in the tree")
            return

        y = node_to_delete
        y_original_color = y.red
        if node_to_delete.left == self.nil:
            x = node_to_delete.right
            self.transplant(node_to_delete, node_to_delete.right)
        elif node_to_delete.right == self.nil:
            x = node_to_delete.left
            self.transplant(node_to_delete, node_to_delete.left)
        else:
            y = self.minimum(node_to_delete.right)
            y_original_color = y.red
            x = y.right
            if y.parent == node_to_delete:
                x.parent = y
            else:
                self.transplant(y, y.right)
                y.right = node_to_delete.right
                y.right.parent = y

            self.transplant(node_to_delete, y)
            y.left = node_to_delete.left
            y.left.parent = y
            y.red = node_to_delete.red
        if y_original_color is False:
            self.balance_after_delete(x)

    def balance_after_delete(self, current_node):
        while current_node != self.root and current_node.red is False:
            if current_node == current_node.parent.left:
                sibling = current_node.parent.right
                # red sibling case
                if sibling.red is True:
                    sibling.red = False
                    current_node.parent.red = True
                    self.left_rotate(current_node.parent)
                    sibling = current_node.parent.right

                # black children of sibling case
                if sibling.left.red is False and sibling.right.red is False:
                    sibling.red = True
                    current_node = current_node.parent
                else:
                    # triangle case(right left case - sibling is right child of parent and left child of sibling is red)
                    # after triangle case we always get the line case
                    if sibling.right.red is False:
                        sibling.left.red = False
                        sibling.red = True
                        self.right_rotate(sibling)
                        sibling = current_node.parent.right
                    # line case(right right case - sibling is right child of parent and right(or both) child of
                    # sibling is red)
                    sibling.red = current_node.parent.red
                    current_node.parent.red = False
                    sibling.right.red = False
                    self.left_rotate(current_node.parent)
                    current_node = self.root
            else:
                sibling = current_node.parent.left
                # red sibling case
                if sibling.red is True:
                    sibling.red = False
                    current_node.parent.red = True
                    self.right_rotate(current_node.parent)
                    sibling = current_node.parent.left

                # black children of sibling case
                if (sibling.right.red is False) and (sibling.left.red is False):
                    sibling.red = True
                    current_node = current_node.parent
                else:
                    # triangle case(left right case - sibling is left child of parent and right child of sibling is red)
                    # after triangle case we always get the line case
                    if sibling.left.red is False:
                        sibling.right.red = False
                        sibling.red = True
                        self.left_rotate(sibling)
                        sibling = current_node.parent.left
                    # line case(left left case - sibling is left child of parent and left(or both) child of
                    # sibling is red)
                    sibling.red = current_node.parent.red
                    current_node.parent.red = False
                    sibling.left.red = False
                    self.right_rotate(current_node.parent)
                    current_node = self.root
        current_node.red = False

    def minimum(self, node):
        while node.left != self.nil:
            node = node.left
        return node

    def __repr__(self):
        lines = []
        print_tree(self.root, lines)
        return '\n'.join(lines)


def print_tree(node, lines, level=0):
    if node.value is not None:
        print_tree(node.right, lines, level + 1)
        lines.append('-' * 4 * level + '> ' +
                     str(node.value) + ' ' + ('r' if node.red else 'b'))
        print_tree(node.left, lines, level + 1)


if __name__ == "__main__":
    red_black_tree = RedBlackTree()
    red_black_tree.insert(15)
    red_black_tree.insert(18)
    red_black_tree.insert(20)
    red_black_tree.insert(25)
    red_black_tree.insert(27)
    red_black_tree.delete(25)
    print(red_black_tree)
