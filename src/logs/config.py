logging_config ={
	'version': 1,
	'formatters': {'default': {
		'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
	}},
	'handlers': {
		'wsgi': {
			'class': 'logging.StreamHandler',
			'stream': 'ext://flask.logging.wsgi_errors_stream',
			'formatter': 'default'
		},
		'login_h': {
			'class': 'logging.handlers.RotatingFileHandler',
			'filename': 'src/logs/logins.log',
			'formatter': 'default',
			'maxBytes': 1024 * 50,
			'backupCount': 3
		},
		'console': {
			'class': 'logging.handlers.RotatingFileHandler',
			'filename': 'src/logs/console.log',
			'formatter': 'default',
			'maxBytes': 1024 * 50,
			'backupCount': 3
		}

	},
	'root': {
		'level': 'INFO',
		'handlers': ['wsgi', 'console']
	},
	'login': {
		'level': 'INFO',
		'handlers': ['login_h']
	}
}
