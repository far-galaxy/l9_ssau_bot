import os
import logging
import logging.handlers

def init_logger(logger):
	if not os.path.isdir(f'logs'):
		os.makedirs(f'logs') 


	f_handler = logging.handlers.TimedRotatingFileHandler('./logs/log', 
	                                                      when='midnight', 
	                                                      #atTime=datetime.time(11,25), 
	                                                      encoding="utf-8")

	f_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', 
	                             datefmt='%d-%b-%y %H:%M:%S')
	f_handler.setFormatter(f_format)
	logger.addHandler(f_handler)

	c_handler = logging.StreamHandler()
	c_format = logging.Formatter('%(levelname)s : %(message)s')
	c_handler.setFormatter(c_format)
	logger.addHandler(c_handler)
	logger.setLevel(logging.NOTSET)