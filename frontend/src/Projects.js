import React, { useState, useEffect } from "react";
import { io } from "socket.io-client";

const Projects = () => {
  const [projects, setProjects] = useState([]);
  const [notification, setNotification] = useState(null); // State for notifications

  useEffect(() => {
    const socket = io("http://localhost:5000");

    // Log connection success
    socket.on("connect", () => {
      console.log("WebSocket connected");
    });

    // Listen for real-time updates
    socket.on("project_update", (data) => {
      console.log("Real-time update received:", data.message);

      // Fetch updated projects list
      fetch("http://localhost:5000/projects")
        .then((response) => response.json())
        .then((data) => {
          console.log("Updated projects:", data);
          setProjects(data);
          setNotification("Projects have been updated!"); // Set notification message

          // Clear notification after 3 seconds
          setTimeout(() => setNotification(null), 3000);
        })
        .catch((error) => {
          console.error("Error fetching updated projects:", error);
        });
    });

    // Clean up the WebSocket connection on component unmount
    return () => socket.close();
  }, []);

  return (
    <div>
      <h1>Active Projects</h1>

      {/* Notification bar */}
      {notification && (
        <div style={{ backgroundColor: "yellow", padding: "10px", margin: "10px 0" }}>
          {notification}
        </div>
      )}

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
