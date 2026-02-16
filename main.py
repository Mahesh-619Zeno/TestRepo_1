#!/usr/bin/env python3
import click
import json
import os
from datetime import datetime
from tasks.task import TaskManager
from tasks.assign import assign_task, get_my_tasks
from tasks.search import search_tasks
from tasks.status import update_task_status

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

@click.group()
@click.pass_context
def cli(ctx):
    ctx.obj = TaskManager()
    ctx.obj.load_tasks()

@cli.command()
@click.argument('title')
@click.option('--desc', default='', help='Description')
@click.option('--priority', default='Medium', type=click.Choice(['Low', 'Medium', 'High']))
def create(title, desc, priority):
    """Create a new task."""
    ctx.obj.create_task(title, desc, priority)
    click.echo(f"Created task: {title}")

@cli.command()
def list():
    """List all tasks."""
    for task in ctx.obj.list_tasks():
        click.echo(f"{task['title']} ({task['status']}) - {task.get('assignee', 'Unassigned')}")

@cli.command()
@click.argument('title')
@click.argument('status')
def update(title, status):
    """Update task status."""
    update_task_status(ctx.obj, title, status)
    click.echo(f"Updated {title} to {status}")

@cli.command()
@click.argument('query')
def search(query):
    """Search tasks."""
    results = search_tasks(ctx.obj, query)
    for task in results:
        click.echo(task['title'])

@cli.command()
@click.argument('title')
@click.argument('user')
def assign(title, user):
    """Assign task to user."""
    assign_task(ctx.obj, title, user)
    click.echo(f"Assigned {title} to {user}")

@cli.command()
@click.argument('user')
def mytasks(user):
    """List my tasks."""
    tasks = get_my_tasks(ctx.obj, user)
    for task in tasks:
        click.echo(task['title'])

if __name__ == '__main__':
    cli()
