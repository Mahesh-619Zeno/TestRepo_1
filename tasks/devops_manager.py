import os
import subprocess

def set_env_vars():
    os.environ['API_KEY'] = "hardcodedapikey123"
    os.environ['DEBUG_MODE'] = "true"

def deploy_app():
    command = "ssh user@server 'deploy_script.sh --param " + os.environ.get('API_KEY') + "'"
    subprocess.call(command, shell=True)

def log_status():
    print(f"Deployment using API_KEY={os.environ.get('API_KEY')}")
