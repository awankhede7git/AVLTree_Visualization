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
        if root is None:
            return Node(key)

        if key < root.key:
            root.left = self.insert(root.left, key)
        else:
            root.right = self.insert(root.right, key)

        root.height = 1 + max(self.getHeight(root.left), self.getHeight(root.right))
        return self.balance(root)

    def delete(self, root, key):
        if not root:
            return root

        if key < root.key:
            root.left = self.delete(root.left, key)
        elif key > root.key:
            root.right = self.delete(root.right, key)
        else:
            if not root.left:
                return root.right
            elif not root.right:
                return root.left

            temp = self.getMinValueNode(root.right)
            root.key = temp.key
            root.right = self.delete(root.right, temp.key)

        if root is None:
            return root  

        root.height = 1 + max(self.getHeight(root.left), self.getHeight(root.right))
        return self.balance(root)

    def balance(self, root):
        balance_factor = self.getBalance(root)
        if balance_factor > 1:
            if self.getBalance(root.left) < 0:
                root.left = self.rotateLeft(root.left)
            return self.rotateRight(root)
        if balance_factor < -1:
            if self.getBalance(root.right) > 0:
                root.right = self.rotateRight(root.right)
            return self.rotateLeft(root)
        return root

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

    def getHeight(self, node):
        return node.height if node else 0

    def getBalance(self, node):
        return self.getHeight(node.left) - self.getHeight(node.right) if node else 0

    def getMinValueNode(self, node):
        while node.left:
            node = node.left
        return node
    
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
def insert_node():
    global root
    data = request.get_json()
    key = data.get("key")

    if key is None:
        return jsonify({"message": "Key is required"}), 400

    root = avl_tree.insert(root, key)
    return jsonify({"message": f"Inserted {key}", "tree": serialize_tree(root)}), 200

@app.route('/delete', methods=['POST'])
def delete_node():
    global root
    data = request.get_json()
    key = data.get("key")

    if key is None:
        return jsonify({"message": "Key is required"}), 400

    root = avl_tree.delete(root, key)
    return jsonify({"message": f"Deleted {key}", "tree": serialize_tree(root)}), 200

@app.route('/status', methods=['GET'])
def status():
    return jsonify({'message': 'AVL Tree Server Running'}), 200

if __name__ == '__main__':
    print("Flask server is running...")
    app.run(debug=True)
