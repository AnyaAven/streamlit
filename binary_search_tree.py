import streamlit as st
import graphviz


class TreeNode:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.val = key


class BST:
    def __init__(self):
        self.root = None

    def insert(self, root, key):
        if root is None:
            return TreeNode(key)
        else:
            if root.val < key:
                root.right = self.insert(root.right, key)
            else:
                root.left = self.insert(root.left, key)
        return root

    def inorder(self, root):
        return self.inorder(root.left) + [root.val] + self.inorder(root.right) if root else []

    def preorder(self, root):
        return [root.val] + self.preorder(root.left) + self.preorder(root.right) if root else []

    def postorder(self, root):
        return self.postorder(root.left) + self.postorder(root.right) + [root.val] if root else []

    def _display_tree(self, root, dot=None):
        if dot is None:
            dot = graphviz.Digraph()
            dot.node(name=str(root.val), label=str(root.val))

        if root.left:
            dot.node(name=str(root.left.val), label=str(root.left.val))
            dot.edge(str(root.val), str(root.left.val))
            self._display_tree(root.left, dot)

        if root.right:
            dot.node(name=str(root.right.val), label=str(root.right.val))
            dot.edge(str(root.val), str(root.right.val))
            self._display_tree(root.right, dot)

        return dot

    def display_tree(self, root):
        return self._display_tree(root).source


def main():
    st.title("Binary Search Tree Visualization 🌳")

    bst = BST()
    input_numbers = st.text_input(
        "Enter numbers separated by commas:", "10, 5, 20, 3, 7, 15, 25")
    numbers = [int(num) for num in input_numbers.split(",")]

    for number in numbers:
        bst.root = bst.insert(bst.root, number)

    st.subheader("BST Visualization:")
    dot_source = bst.display_tree(bst.root)
    st.graphviz_chart(dot_source)

    st.subheader("In-order Traversal of BST:")
    st.write(bst.inorder(bst.root))

    st.subheader("Pre-order Traversal of BST:")
    st.write(bst.preorder(bst.root))

    st.subheader("Post-order Traversal of BST:")
    st.write(bst.postorder(bst.root))


if __name__ == "__main__":
    main()
