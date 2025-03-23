import React, { useEffect, useRef } from "react";
import { Network } from "vis-network/standalone";
//import "vis-network/styles/vis-network.css";

const AVLTree = ({ treeData }) => {
  const containerRef = useRef(null);

  useEffect(() => {
    if (!treeData || !containerRef.current) return;

    // Convert treeData to Vis.js compatible format
    const nodes = [];
    const edges = [];

    const traverse = (node, parent = null) => {
      if (!node) return;
      nodes.push({
        id: node.key,
        label: String(node.key),
        color: {
          background: "#7b3fa9", // Purple node color 
          border: "#5b2c82", // Darker purple border 
          highlight: { background: "#a460f0", border: "#8a40d6" }, // Highlight color when selected 
          hover: {
            border: "#16a085", // Green border on hover
            background: "#1abc9c", // Light green background on hover
          },
        },
        font: { color: "#ffffff", size: 18 }, // White text
      });

      if (parent !== null) {
        edges.push({ from: parent, to: node.key });
      }

      traverse(node.left, node.key);
      traverse(node.right, node.key);
    };

    traverse(treeData);

    const data = { nodes, edges };
    const options = {
      layout: {
        hierarchical: {
          direction: "UD",
          sortMethod: "directed",
        },
      },
      edges: {
        arrows: "to",
      },
    };

    const network = new Network(containerRef.current, data, options);

    return () => network.destroy();
  }, [treeData]);

  return (
    <div
      ref={containerRef}
      style={{ width: "600px", height: "400px", border: "1px solid black" }}
    />
  );
};

export default AVLTree;
