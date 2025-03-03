import logging
from typing import Optional
import logging.config

def init_logger(loglevel, path: Optional[str] = None):
    logger = logging.getLogger(__name__)
    logger.setLevel(loglevel)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    if path:
        file_handler = logging.FileHandler(path)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    else:
        file_handler = None

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger

LOGGING_CONFIG = {
    'version': 1,
    'formatters': {
        'default': {
            'format': '%(name)s|%(levelname)4s| %(message)s',
            'datefmt': '%H:%M'
        }
    },
    'handlers': {
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'log_file.log',
            'formatter': 'default'
        },
        'stream': {
            'class': 'logging.StreamHandler',
            'formatter': 'default'
        }
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['file', 'stream']
    }
}

logging.config.dictConfig(LOGGING_CONFIG)



