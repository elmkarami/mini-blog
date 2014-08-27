#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This starts out pretty simple -- just automating deployment on a Heroku server with a few commands.
"""

from fabric.operations import local
        
def update_dependencies():
    """Update requirements locally."""
    local('pip freeze -> requirements.txt')


def deploy(msg):
    "Full deploy: push to Heroku"
    update_dependencies()
    local("git push heroku master")
