import React, { useState, useEffect } from "react";
import axios from "axios";
import AVLTree from "./AVLTree"; // AVL Tree visualization component
import "./App.css";

function App() {
  const [key, setKey] = useState("");
  const [message, setMessage] = useState("");
  const [treeData, setTreeData] = useState(null);

  // Fetch AVL Tree from backend
  const fetchTree = async () => {
    try {
      const response = await axios.get("http://127.0.0.1:5000/get_tree");
      console.log("Fetched Tree Data:", response.data.tree);
      setTreeData(response.data.tree);
      setMessage("");
    } catch (error) {
      console.error("Error fetching tree:", error);
      setMessage("Error fetching tree data");
    }
  };

  useEffect(() => {
    fetchTree();
  }, []);

  // Insert a node
  const handleInsert = async () => {
    if (key === "" || isNaN(parseInt(key))) {
      setMessage("Please enter a valid number");
      return;
    }
    try {
      const response = await axios.post("http://127.0.0.1:5000/insert", { key: parseInt(key) });
      console.log("Tree after insertion:", response.data.tree);
      setTreeData(response.data.tree);
      setKey("");
      setMessage("Value inserted successfully!");
    } catch (error) {
      console.error("Insert error:", error);
      setMessage("Error inserting node");
    }
  };

  // Delete a node
  const handleDelete = async () => {
    if (key === "" || isNaN(parseInt(key))) {
      setMessage("Please enter a valid number");
      return;
    }
    try {
      const response = await axios.post("http://127.0.0.1:5000/delete", { key: parseInt(key) });
      console.log("Tree after deletion:", response.data.tree);
      setTreeData(response.data.tree);
      setKey("");
      setMessage("Value deleted successfully!");
    } catch (error) {
      console.error("Delete error:", error);
      setMessage("Error deleting node");
    }
  };

  // Search for a node
  const handleSearch = async () => {
    if (key === "" || isNaN(parseInt(key))) {
      setMessage("Please enter a valid number");
      return;
    }
    try {
      const response = await axios.post("http://127.0.0.1:5000/search", { key: parseInt(key) });
      setMessage(response.data.message); // Display success message from backend
    } catch (error) {
      console.error("Search error:", error);
      setMessage("Value not found in the tree");
    }
  };

  return (
    <div>
      <h1>AVL Tree Visualization</h1>
      <input
        type="number"
        placeholder="Enter value"
        value={key}
        onChange={(e) => setKey(e.target.value)}
      />
      <button onClick={handleInsert}>Insert</button>
      <button onClick={handleDelete}>Delete</button>
      <button onClick={handleSearch}>Search</button>

      {message && <p style={{ color: "red" }}>{message}</p>}
      {treeData ? <AVLTree treeData={treeData} /> : <p>Loading tree...</p>}
    </div>
  );
}

export default App;
