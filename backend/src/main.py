from flask import Flask, request, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from dotenv import load_dotenv
import os
import shutil
import csv
from io import StringIO
import requests
import PyPDF2
from pytesseract import image_to_string
from PIL import Image
import magic

# Load environment variables
load_dotenv()

# Retrieve the API key
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

app = Flask(__name__)

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI")
db = SQLAlchemy(app)


# Project Model
class Project(db.Model):
    __tablename__ = "projects"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    project_data = db.Column(db.JSON, default={})
    additional_metadata = db.Column(db.JSON, default={})


class Knowledgebase(db.Model):
    __tablename__ = "knowledgebase"
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(
        db.Integer, db.ForeignKey("projects.id", ondelete="CASCADE"), nullable=False
    )
    content_type = db.Column(db.String(50), nullable=False)
    content = db.Column(db.JSON, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Conversation(db.Model):
    __tablename__ = "conversations"
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(
        db.Integer, db.ForeignKey("projects.id", ondelete="CASCADE"), nullable=False
    )
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    revision_id = db.Column(db.Integer, default=0)
    original_message = db.Column(db.Text, nullable=True)
    updated_message = db.Column(db.Text, nullable=True)
    updated_at = db.Column(db.DateTime, nullable=True)


# Create project
@app.route("/projects", methods=["POST"])
def create_project():
    data = request.json
    new_project = Project(
        name=data["name"],
        project_data=data.get("project_data", {}),
        additional_metadata=data.get("additional_metadata", {}),
    )
    db.session.add(new_project)
    db.session.commit()

    # Add to knowledgebase
    entry = Knowledgebase(
        project_id=new_project.id,
        content_type="summary",
        content={
            "name": new_project.name,
            "metadata": new_project.additional_metadata,
            "project_data": new_project.project_data,
        },
    )
    db.session.add(entry)
    db.session.commit()

    # Create directory for the new project
    project_dir = f"project-workspaces/{new_project.id}"
    os.makedirs(project_dir, exist_ok=True)

    return jsonify({"message": "Project created", "project_id": new_project.id}), 201


# Get all projects
@app.route("/projects", methods=["GET"])
def get_projects():
    projects = Project.query.all()
    return (
        jsonify(
            [
                {
                    "id": project.id,
                    "name": project.name,
                    "created_at": project.created_at,
                    "project_data": project.project_data,
                    "additional_metadata": project.additional_metadata,
                }
                for project in projects
            ]
        ),
        200,
    )


# Get a single project
@app.route("/projects/<int:project_id>", methods=["GET"])
def get_project(project_id):
    project = Project.query.get_or_404(project_id)
    return (
        jsonify(
            {
                "id": project.id,
                "name": project.name,
                "created_at": project.created_at,
                "project_data": project.project_data,
                "additional_metadata": project.additional_metadata,
            }
        ),
        200,
    )


# Update a project
@app.route("/projects/<int:project_id>", methods=["PUT"])
def update_project(project_id):
    project = Project.query.get_or_404(project_id)
    data = request.json
    project.name = data.get("name", project.name)
    project.project_data = data.get("project_data", project.project_data)
    project.additional_metadata = data.get(
        "additional_metadata", project.additional_metadata
    )
    db.session.commit()

    # Update knowledgebase
    entry = Knowledgebase.query.filter_by(
        project_id=project.id, content_type="summary"
    ).first()
    if entry:
        entry.content = {
            "name": project.name,
            "metadata": project.additional_metadata,
            "project_data": project.project_data,
        }
        db.session.commit()

    return jsonify({"message": "Project updated"}), 200


# Delete a project
@app.route("/projects/<int:project_id>", methods=["DELETE"])
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)
    db.session.delete(project)
    db.session.commit()

    # Remove the project directory
    project_dir = f"project-workspaces/{project_id}"
    if os.path.exists(project_dir):
        shutil.rmtree(project_dir)

    return jsonify({"message": "Project deleted"}), 200


@app.route("/knowledgebase/populate", methods=["POST"])
def populate_knowledgebase():
    projects = Project.query.all()
    for project in projects:
        entry = Knowledgebase(
            project_id=project.id,
            content_type="summary",
            content={
                "name": project.name,
                "metadata": project.additional_metadata,
                "project_data": project.project_data,
            },
        )
        db.session.add(entry)
    db.session.commit()
    return jsonify({"message": "Knowledgebase populated"}), 201


@app.route("/knowledgebase/search", methods=["GET"])
def search_knowledgebase():
    filters = request.args
    query = Knowledgebase.query

    if "content_type" in filters:
        query = query.filter_by(content_type=filters["content_type"])

    if "project_id" in filters:
        query = query.filter_by(project_id=filters["project_id"])

    if "priority" in filters:
        query = query.filter(
            Knowledgebase.content["metadata"].op("->>")("priority")
            == filters["priority"]
        )

    if "tags" in filters:
        query = query.filter(
            Knowledgebase.content["metadata"]
            .op("->>")("tags")
            .contains(filters["tags"])
        )

    results = query.all()
    return (
        jsonify(
            [
                {
                    "id": entry.id,
                    "project_id": entry.project_id,
                    "content_type": entry.content_type,
                    "content": entry.content,
                    "created_at": entry.created_at,
                }
                for entry in results
            ]
        ),
        200,
    )


