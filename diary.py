#!/usr/bin/python

import os
import subprocess
import time
import Crypto.Cipher.AES

def set_default_editor() :
    """Sets the default editor."""

    osedit = os.getenv('EDITOR')
    if osedit == None :
        defedit = "vim"
    else :
        defedit = osedit
    return defedit

def set_diary_path() :
    """
    Sets the default diary path.
    """

    oshome = os.getenv('HOME')
    diary_path = oshome + '/.vivek/diary/'
    return diary_path

class Diary_Prefs :
    def __init__(cls, edit='default', diary_path='default') :
        if edit == 'default' :
            cls.editor = set_default_editor()
        else :
            cls.editor = edit
        if diary_path == 'default' :
            cls.diary_path = set_diary_path()
        else :
            cls.diary_path = diary_path
        return None

    def __repr__(cls) :
        editstr =      "Edior: " + cls.editor
        diarstr = "    Diary path: " + cls.diary_path + " ."
        return editstr + diarstr

    def __str__(cls) :
        return cls.__repr__()

def extract_time_file_name() :
    """
    Checks the current time and returns a string which will form the
    initial part of the file name.
    """

    timestr = time.strftime('%Y%m%d_%H%M')
    return timestr

def extract_time_header() :
    """Returns a time stamp to be used as the header."""

    return time.ctime()

def run_command(cmdlst) :
    """
    Given a string, it runs it on a shell.
    1 argument: a list of strings containing the command
    """

    try :
        subprocess.check_call(cmdlst)
    except :
        print "Error: run_command:", ' '.join(cmdlst)


def check_and_create_main (diaryprefs) :
    """
    It creates an environment for main.tex and finally creates it.
    """

    mainfile = diaryprefs.diary_path + 'main.tex'
    mainhead = diaryprefs.diary_path + 'mainhead.tem'
    mainfoot = diaryprefs.diary_path + 'mainfoot.tem'
    maindata = diaryprefs.diary_path + 'maindata.lst'

    mainheadtxt="""
\\documentclass{article}

\\title{Diary}
\\author{}
\\begin{document}
\\maketitle
\\tableofcontents
"""

    mainfoottxt="""
\\end{document}
"""

    # First create the directories of necessary.

    if not os.path.isdir(diaryprefs.diary_path) :
        os.makedirs(diaryprefs.diary_path, 0700)

    if not os.path.isfile(mainhead) :
        with open(mainhead, 'w') as mh :
            mh.write(mainheadtxt)

    if not os.path.isfile(mainfoot) :
        with open(mainfoot, 'w') as mf :
            mf.write(mainfoottxt)

    if os.path.isfile(maindata) :
        with open(mainfile, 'w') as mfl :
            # Write header
            with open(mainhead, 'r') as mh :
                for line in mh :
                    mfl.write(line)
            with open(maindata, 'r') as md :
                for dayentry in md :
                    texline = '\include{' + dayentry.strip() + '}'
                    mfl.write(texline + '\n')
            with open(mainfoot, 'r') as mf :
                for line in mf :
                    mfl.write(line)

def get_diary_entry(diaryprefs) :
    maindata = diaryprefs.diary_path + 'maindata.lst'
    timestamp = extract_time_file_name()
    diary_file = diaryprefs.diary_path + timestamp + '.tex'

    print "Writing in:", diary_file

    heading = '\\section{' + extract_time_header() + '}\n'
    with open(diary_file, 'a') as df :
        df.write(heading)

    run_command([diaryprefs.editor, diary_file])
    with open(maindata, 'a') as md :
        md.write(timestamp + '\n')

def compile_main_file(diaryprefs) :
    curr_dir = os.getcwd()
    os.chdir(diaryprefs.diary_path)
    run_command(['fulltex', 'main.tex'])
    os.chdir(curr_dir)

def show_main_file(diaryprefs) :
    run_command(['zathura', diaryprefs.diary_path + 'main.pdf'])


def encrypt_message(rawstr, passphrase, iv) :
    aes_block_size = Crypto.Cipher.AES.block_size

    # blocksize should divide length of messsage:
    padstrln = aes_block_size - (len(rawstr) % aes_block_size)
    rawstr = rawstr + ' ' * padstrln

    passlen = len(passphrase)
    if passlen > aes_block_size :
        passphrasenew = passphrase[:aes_block_size]
    else :
        padsize = aes_block_size - (passlen % aes_block_size)
        passphrasenew = passphrase + ' ' * padsize

    aes = Crypto.Cipher.AES.new(passphrasenew, Crypto.Cipher.AES.MODE_CBC, iv)
    cipher = aes.encrypt(rawstr)
    return cipher


    print passlen
    print rawstr, aes_block_size, len(rawstr)
    print passphrasenew, aes_block_size, len(passphrasenew)

dp = Diary_Prefs(edit='vim')

check_and_create_main(dp)
get_diary_entry(dp)
check_and_create_main(dp)
compile_main_file(dp)
show_main_file(dp)
print encrypt_message('Hello Uma!', 'abcdef', 'abcdefghijklmnop')
