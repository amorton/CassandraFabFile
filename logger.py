#!/usr/bin/env python
### Script provided by DataStax.

import urllib2, os, re, shlex, subprocess, time

configfile = 'ami.log'

def appendLog(text):
    with open(configfile, "a") as f:
        f.write(text + "\n")
        print text

def exe(command, log=True):
    # Helper function to execute commands and print traces of the command and output for debugging/logging purposes
    process = subprocess.Popen(shlex.split(command), stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    read = process.communicate()
    
    if log:
        # Print output on next line if it exists
        if len(read[0]) > 0:
            appendLog('[EXEC] ' + time.strftime("%m/%d/%y-%H:%M:%S", time.localtime()) + ' ' + command + ":\n" + read[0])
        elif len(read[1]) > 0:
            appendLog('[ERROR] ' + time.strftime("%m/%d/%y-%H:%M:%S", time.localtime()) + ' ' + command + ":\n" + read[1])
    
    if not log or (len(read[0]) == 0 and len(read[1]) == 0):
        appendLog('[EXEC] ' + time.strftime("%m/%d/%y-%H:%M:%S", time.localtime()) + ' ' + command)
    
    return process

def pipe(command1, command2, log=True):
    # Helper function to execute piping commands and print traces of the commands and output for debugging/logging purposes
    p1 = subprocess.Popen(shlex.split(command1), stdout=subprocess.PIPE)
    p2 = subprocess.Popen(shlex.split(command2), stdin=p1.stdout, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    p1.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits.
    read = p2.stdout.read()

    
    if not log:
        read = ""
    
    # Print output on next line if it exists
    if len(read) > 0:
        appendLog('[PIPE] ' + time.strftime("%m/%d/%y-%H:%M:%S", time.localtime()) + ' ' + command1 + ' | ' + command2 + ":\n" + read)
    else:
        appendLog('[PIPE] ' + time.strftime("%m/%d/%y-%H:%M:%S", time.localtime()) + ' ' + command1 + ' | ' + command2)

    output = p2.communicate()[0]
    
    if log:
        if output and len(output) > 0 and len(output[0]) > 0:
            appendLog('[PIPE] ' + time.strftime("%m/%d/%y-%H:%M:%S", time.localtime()) + ' ' + command1 + ' | ' + command2 + ":\n" + output[0])
        elif output and len(output) > 1 and len(output[1] > 0):
            appendLog('[PIPE] ' + time.strftime("%m/%d/%y-%H:%M:%S", time.localtime()) + ' ' + command1 + ' | ' + command2 + ":\n" + output[1])

        return output

def info(infotext):
    appendLog('[INFO] ' + str(infotext))

def warn(infotext):
    appendLog('[WARN] ' + str(infotext))

def error(infotext):
    appendLog('[ERROR] ' + str(infotext))
