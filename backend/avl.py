
import tkinter as tk
import time

class AVLNode:
    def __init__(self, key):
        self.key = key
        self.height = 1
        self.left = None
        self.right = None


class AVLTree:
    def __init__(self):
        self.root = None
        self.rotation_history = []
        self.search_path = []

    def insert(self, root, key):
        if not root:
            return AVLNode(key), True

        if key < root.key:
            root.left, inserted = self.insert(root.left, key)
        elif key > root.key:
            root.right, inserted = self.insert(root.right, key)
        else:
            return root, False  # Duplicate key

        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))
        balance = self.get_balance(root)

        # LL
        if balance > 1 and key < root.left.key:
            self.rotation_history.append(f"[{time.strftime('%H:%M:%S')}] LL Rotation at node {root.key}")
            return self.right_rotate(root), inserted

        # RR
        if balance < -1 and key > root.right.key:
            self.rotation_history.append(f"[{time.strftime('%H:%M:%S')}] RR Rotation at node {root.key}")
            return self.left_rotate(root), inserted

        # LR
        if balance > 1 and key > root.left.key:
            self.rotation_history.append(f"[{time.strftime('%H:%M:%S')}] LR Rotation at node {root.key}")
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root), inserted

        # RL
        if balance < -1 and key < root.right.key:
            self.rotation_history.append(f"[{time.strftime('%H:%M:%S')}] RL Rotation at node {root.key}")
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root), inserted

        return root, inserted
    # def insert(self, root, key, snapshots=None):
    #     if not root:
    #         new_node = AVLNode(key)
    #         if snapshots is not None:
    #             self.snapshot_tree(new_node, snapshots)  # capture after creation
    #         return new_node

    #     if key < root.key:
    #         root.left = self.insert(root.left, key, snapshots)
    #     elif key > root.key:
    #         root.right = self.insert(root.right, key, snapshots)
    #     else:
    #         return root  # Duplicate

    #     root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))
    #     balance = self.get_balance(root)

    #     # LL
    #     if balance > 1 and key < root.left.key:
    #         self.rotation_history.append(f"[{time.strftime('%H:%M:%S')}] LL Rotation at node {root.key}")
    #         root = self.right_rotate(root)
    #     # RR
    #     elif balance < -1 and key > root.right.key:
    #         self.rotation_history.append(f"[{time.strftime('%H:%M:%S')}] RR Rotation at node {root.key}")
    #         root = self.left_rotate(root)
    #     # LR
    #     elif balance > 1 and key > root.left.key:
    #         self.rotation_history.append(f"[{time.strftime('%H:%M:%S')}] LR Rotation at node {root.key}")
    #         root.left = self.left_rotate(root.left)
    #         root = self.right_rotate(root)
    #     # RL
    #     elif balance < -1 and key < root.right.key:
    #         self.rotation_history.append(f"[{time.strftime('%H:%M:%S')}] RL Rotation at node {root.key}")
    #         root.right = self.right_rotate(root.right)
    #         root = self.left_rotate(root)

    #     if snapshots is not None:
    #         self.snapshot_tree(root, snapshots)  # snapshot after balance fixes

    #     return root



    def delete(self, root, key):
        if not root:
            return root, False  # Not found

        deleted = False
        if key < root.key:
            root.left, deleted = self.delete(root.left, key)
        elif key > root.key:
            root.right, deleted = self.delete(root.right, key)
        else:
            deleted = True
            if not root.left:
                return root.right, True
            elif not root.right:
                return root.left, True

            temp = self.get_min_value_node(root.right)
            root.key = temp.key
            root.right, _ = self.delete(root.right, temp.key)

        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))
        balance = self.get_balance(root)

        # LL
        if balance > 1 and self.get_balance(root.left) >= 0:
            self.rotation_history.append(f"[{time.strftime('%H:%M:%S')}] LL Rotation at node {root.key}")
            return self.right_rotate(root), deleted

        # LR
        if balance > 1 and self.get_balance(root.left) < 0:
            self.rotation_history.append(f"[{time.strftime('%H:%M:%S')}] LR Rotation at node {root.key}")
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root), deleted

        # RR
        if balance < -1 and self.get_balance(root.right) <= 0:
            self.rotation_history.append(f"[{time.strftime('%H:%M:%S')}] RR Rotation at node {root.key}")
            return self.left_rotate(root), deleted

        # RL
        if balance < -1 and self.get_balance(root.right) > 0:
            self.rotation_history.append(f"[{time.strftime('%H:%M:%S')}] RL Rotation at node {root.key}")
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root), deleted

        return root, deleted


    def search(self, root, key):
        self.search_path = []
        return self._search(root, key)

    def _search(self, node, key):
        if node is None:
            return None
        self.search_path.append(node.key)
        if key == node.key:
            return node
        elif key < node.key:
            return self._search(node.left, key)
        else:
            return self._search(node.right, key)

    def get_min_value_node(self, root):
        while root.left:
            root = root.left
        return root

    def left_rotate(self, z):
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    def right_rotate(self, z):
        y = z.left
        T3 = y.right
        y.right = z
        z.left = T3
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    def get_height(self, node):
        return node.height if node else 0

    def get_balance(self, node):
        return self.get_height(node.left) - self.get_height(node.right) if node else 0

    def add(self, key):
        self.rotation_history.clear()
        self.root, inserted = self.insert(self.root, key)
        return inserted

    # def add(self, key, snapshots=None):
    #     self.rotation_history.clear()
    #     if self.search(self.root, key):  # prevent duplicate insertions
    #         return False
    #     self.root = self.insert(self.root, key, snapshots)
    #     return True


    def remove(self, key):
        self.rotation_history.clear()
        self.root, deleted = self.delete(self.root, key)
        return deleted
    def reset_search_path(self):
        self.search_path = []

    def snapshot_tree(self, node, snapshot_list):
        def clone_node(n):
            if n is None:
                return None
            copy = AVLNode(n.key)
            copy.height = n.height
            copy.left = clone_node(n.left)
            copy.right = clone_node(n.right)
            return copy

        snapshot_list.append(clone_node(node))


