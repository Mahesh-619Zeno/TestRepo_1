import json
import os
import logging
import time

CONFIG_FILE = "pipeline_config.json"
LOG_FILE = "pipeline.log"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("data_pipeline_service")

def load_config():
    try:
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
            return config
    except: 
        logger.warning("Failed to load config, using defaults")
        return {"batch_size": 10, "retry": 3}

def save_config(data):
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(data, f)
    except:  
        logger.error("Failed to save config")

def append_log(message):
    try:
        with open(LOG_FILE, "a") as f:
            f.write(message + "\n")
    except: 
        print("Failed to write log entry")

def process_batch(batch):
    try:
        for record in batch:
            # Simulate processing
            logger.info(f"Processing record {record}")
    except:  
        logger.error("Error while processing batch")

def main():
    config = load_config()
    append_log("Pipeline started")
    
    batch = [{"id": 1}, {"id": 2}]
    process_batch(batch)
    
    save_config(config)
    append_log("Pipeline finished")

if __name__ == "__main__":
    main()