#!/usr/bin/env python
import optparse
import os
import pexpect
import sys
import json
import jsonrpclib


def init_corenlp_command(corenlp_path, memory, properties):
    """
    Checks the location of the jar files.
    Spawns the server as a process.
    """

    jars = ["stanford-corenlp-3.3.1.jar",
            "stanford-corenlp-3.3.1-models.jar",
            "ejml-0.23.jar"
            ]

    java_path = "java"
    classname = "edu.stanford.nlp.sentiment.SentimentPipeline"

    # add and check classpaths
    jars = [corenlp_path + "/" + jar for jar in jars]
    for jar in jars:
        if not os.path.exists(jar):
            raise Exception("Error! Cannot locate: %s" % jar)

    # add memory limit on JVM
    if memory:
        limit = "-Xmx%s" % memory
    else:
        limit = ""

    return "%s %s -cp %s %s %s" % (java_path, limit, ':'.join(jars),
                                   classname, '-stdin')



class StanfordCoreNLPSentimentServer:

    """
    Command-line interaction with Stanford's CoreNLP java utilities.
    Can be run as a JSON-RPC server or imported as a module.
    """

    def _spawn_corenlp(self):
        self.corenlp = pexpect.spawn(self.start_corenlp, timeout=5,
                                     maxread=8192, searchwindowsize=80)

        self.corenlp.expect("reached.")
        self.corenlp.readline()

    def __init__(self, corenlp_path, memory="2g", properties='default.properties', serving=False):
        """
        Checks the location of the jar files.
        Spawns the server as a process.
        """

        # spawn the server
        self.serving = serving
        self.start_corenlp = init_corenlp_command(corenlp_path, memory, properties)
        self._spawn_corenlp()


    def close(self, force=True):
        self.corenlp.terminate(force)

    def isalive(self):
        return self.corenlp.isalive()

    def __del__(self):
        # If our child process is still around, kill it
        if self.isalive():
            self.close()


    def parse(self, text):
        """
        This function takes a text string, sends it to the Stanford parser,
        reads in the result, parses the results and returns a list
        with one dictionary entry for each parsed sentence.
        """
        self.corenlp.sendline(text)
        try:
            self.corenlp.expect("\r\n  ")
        except Exception as e:
            print e
            pass

        data = self.corenlp.readline().strip()
        return data



class StanfordNLPSentimentClient:

    def __init__(self, url):
        self.server = jsonrpclib.Server(url)


    def classify(self, text):
        return self.server.parse(text)