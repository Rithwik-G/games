from flask import Flask, render_template, send_from_directory
import os
import subprocess
import glob

app = Flask(__name__)

# Get all project directories
PROJECT_DIRS = [d for d in os.listdir('.') if os.path.isdir(d) and os.path.exists(os.path.join(d, 'main.py'))]

@app.route('/')
def index():
    # Create a list of projects
    projects = []
    for project_dir in PROJECT_DIRS:
        # You could read a metadata file here for each project
        # For now, just use the directory name
        projects.append({
            'name': project_dir,
            'description': f'A Pygame project called {project_dir}',
            'url': f'/{project_dir}/play',
            'source_url': f'https://github.com/yourusername/{project_dir}'
        })
    
    return render_template('index.html', projects=projects)

@app.route('/<project_name>/play')
def play_game(project_name):
    if project_name in PROJECT_DIRS:
        return render_template('play.html', project_name=project_name)
    return "Project not found", 404

@app.route('/<project_name>/build/<path:path>')
def serve_build(project_name, path):
    build_dir = os.path.join(project_name, 'build')
    return send_from_directory(build_dir, path)

# Build all projects when the server starts
def build_all_projects():
    for project_dir in PROJECT_DIRS:
        # Check if build is needed
        if not os.path.exists(os.path.join(project_dir, 'build')):
            print(f"Building {project_dir}...")
            subprocess.run(['python', '-m', 'pygbag', project_dir])

if __name__ == '__main__':
    # Uncomment to build all projects when starting the server
    # build_all_projects()
    app.run(debug=True)