from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys
import json

import tensorflow as tf
import util

def fetch_model():
  config = util.initialize_from_env()
  log_dir = config["log_dir"]
  model = util.get_model(config)
  saver = tf.train.Saver()

  return model, saver

