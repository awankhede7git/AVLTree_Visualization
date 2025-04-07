import React, { useEffect, useRef } from "react";
import { Network } from "vis-network/standalone";

const AVLTree = ({ treeData }) => {
  const containerRef = useRef(null);

  useEffect(() => {
    if (!treeData || !containerRef.current) return;

    const nodes = [];
    const edges = [];
    const addedNodes = new Set(); // Track added nodes to prevent duplicates

    // 🔹 Traverse the tree and assign level-based positions
    const traverse = (node, parent = null, level = 0) => {
      if (!node) return;

      // ✅ Avoid duplicate node IDs
      if (!addedNodes.has(node.key)) {
        nodes.push({
          id: node.key,
          label: ` ${node.key} \n (L ${level})`, // Show level in node
          level: level, // Track node's level
          color: {
            background: "#7b3fa9",
            border: "#5b2c82",
            highlight: { background: "#a460f0", border: "#8a40d6" },
            hover: { border: "#16a085", background: "#1abc9c" },
          },
          font: { color: "#ffffff", size: 18 },
        });
        addedNodes.add(node.key);
      }

      if (parent !== null) {
        edges.push({ from: parent, to: node.key });
      }

      traverse(node.left, node.key, level + 1);
      traverse(node.right, node.key, level + 1);
    };

    traverse(treeData);

    const data = { nodes, edges };
    const options = {
      layout: {
        hierarchical: {
          direction: "UD", // Top to Bottom
          sortMethod: "directed",
          nodeSpacing: 100,
          levelSeparation: 100, // Space between levels
        },
      },
      edges: {
        arrows: { to: true },
      },
      physics: false, // Keep nodes fixed
    };

    const network = new Network(containerRef.current, data, options);

    return () => network.destroy();
  }, [treeData]);

  return (
    <div
      ref={containerRef}
      style={{ width: "700px", height: "500px", border: "2px solid black" }}
    />
  );
};

export default AVLTree;
