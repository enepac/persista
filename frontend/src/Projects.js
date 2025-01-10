import React, { useState, useEffect } from "react";
import { io } from "socket.io-client";

const Projects = () => {
  const [projects, setProjects] = useState([]);

  useEffect(() => {
    // Connect to the WebSocket server
    const socket = io("http://localhost:5000");

    // Log connection success
    socket.on("connect", () => {
      console.log("WebSocket connected");
      // Emit a test event to the server
      socket.emit("test_event", { data: "Hello from frontend!" });
    });

    // Handle server responses
    socket.on("response_event", (data) => {
      console.log("Response from server:", data.message);
    });

    // Fetch initial projects data
    fetch("http://localhost:5000/projects")
      .then((response) => response.json())
      .then((data) => {
        console.log("Fetched projects:", data);
        setProjects(data);
      })
      .catch((error) => {
        console.error("Error fetching projects:", error);
      });

    // Handle WebSocket disconnection
    socket.on("disconnect", () => {
      console.log("WebSocket disconnected");
    });

    // Clean up the WebSocket connection on component unmount
    return () => socket.close();
  }, []);

  return (
    <div>
      <h1>Active Projects</h1>
      <ul>
        {projects.map((project) => (
          <li key={project.id}>
            <strong>{project.name}</strong> - Priority:{" "}
            {project.additional_metadata?.priority || "N/A"}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Projects;
