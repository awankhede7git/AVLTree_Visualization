import React, { useState, useEffect } from "react";
import axios from "axios";
import AVLTree from "./AVLTree"; // AVL Tree visualization component
import "./App.css";

function App() {
  const [key, setKey] = useState("");
  const [message, setMessage] = useState("");
  const [treeData, setTreeData] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [rotations, setRotations] = useState([]);


  const fetchTree = async () => {
    setIsLoading(true);
    try {
      const response = await axios.get("http://127.0.0.1:5000/get_tree");
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

  // const handleInsert = async () => {
  //   if (key === "" || isNaN(parseInt(key))) {
  //     setMessage("Please enter a valid number");
  //     return;
  //   }
  //   setIsLoading(true);
  //   try {
  //     const response = await axios.post("http://127.0.0.1:5000/insert", { key: parseInt(key) });
  //     setTreeData(response.data.tree);
  //     setKey("");
  //     setMessage(response.data.message);
  //   } catch (error) {
  //     setMessage(error.response?.data?.message || "Error inserting node");
  //   } finally {
  //     setIsLoading(false);
  //   }
  // };
  const handleInsert = async () => {
    if (key === "" || isNaN(parseInt(key))) {
      setMessage("Please enter a valid number");
      return;
    }
    setIsLoading(true);
    try {
      const response = await axios.post("http://127.0.0.1:5000/insert", { key: parseInt(key) });
      setTreeData(response.data.tree);
      setKey("");
      setMessage(response.data.message);
      setRotations(response.data.rotations || []);
    } catch (error) {
      setMessage(error.response?.data?.message || "Error inserting node");
      setRotations([]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleDelete = async () => {
    if (key === "" || isNaN(parseInt(key))) {
      setMessage("Please enter a valid number");
      return;
    }
    setIsLoading(true);
    try {
      const response = await axios.post("http://127.0.0.1:5000/delete", { key: parseInt(key) });
      setTreeData(response.data.tree);
      setKey("");
      setMessage(response.data.message);
    } catch (error) {
      setMessage(error.response?.data?.message || "Error deleting node");
    } finally {
      setIsLoading(false);
    }
  };

  const handleSearch = async () => {
    if (key === "" || isNaN(parseInt(key))) {
      setMessage("Please enter a valid number");
      return;
    }
    setIsLoading(true);
    try {
      const response = await axios.post("http://127.0.0.1:5000/search", { key: parseInt(key) });
      setMessage(response.data.message);
    } catch (error) {
      setMessage(error.response?.data?.message || "Error searching node");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="App">
      <h1>AVL Tree Operations</h1>
      <input
        type="number"
        placeholder="Enter key"
        value={key}
        onChange={(e) => setKey(e.target.value)}
      />
      <div>
        <button onClick={handleInsert} disabled={isLoading}>Insert</button>
        <button onClick={handleDelete} disabled={isLoading}>Delete</button>
        <button onClick={handleSearch} disabled={isLoading}>Search</button>
      </div>
      {isLoading && <div>Loading...</div>}
      {message && <p>{message}</p>}
      {rotations.length > 0 && (
        <div className="rotations">
          <h3>Rotations:</h3>
          <ul>
            {rotations.map((rot, index) => (
              <li key={index}>{rot}</li>
            ))}
          </ul>
        </div>
      )}

      <AVLTree treeData={treeData} />
    </div>
  );
}

export default App;
