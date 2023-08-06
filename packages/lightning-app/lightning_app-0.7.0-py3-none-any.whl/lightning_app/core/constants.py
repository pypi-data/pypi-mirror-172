import os
from pathlib import Path

import lightning_cloud.env

import lightning_app

SUPPORTED_PRIMITIVE_TYPES = (type(None), str, int, float, bool)
STATE_UPDATE_TIMEOUT = 0.001
STATE_ACCUMULATE_WAIT = 0.05
# Duration in seconds of a moving average of a full flow execution
# beyond which an exception is raised.
FLOW_DURATION_THRESHOLD = 1.0
# Number of samples for the moving average of the duration of flow execution
FLOW_DURATION_SAMPLES = 5

APP_SERVER_HOST = os.getenv("LIGHTNING_APP_STATE_URL", "http://127.0.0.1")
APP_SERVER_PORT = 7501
APP_STATE_MAX_SIZE_BYTES = 1024 * 1024  # 1 MB
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", None)
REDIS_QUEUES_READ_DEFAULT_TIMEOUT = 0.005
REDIS_WARNING_QUEUE_SIZE = 1000
USER_ID = os.getenv("USER_ID", "1234")
FRONTEND_DIR = os.path.join(os.path.dirname(lightning_app.__file__), "ui")
PACKAGE_LIGHTNING = os.getenv("PACKAGE_LIGHTNING", None)
CLOUD_UPLOAD_WARNING = int(os.getenv("CLOUD_UPLOAD_WARNING", "2"))
DISABLE_DEPENDENCY_CACHE = bool(int(os.getenv("DISABLE_DEPENDENCY_CACHE", "0")))
# Project under which the resources need to run in cloud. If this env is not set,
# cloud runner will try to get the default project from the cloud
LIGHTNING_CLOUD_PROJECT_ID = os.getenv("LIGHTNING_CLOUD_PROJECT_ID")
LIGHTNING_CREDENTIAL_PATH = os.getenv("LIGHTNING_CREDENTIAL_PATH", str(Path.home() / ".lightning" / "credentials.json"))
DOT_IGNORE_FILENAME = ".lightningignore"
DEBUG_ENABLED = bool(int(os.getenv("LIGHTNING_DEBUG", "0")))
LIGHTNING_COMPONENT_PUBLIC_REGISTRY = "https://lightning.ai/v1/components"
LIGHTNING_APPS_PUBLIC_REGISTRY = "https://lightning.ai/v1/apps"
ENABLE_STATE_WEBSOCKET = bool(int(os.getenv("ENABLE_STATE_WEBSOCKET", "0")))

DEBUG: bool = lightning_cloud.env.DEBUG


def get_lightning_cloud_url() -> str:
    # DO NOT CHANGE!
    return os.getenv("LIGHTNING_CLOUD_URL", "https://lightning.ai")
