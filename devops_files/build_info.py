import os

BUILD_VERSION = os.getenv("BUILD_VERSION", "local-dev")
GIT_COMMIT = os.getenv("GIT_COMMIT", "unknown")

def get_build_info():
    return {"build_version": BUILD_VERSION, "git_commit": GIT_COMMIT}

if __name__ == "__main__":
    print("📦 Build Info:")
    for k, v in get_build_info().items():
        print(f"{k}: {v}")
