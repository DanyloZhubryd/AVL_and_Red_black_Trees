class TreeNode(object):
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.height = 1


class AvlTree(object):
    def __init__(self):
        self.root = None

    def insert(self, value):
        if not self.root:
            self.root = TreeNode(value)
            return self.root
        return self._insert(self.root, value)

    def _insert(self, node, value):
        if not node:
            return TreeNode(value)
        elif node.value < value:
            node.left = self._insert(node.left, value)
        else:
            node.right = self._insert(node.right, value)

        node.height = 1 + max(self.get_height(node.left),
                              self.get_height(node.right))

        balance = self.get_balance(node)

        if balance > 1 and value < node.left.value:
            return self.right_rotate(node)

        if balance < -1 and value > node.right.value:
            return self.left_rotate(node)

        if balance > 1 and value > node.left.value:
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)

        if balance < -1 and value < node.right.value:
            node.right = self.right_rotate(node.right)
            return self.left_rotate(node)

        return node

    def delete(self, value):
        self._delete(self.root, value)

    def _delete(self, node, value):
        if not node:
            return node

        elif value < node.value:
            node.left = self._delete(node.left, value)

        elif value > node.value:
            node.right = self._delete(node.right, value)

        else:
            if node.left is None:
                temp = node.right
                node = None
                return temp

            elif node.right is None:
                temp = node.left
                node = None
                return temp

            temp = self.get_min_value_node(node.right)
            node.value = temp.value
            node.right = self._delete(node.right,
                                      temp.value)
        if node is None:
            return node
        node.height = 1 + max(self.get_height(node.left),
                              self.get_height(node.right))

        balance = self.get_balance(node)
        if balance < -1 and self.get_balance(node.left) <= 0:
            return self.right_rotate(node)

        if balance > 1 and self.get_balance(node.right) >= 0:
            return self.left_rotate(node)

        if balance < -1 and self.get_balance(node.left) > 0:
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)

        if balance > 1 and self.get_balance(node.right) < 0:
            node.right = self.right_rotate(node.right)
            return self.left_rotate(node)

        return node

    def left_rotate(self, x_node):
        y_node = x_node.right
        b_node = y_node.left
        y_node.left = x_node
        if x_node == self.root:
            self.root = y_node
        x_node.right = b_node

        x_node.height = 1 + max(self.get_height(x_node.left),
                                self.get_height(x_node.right))
        y_node.height = 1 + max(self.get_height(y_node.left),
                                self.get_height(y_node.right))
        return y_node

    def right_rotate(self, x_node):
        y_node = x_node.left
        c_node = y_node.right
        y_node.right = x_node
        if x_node == self.root:
            self.root = y_node
        x_node.left = c_node

        x_node.height = 1 + max(self.get_height(x_node.left),
                                self.get_height(x_node.right))
        y_node.height = 1 + max(self.get_height(y_node.left),
                                self.get_height(y_node.right))
        return y_node

    def get_height(self, node):
        if not node:
            return 0

        return node.height

    def get_balance(self, node):
        if not node:
            return 0

        return self.get_height(node.right) - self.get_height(node.left)

    def get_min_value_node(self, node):
        if node is None or node.left is None:
            return node

        return self.get_min_value_node(node.left)

    def __repr__(self):
        lines = []
        print_tree(self.root, lines)
        return '\n'.join(lines)


def print_tree(node, lines, level=0):
    if node is not None:
        print_tree(node.left, lines, level + 1)
        lines.append('-' * 4 * level + '> ' +
                     str(node.value) + ' h=' + str(node.height))
        print_tree(node.right, lines, level + 1)


if __name__ == "__main__":
    myTree = AvlTree()
    nums = [9, 5, 10, 0, 6, 11, -1, 1, 2]

    for num in nums:
        myTree.insert(num)

    print(myTree.root.value)
    print(myTree.root.value)
    print(myTree)
