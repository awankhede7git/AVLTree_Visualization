import React, { useState, useEffect } from "react";
import axios from "axios";
import AVLTree from "./AVLTree"; // AVL Tree visualization component
import "./App.css";

function App() {
  const [key, setKey] = useState("");
  const [message, setMessage] = useState("");
  const [treeData, setTreeData] = useState(null);
  const [isLoading, setIsLoading] = useState(false); // Loading state

  // Fetch AVL Tree from backend
  const fetchTree = async () => {
    setIsLoading(true);
    try {
      const response = await axios.get("http://127.0.0.1:5000/get_tree");
      console.log("Fetched Tree Data:", response.data.tree);
      setTreeData(response.data.tree);
      setMessage("");
    } catch (error) {
      console.error("Error fetching tree:", error);
      setMessage("Error fetching tree data");
    } finally {
      setIsLoading(false);
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
    setIsLoading(true);
    try {
      const response = await axios.post("http://127.0.0.1:5000/insert", { key: parseInt(key) });
      console.log("Tree after insertion:", response.data.tree);
      setTreeData(null); // Force re-render
      setTimeout(() => setTreeData(response.data.tree), 0);
      setKey("");
      setMessage(response.data.message);  // Display success message
    } catch (error) {
      if (error.response && error.response.data.message) {
        console.error("Insert error:", error.response.data.message);
        setMessage(error.response.data.message);  // Display error message from the backend
      } else {
        console.error("Insert error:", error);
        setMessage("Error inserting node");
      }
    } finally {
      setIsLoading(false);
    }
  };

  // Delete a node
  const handleDelete = async () => {
    if (key === "" || isNaN(parseInt(key))) {
      setMessage("Please enter a valid number");
      return;
    }
    setIsLoading(true);
    try {
      const response = await axios.post("http://127.0.0.1:5000/delete", { key: parseInt(key) });
      console.log("Tree after deletion:", response.data.tree);
      setTreeData(null); // Force re-render
      setTimeout(() => setTreeData(response.data.tree), 0);
      setKey("");
      setMessage(response.data.message);  // Display success message
    } catch (error) {
      if (error.response && error.response.data.message) {
        console.error("Delete error:", error.response.data.message);
        setMessage(error.response.data.message);  // Display error message from the backend
      } else {
        console.error("Delete error:", error);
        setMessage("Error deleting node");
      }
    } finally {
      setIsLoading(false);
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
      <button onClick={handleInsert} disabled={isLoading || key === "" || isNaN(parseInt(key))}>
        {isLoading ? "Inserting..." : "Insert"}
      </button>
      <button onClick={handleDelete} disabled={isLoading || key === "" || isNaN(parseInt(key))}>
        {isLoading ? "Deleting..." : "Delete"}
      </button>
      {message && <p style={{ color: "red" }}>{message}</p>}
      {treeData ? <AVLTree treeData={treeData} /> : <p>{isLoading ? "Loading tree..." : "Tree is empty"}</p>}
    </div>
  );
}

export default App;
