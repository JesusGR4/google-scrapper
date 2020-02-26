#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging, os
log_file = os.getenv('PYTHON_LOG')
logging.basicConfig(filename=log_file, filemode='w', level=logging.DEBUG)
logger = logging.getLogger('basic_logging')
