logger_config = {
    'version': 1,
    'formatters': {
        'std_format': {
            'format': '{asctime} - {levelname} - {name} - {message}',
            'style':'{',
            },
        },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'std_format',
            'level': 'DEBUG',
            },
        },
    'loggers': {
        'main_logger': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}