@app.route("/knowledgebase/export", methods=["GET"])
def export_knowledgebase():
    format = request.args.get("format", "json")
    entries = Knowledgebase.query.all()

    if format == "csv":
        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(["ID", "Project ID", "Content Type", "Content", "Created At"])
        for entry in entries:
            writer.writerow(
                [
                    entry.id,
                    entry.project_id,
                    entry.content_type,
                    entry.content,
                    entry.created_at,
                ]
            )
        output.seek(0)
        return Response(
            output,
            mimetype="text/csv",
            headers={"Content-Disposition": "attachment;filename=knowledgebase.csv"},
        )

    # Default JSON response
    return (
        jsonify(
            [
                {
                    "id": entry.id,
                    "project_id": entry.project_id,
                    "content_type": entry.content_type,
                    "content": entry.content,
                    "created_at": entry.created_at,
                }
                for entry in entries
            ]
        ),
        200,
    )

#upload file
@app.route("/projects/<int:project_id>/upload", methods=["POST"])
def upload_file(project_id):
    project = Project.query.get_or_404(project_id)
    file = request.files["file"]
    file_name = file.filename

    # Save the file
    folder_recommendation = "general"
    project_dir = f"project-workspaces/{project_id}/{folder_recommendation}"
    os.makedirs(project_dir, exist_ok=True)
    file_path = os.path.join(project_dir, file_name)
    file.save(file_path)

    # Skip file analysis temporarily
    extracted_content = "File analysis skipped for debugging."

    # Save placeholder metadata to the database
    knowledge_entry = Knowledgebase(
        project_id=project.id,
        content_type="file",
        content={
            "file_name": file_name,
            "file_type": "unknown",
            "extracted_content": extracted_content,
        },
    )
    db.session.add(knowledge_entry)
    db.session.commit()

    return (
        jsonify(
            {
                "message": "File uploaded successfully",
                "recommended_folder": folder_recommendation,
                "file_path": file_path,
            }
        ),
        201,
    )



@app.route("/conversations", methods=["POST"])
def create_conversation():
    data = request.json
    new_conversation = Conversation(
        project_id=data["project_id"], message=data["message"]
    )
    db.session.add(new_conversation)
    db.session.commit()

    return (
        jsonify(
            {
                "message": "Conversation created",
                "conversation_id": new_conversation.id,
                "project_id": new_conversation.project_id,
                "content": new_conversation.message,
                "created_at": new_conversation.created_at,
            }
        ),
        201,
    )


@app.route("/conversations/<int:conversation_id>", methods=["PUT"])
def edit_conversation(conversation_id):
    conversation = Conversation.query.get_or_404(conversation_id)
    data = request.json

    # Save the original message for tracking
    if not conversation.original_message:
        conversation.original_message = conversation.message
    conversation.updated_message = data.get(
        "updated_message", conversation.updated_message
    )
    conversation.updated_at = datetime.utcnow()
    db.session.commit()

    return (
        jsonify(
            {
                "message": "Conversation updated",
                "conversation_id": conversation.id,
                "original_message": conversation.original_message,
                "updated_message": conversation.updated_message,
                "updated_at": conversation.updated_at,
            }
        ),
        200,
    )


@app.route("/conversations/<int:conversation_id>", methods=["GET"])
def get_conversation(conversation_id):
    conversation = Conversation.query.get_or_404(conversation_id)
    return (
        jsonify(
            {
                "conversation_id": conversation.id,
                "project_id": conversation.project_id,
                "original_message": conversation.original_message,
                "updated_message": conversation.updated_message,
                "message": conversation.message,
                "created_at": conversation.created_at,
                "updated_at": conversation.updated_at,
            }
        ),
        200,
    )


def generate_ai_response(project_id, user_message):
    # Fetch the project from the database
    project = Project.query.get_or_404(project_id)

    # Build the project context to send to the AI model
    project_context = {
        "name": project.name,
        "metadata": project.additional_metadata,
        "project_data": project.project_data,
    }

    # Prepare the payload for the AI model API
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_message},
        ],
        "stream": False,
    }

    # Add your API key in the headers
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json",
    }

    # Send the request to the AI model API
    try:
        response = requests.post(
            "https://api.deepseek.com/chat/completions", json=payload, headers=headers
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

    # Return the AI-generated response
    return response.json()


@app.route("/projects/<int:project_id>/suggestions", methods=["POST"])
def get_contextual_suggestions(project_id):
    data = request.json
    user_message = data.get("message", "")
    suggestions = generate_ai_response(project_id, user_message)

    if "error" in suggestions:
        return (
            jsonify(
                {
                    "message": "Error generating suggestions",
                    "error": suggestions["error"],
                }
            ),
            500,
        )

    return (
        jsonify({"message": "Suggestions generated", "suggestions": suggestions}),
        200,
    )

if __name__ == "__main__":
    app.run(debug=True, port=5000)


