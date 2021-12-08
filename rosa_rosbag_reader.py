#!/usr/bin/env python3


"""

Author: Thorsten Hempel

"""

import rosbag
import yaml
import os
import sys
import textwrap
import argparse
import csv

ROSA_TOPICS = ['/WS1/attention','/WS1/attention_visual', '/WS1/borderless/commands', '/WS1/reco_stt','/WS1/activebody' ]

def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("--bag", default="", type=str, help="Path to bag")
    parser.add_argument("--topic", default="", type=str,
                        help="topic to output")
    parser.add_argument("--info", help="print rosbag info",
                        action='store_true')
    parser.add_argument('--print', action='store_true')
    parser.add_argument('--export', action='store_true')
    parser.add_argument('--export_name', default='')
    parser.add_argument('--export_all', dest='export_all', action='store_true')
    args = parser.parse_args()
    return args


def writeAttentionToCSV(bag, topic, file=""):
    with open(file +'.csv', mode='w') as data_file:
        data_writer = csv.writer(
            data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        data_writer.writerow(['timestamp', 'data'])

        # Get all message on the /joint states topic
        for topic, msg, t in bag.read_messages(topics=[topic]):
            data_writer.writerow([t, msg.data])
    return file


def writeAttention_VisualToCSV(bag, topic, file=""):
    with open(file +'.csv', mode='w') as data_file:
        data_writer = csv.writer(
            data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        data_writer.writerow(['timestamp', 'id', 'visual'])

        # Get all message on the /joint states topic
        for topic, msg, t in bag.read_messages(topics=[topic]):
            data_writer.writerow([t, msg.id, msg.visual])
    return file


def writeBorderless_commandsToCSV(bag, topic, file=""):
    with open(file +'.csv', mode='w') as data_file:
        data_writer = csv.writer(
            data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        data_writer.writerow(['timestamp', 'command', 'text', 'x',
                             'y', 'size', 'r', 'g', 'b', 'a', 'r', 'g', 'b', 'a'])

        # Get all message on the /joint states topic
        for topic, msg, t in bag.read_messages(topics=[topic]):
            # Only write to CSV if the message is for our robot
            data_writer.writerow([t, msg.command, msg.text, msg.x, msg.y, msg.size, msg.color_fill.r, msg.color_fill.g, msg.color_fill.b,
                                 msg.color_fill.a, msg.color_stroke.r, msg.color_stroke.g, msg.color_stroke.b, msg.color_stroke.a])
    return file


def writeReco_sttToCSV(bag, topic, file=""):
    with open(file +'.csv', mode='w') as data_file:
        data_writer = csv.writer(
            data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        data_writer.writerow(['timestamp', 'data'])

        # Get all message on the /joint states topic
        for topic, msg, t in bag.read_messages(topics=[topic]):
            # Only write to CSV if the message is for our robot
            data_writer.writerow([t, msg.data,])
    return file


def writeActiveBodyToCSV(bag, topic, file=""):
    with open(file +'.csv', mode='w') as data_file:
        data_writer = csv.writer(
            data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
       
        header = 0
        # Get all message on the /joint states topic
        for topic, msg, t in bag.read_messages(topics=[topic]):
            rows = ['timestamp', 'IsTracked']
            iter = 0
            row_line = 2
            if header == 0:
                for JoinType in msg.Joints:
                    rows.append('JoinType: {} x'.format(iter))
                    rows.append('JoinType: {} y'.format(iter))
                    rows.append('JoinType: {} z'.format(iter))
                    rows.append('JoinType: {} TrackingState'.format(iter))
                    iter+=1
                header = 1
                data_writer.writerow(rows)
            data_row = [t, msg.IsTracked]
            for JoinType in msg.Joints:
                data_row.append(JoinType.X)
                data_row.append(JoinType.Y)
                data_row.append(JoinType.Z)
                data_row.append(JoinType.TrackingState)
            data_writer.writerow(data_row)
    return file

            
def writeTopicToCSV(bag, topic, file="", suppress_error = False):
    if file == "":
        _, file = os.path.split(topic)
    file_name = ''  
    if topic == '/WS1/attention':
        file_name = writeAttentionToCSV(bag, topic, file)
    elif topic == '/WS1/attention_visual':
        file_name = writeAttention_VisualToCSV(bag, topic, file)
    elif topic == '/WS1/borderless/commands':
        file_name = writeBorderless_commandsToCSV(bag, topic, file)
    elif topic == '/WS1/reco_stt':
        file_name = writeReco_sttToCSV(bag, topic, file)
    elif topic == '/WS1/activebody':
        file_name = writeActiveBodyToCSV(bag, topic, file)
    else: 
        if not suppress_error: raise RuntimeError("Topic not supported for CSV export")
  
    if not file_name == '':
        print("Finished creating csv file! Saved to >>{}.csv<<.".format(file_name))

def exportAllTopicsToCSV(bag):
    for topic in ROSA_TOPICS:
        writeTopicToCSV(bag, topic, suppress_error=True)


def printMsgsInBagFile(bag, topic):
    no_msgs_found = True
    # Establish counters to keep track of the message number being received under each topic name
    msg_counters = {}  # empty dict
    total_count = 0
    bag_in = bag
    for topic, msg, t in bag_in.read_messages(topic):
        print("\n# =======================================")
        total_count += 1
        no_msgs_found = False
        # Keep track of individual message counters for each message type
        if topic not in msg_counters:
            msg_counters[topic] = 1
        else:
            msg_counters[topic] += 1

        # Print topic name and message receipt info
        print("# topic:           " + topic)
        print("# msg_count:       %u" % msg_counters[topic])
        # the comma at the end prevents the newline char being printed at the end in Python2; see:
        # https://www.geeksforgeeks.org/print-without-newline-python/
        print("# timestamp (sec): {:.9f}".format(t.to_sec())),
        print("# - - -")

        # Print the message
        print(msg)

    print("")
    print("# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    print("# Total messages found: {:>16}".format(total_count))
    print("#")
    for topic in msg_counters:
        print("#    {:<30} {:>4}".format(topic + ":", msg_counters[topic]))
    if no_msgs_found:
        print("# NO MESSAGES FOUND IN THESE TOPICS")
    print("#")
    print("# DONE.")
    print("# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")


# If this file is called directly, as opposed to imported, run this:
if __name__ == '__main__':
    args = parseArgs()
    bag = args.bag
    topic = args.topic
    info = args.info
    export = args.export
    export_name = args.export_name
    export_all = args.export_all

    bag = rosbag.Bag(bag, 'r')
    if info:
        info_dict = yaml.safe_load(bag._get_yaml_info())
        print(yaml.dump(info_dict))

    if not topic == '' and args.print:
        printMsgsInBagFile(bag, topic)

    if export:
        writeTopicToCSV(bag, topic, export_name)
    
    if export_all:
        exportAllTopicsToCSV(bag)

    bag.close()
    # printArgs(args) # for debugging
