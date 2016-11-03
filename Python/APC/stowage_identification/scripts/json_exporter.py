#!/usr/bin/env python
import rospy
import json
from apc_msgs.srv import *
from apc_msgs.msg import *
import IPython

def json_exporter(bins, filename, num_2_item_dict):
    out_data = dict()
    bin_content_dict = dict()
    for b in bins:
      bin_name = b.name
      item_list = []
      for item in b.bin_contents:
        item_list.append(num_2_item_dict[str(item)])
      bin_content_dict[bin_name] = item_list

    out_data['bin_contents'] = bin_content_dict

    with open(filename, 'w') as outfile:
      json.dump(out_data, outfile, sort_keys=True, indent=4, separators=(',',': '))
