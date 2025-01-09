# AI-Powered Conversational Application

## Background

In today’s fast-paced digital landscape, professionals and businesses require tools that streamline workflows, enhance collaboration, and adapt to diverse use cases. This **AI-powered conversational application** is designed to address these needs by leveraging cutting-edge AI technologies and robust architecture to deliver intelligent, context-aware interactions. 

The application integrates seamlessly with multiple external AI models, enabling it to cater to a wide range of industries and use cases. From managing complex datasets to providing real-time guidance, it empowers users to achieve more with less effort.

---

## Features

1. **Intelligent Conversations**:
   - Supports AI-powered, context-aware interactions.
   - Integrates with multiple AI models (e.g., DeepSeek V3, GPT-based models, Claude).

2. **Multi-Project Management**:
   - Create and manage isolated project workspaces.
   - Tailored AI responses based on the current project context.

3. **Dynamic Resource Allocation**:
   - Efficient use of system resources to optimize performance.
   - Supports scalable deployments across local and cloud environments.

4. **File and Data Management**:
   - Centralized storage for project-specific files.
   - Real-time file retrieval and advanced similarity search using Milvus.

5. **Undo and Edit Functionalities**:
   - Modify conversation history for improved user control.

6. **Health Monitoring and Testing**:
   - Built-in health check endpoint for service monitoring.
   - Automated testing scripts ensure system reliability.

---

## Benefits

1. **Increased Productivity**:
   - Automates repetitive tasks and accelerates decision-making with intelligent suggestions.

2. **Seamless Collaboration**:
   - Provides project-specific workspaces for teams, ensuring clear context and data isolation.

3. **Scalability**:
   - Designed to handle an increasing number of projects and users without performance degradation.

4. **Enhanced Control**:
   - Features like Undo and Edit give users more control over their interactions.

5. **Simplified Deployment**:
   - Docker Compose ensures one-click deployment and consistent environments across systems.

---

## Use Cases

1. **Freelancers and Consultants**:
   - Manage multiple client projects with isolated workspaces and tailored AI assistance.

2. **Development Teams**:
   - Collaborate on complex software projects, leveraging context-aware guidance and real-time file management.

3. **Enterprises**:
   - Deploy AI-driven solutions for customer support, data analysis, and internal process optimization.

4. **Educational Institutions**:
   - Provide AI-powered tools for research, learning, and administrative tasks.

5. **Startups**:
   - Scale effortlessly with a versatile and cost-effective architecture.

---

## Overview of Architecture

The application is built using a modular and containerized architecture, ensuring scalability and reliability:
- **PostgreSQL**: For structured data storage.
- **Redis**: For caching and real-time features.
- **etcd**: For distributed key-value storage and service discovery.
- **MinIO**: For object storage, ideal for managing files.
- **Milvus**: For advanced similarity search and data indexing.
- **Backend**: Python-based API providing core functionalities.
- **Frontend**: React-based interface for a seamless user experience.

---

This background story and overview aim to provide a comprehensive understanding of the application's purpose, capabilities, and value proposition.

## Project Directory Structure
persista
├── backend/
│   ├── src/
│   │   ├── __init__.py
│   │   ├── __pycache__/
│   │   ├── main.py
│   │   └── other_files.py
│   ├── tests/
│   ├── __init__.py
│   ├── __pycache__/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
├── database/
│   ├── migrations/
│   └── scripts/
├── docs/
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   ├── Dockerfile
│   └── package.json
├── logs/
├── project-workspaces/
│   ├── .gitkeep
│   └── README.md
├── venv/
│   ├── Include/
│   ├── Lib/
│   │   └── site-packages/
│   ├── Scripts/
│   └── pyvenv.cfg
├── .env
├── .gitattributes
├── .gitignore
├── docker-compose.yml
├── initialize_project.sh
├── milvus.log
├── README.md
├── test_milvus.py
├── test_results.log
├── test_services.bat
└── test_services.sh


## 1. Project Initialization and Configuration

### Overview
The project setup was designed to leverage containerization and ensure modularity, scalability, and efficiency. The configuration included key components for backend, frontend, database, caching, and vector search, using Docker Compose for seamless orchestration.

### Key Components and Configuration

1. **PostgreSQL**:
   - Used for structured data storage.
   - Exposed on port `5432` for external access.
   - Data persistence configured using Docker volumes.

2. **Redis**:
   - Used for caching and real-time features.
   - Exposed on port `6379`.

3. **etcd**:
   - Used for distributed key-value storage and service discovery.
   - Configured with auto-compaction and snapshot settings for optimized performance.
   - Exposed on port `7275`.

4. **MinIO**:
   - Object storage solution used for managing files.
   - Exposed on ports `9000` (API) and `9001` (console).
   - Configured with default credentials for initial setup.

5. **Milvus**:
   - A vector database for advanced similarity search and data indexing.
   - Integrated with etcd and MinIO for metadata and file storage.
   - Exposed on ports `19530` (API) and `9091` (monitoring).

6. **Backend**:
   - Custom Python application containerized and exposed on port `5000`.
   - Dependent on PostgreSQL, Redis, and Milvus.

7. **Frontend**:
   - React-based frontend containerized and exposed on port `4283`.
   - Configured for hot-reloading during development.

8. **Networking**:
   - All services connected via a bridge network (`persista-network`) for seamless communication.

9. **Volumes**:
   - Persistent storage configured for all services to retain data across container restarts.

### Docker Compose File
The `docker-compose.yml` file was created to orchestrate the above services. Key highlights include:
- Defined services for PostgreSQL, Redis, etcd, MinIO, Milvus, backend, and frontend.
- Configured health checks for critical services to ensure reliable startup and operation.
- Resources allocated dynamically to ensure efficient utilization of system capacity.

### Execution
1. To start the services:
   ```bash
   docker-compose up --build

## 2. Project Workspaces Integration

The **`project-workspaces`** directory has been integrated into the project to provide a centralized location for managing project-specific data and configurations. This ensures that the application can handle multiple projects effectively while maintaining data isolation and organization.

### Purpose
The `project-workspaces` directory is designed to:
- Serve as a base for organizing project-specific files and configurations.
- Support multi-project management by isolating data and preventing mix-ups.
- Enable easy access to project data for the backend container.

### Changes to `docker-compose.yml`
1. Added a new volume named `project_workspaces_data` to the `volumes` section:
   ```yaml
   volumes:
     project_workspaces_data:

2. Mapped the volume to the `project-workspaces` directory in the `backend` service:
   ```yaml
   backend:
     volumes:
       - ./project-workspaces:/project-workspaces
