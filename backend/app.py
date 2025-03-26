from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# AVL Tree Node class
class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1

# AVL Tree class
class AVLTree:
    def insert(self, root, key):
        if root is not None and key == root.key:
            return root, False, None  # No insertion, key exists

        if root is None:
            return Node(key), True, "Inserted node without rotation"  # New node inserted

        if key < root.key:
            root.left, inserted, rotation = self.insert(root.left, key)
        else:
            root.right, inserted, rotation = self.insert(root.right, key)

        if not inserted:
            return root, False, None

        root.height = 1 + max(self.getHeight(root.left), self.getHeight(root.right))

        # Balance the node
        balanced_root, balance_rotation = self.balance_with_rotation_info(root)
        if balance_rotation:
            rotation = balance_rotation  # Capture the rotation info

        return balanced_root, True, rotation

    def balance_with_rotation_info(self, root):
        balance_factor = self.getBalance(root)
        if balance_factor > 1:
            if self.getBalance(root.left) < 0:
                root.left = self.rotateLeft(root.left)
                return self.rotateRight(root), "Left-Right Rotation"
            return self.rotateRight(root), "Right Rotation"
        if balance_factor < -1:
            if self.getBalance(root.right) > 0:
                root.right = self.rotateRight(root.right)
                return self.rotateLeft(root), "Right-Left Rotation"
            return self.rotateLeft(root), "Left Rotation"
        return root, None  # No rotation

    def delete(self, root, key):
        if not root:
            return root, None

        if key < root.key:
            root.left, rotation = self.delete(root.left, key)
        elif key > root.key:
            root.right, rotation = self.delete(root.right, key)
        else:
            if not root.left:
                return root.right, "Deleted node without rotation"
            elif not root.right:
                return root.left, "Deleted node without rotation"

            temp = self.getMinValueNode(root.right)
            root.key = temp.key
            root.right, rotation = self.delete(root.right, temp.key)

        if root is None:
            return root, None

        root.height = 1 + max(self.getHeight(root.left), self.getHeight(root.right))

        # Balance the node
        balanced_root, balance_rotation = self.balance_with_rotation_info(root)
        if balance_rotation:
            rotation = balance_rotation  # Capture the rotation info

        return balanced_root, rotation

    def getHeight(self, node):
        return node.height if node else 0

    def getBalance(self, node):
        return self.getHeight(node.left) - self.getHeight(node.right) if node else 0

    def rotateLeft(self, z):
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        z.height = 1 + max(self.getHeight(z.left), self.getHeight(z.right))
        y.height = 1 + max(self.getHeight(y.left), self.getHeight(y.right))
        return y

    def rotateRight(self, z):
        y = z.left
        T3 = y.right
        y.right = z
        z.left = T3
        z.height = 1 + max(self.getHeight(z.left), self.getHeight(z.right))
        y.height = 1 + max(self.getHeight(y.left), self.getHeight(y.right))
        return y

    def getMinValueNode(self, node):
        while node.left:
            node = node.left
        return node

    def search(self, root, key):
        if root is None:
            return False
        if key == root.key:
            return True
        elif key < root.key:
            return self.search(root.left, key)
        else:
            return self.search(root.right, key)

    def contains(self, root, key):
        return self.search(root, key)


# Initialize AVL tree
avl_tree = AVLTree()
root = None

def serialize_tree(node):
    if node is None:
        return None
    return {
        "key": node.key,
        "left": serialize_tree(node.left),
        "right": serialize_tree(node.right)
    }

@app.route("/get_tree", methods=["GET"])
def get_tree():
    return jsonify({"tree": serialize_tree(root)}), 200

@app.route('/insert', methods=['POST'])
def insert():
    global root
    data = request.get_json()
    key = data.get('key')
    if key is None:
        return jsonify({'message': 'Invalid input'}), 400

    root, inserted, rotation_info = avl_tree.insert(root, key)
    if inserted:
        message = f"Inserted {key}. {rotation_info}"
        return jsonify({'message': message, 'tree': serialize_tree(root)}), 200
    else:
        return jsonify({'message': f'Key {key} already exists.'}), 400

@app.route('/delete', methods=['POST'])
def delete_node():
    global root
    data = request.get_json()
    key = data.get("key")

    if key is None:
        return jsonify({"message": "Key is required"}), 400

    if not avl_tree.contains(root, key):
        return jsonify({"message": f"Key {key} not present in the tree."}), 400

    root, rotation_info = avl_tree.delete(root, key)
    if root is None:
        return jsonify({"message": f"Deleted {key}. {rotation_info}"}), 200
    else:
        return jsonify({"message": f"Deleted {key}. {rotation_info}", "tree": serialize_tree(root)}), 200

@app.route('/status', methods=['GET'])
def status():
    return jsonify({'message': 'AVL Tree Server Running'}), 200

@app.route("/search", methods=["POST"])
def search_node():
    global root
    data = request.get_json()
    key = data.get("key")

    if key is None:
        return jsonify({"message": "Key is required"}), 400

    if avl_tree.search(root, key):
        return jsonify({"message": f"Value {key} found in the tree"}), 200
    else:
        return jsonify({"message": "Value not found in the tree"}), 404

if __name__ == '__main__':
    print("Flask server is running...")
    app.run(debug=True)
