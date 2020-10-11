import json
from pathlib import Path
from flask import abort
from typing import Optional
from dataclasses import dataclass

@dataclass
class Project:
    name: str
    demo: Optional[str]
    blog: Optional[str]
    source: Optional[str]
    image: str
    description: str

    @staticmethod
    def json_to_project(json):
        name = json['name']
        demo = json['demo']
        blog = json['blog']
        source = json['source']
        image = json['image']
        description = json['description']

        return Project(name, demo, blog, source, image, description)

class ProjectLoader:

    def __init__(self, app):
        self.app = app
        self.path = app.config['PROJECTLOADER_ROOT']
        self.projects = self.load_projects(self.path)

    def load_projects(self, filepath):
        try:
            with open(filepath, 'r') as f:
                raw_projects = json.load(f)
                projects = [Project.json_to_project(raw) for raw in raw_projects]

            return projects
        except e:
            with open(filepath, 'w') as f:
                raise e
                json.dump([], f)
                return []

    def __iter__(self):
        return self.projects.__iter__()