class AVLVisualizer:
    def __init__(self, tree, canvas):
        self.tree = tree
        self.canvas = canvas

    def draw_tree(self):
        self.canvas.delete("all")
        if self.tree.root:
            self._draw_node(self.tree.root, 400, 50, 200)

    def _draw_node(self, node, x, y, dx):
        if node.left:
            self.canvas.create_line(x, y, x - dx, y + 80)
            self._draw_node(node.left, x - dx, y + 80, dx // 2)
        if node.right:
            self.canvas.create_line(x, y, x + dx, y + 80)
            self._draw_node(node.right, x + dx, y + 80, dx // 2)

        fill_color = "yellow" if node.key in self.tree.search_path else "skyblue"
        self.canvas.create_oval(x - 20, y - 20, x + 20, y + 20, fill=fill_color)
        self.canvas.create_text(x, y, text=str(node.key), font=("Helvetica", 10, "bold"))
        self.canvas.create_text(x, y + 25, text=f"H:{node.height}, BF:{self.tree.get_balance(node)}", font=("Helvetica", 8))


def main():
    tree = AVLTree()

    root = tk.Tk()
    root.title("Advanced AVL Tree Visualizer")

    canvas = tk.Canvas(root, width=900, height=600, bg="white")
    canvas.pack()

    visualizer = AVLVisualizer(tree, canvas)

    control_frame = tk.Frame(root)
    control_frame.pack()

    entry = tk.Entry(control_frame, width=10)
    entry.grid(row=0, column=0, padx=5)


    def insert():
        try:
            value = int(entry.get())
            tree.rotation_history.clear()
            inserted = tree.add(value)

            if inserted:
                visualizer.draw_tree()
                root.update()
                time.sleep(0.5)

                if tree.rotation_history:
                    msg = f"Inserted: {value} | " + " | ".join([line.split("] ")[1] for line in tree.rotation_history])
                else:
                    msg = f"Inserted: {value} | No rotation occurred"
                msg_label.config(text=msg)
                update_history()
            else:
                msg_label.config(text=f"Error: {value} already exists in the tree.")
        except:
            msg_label.config(text="Enter valid integer.")
        entry.delete(0, tk.END)


    # def insert():
    #     try:
    #         value = int(entry.get())
    #         snapshots = []
    #         inserted = tree.add(value, snapshots)

    #         if inserted:
    #             for snap in snapshots:
    #                 visualizer.tree.root = snap
    #                 visualizer.draw_tree()
    #                 root.update()
    #                 time.sleep(0.5)

    #             visualizer.tree.root = tree.root  # final state
    #             visualizer.draw_tree()

    #             if tree.rotation_history:
    #                 msg = f"Inserted: {value} | " + " | ".join([line.split("] ")[1] for line in tree.rotation_history])
    #             else:
    #                 msg = f"Inserted: {value} | No rotation occurred"
    #             msg_label.config(text=msg)
    #             update_history()
    #         else:
    #             msg_label.config(text=f"Error: {value} already exists in the tree.")
    #     except:
    #         msg_label.config(text="Enter valid integer.")
    #     entry.delete(0, tk.END)




    def delete():
        try:
            value = int(entry.get())
            tree.reset_search_path()
            deleted = tree.remove(value)
            if deleted:
                msg_label.config(text=f"Deleted: {value}")
            else:
                msg_label.config(text=f"{value} not found in tree")
            visualizer.draw_tree()
            root.update()
            time.sleep(0.5)
            update_history()
        except:
            msg_label.config(text="Enter valid integer.")
        entry.delete(0, tk.END)


    def search():
        try:
            value = int(entry.get())
            tree.reset_search_path()
            found = tree.search(tree.root, value)
            visualizer.draw_tree()
            msg = f"Found: {value}" if found else f"{value} not found"
            msg_label.config(text=msg)
        except:
            msg_label.config(text="Enter valid integer.")
        entry.delete(0, tk.END)


    tk.Button(control_frame, text="Insert", command=insert).grid(row=0, column=1)
    tk.Button(control_frame, text="Delete", command=delete).grid(row=0, column=2)
    tk.Button(control_frame, text="Search", command=search).grid(row=0, column=3)

    msg_label = tk.Label(root, text="Welcome to AVL Visualizer!", fg="blue")
    msg_label.pack()

    history_label = tk.Label(root, text="Rotation History:")
    history_label.pack(anchor="w")

    history_text = tk.Text(root, height=6, width=70)
    history_text.pack()

    # def update_history():
    #     history_text.delete("1.0", tk.END)
    #     for line in tree.rotation_history:
    #         history_text.insert(tk.END, line + "\n")
    def update_history():
        history_text.delete("1.0", tk.END)
        if tree.rotation_history:
            for line in tree.rotation_history:
                history_text.insert(tk.END, line + "\n")
        else:
            history_text.insert(tk.END, "No rotations occurred.\n")


    root.mainloop()

if __name__ == "__main__":
    main()
