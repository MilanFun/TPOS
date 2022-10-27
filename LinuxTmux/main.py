import os
import libtmux
import argparse
import shutil
import random
import socket
from contextlib import closing
from tqdm.auto import trange


"""
Constant variables for tmux session name, id adress for jupyter notebook environment, default path and name for virtual environment
"""
SESSION_NAME = "session-created-by-PtukhaA"
IP_ADDRESS = "127.0.0.1"
PATH = os.path.abspath(os.getcwd()) + "/virtualfolder"
VENV = "venv"


def find_free_port():
    """
    Find free port for starting jupyter notebook
    """
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('',0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        return s.getsockname()[1]


def generate_token():
    """
    Token generation for jupyter notebook initialization
    """

    chars = 'abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'

    password = ''
    for i in range(32):
        password += random.choice(chars)

    return password



def start(sessions, num_users):
    """
    Initializing of $num_users environments in path $PATH
    """

    t = trange(num_users, desc='Starting', leave=True)
    result = list()

    for i in t:
        port = str(find_free_port())
        venv = VENV + str(i + 1)
        path = PATH + "/" + venv
        token = generate_token()

        if not os.path.exists(path=path):
            os.mkdir(path=path)
        
        window = sessions.new_window("{}".format(str(i + 1)), attach=False)
        pane = window.split_window(attach=False)

        pane.send_keys("python3 -m venv {}".format(path), enter=True)
        pane.send_keys("cd {}".format(path), enter=True)
        pane.send_keys("source bin/activate", enter=True)
        pane.send_keys("jupyter notebook --ip {} --port {} --no-browser --NotebookApp.token='{}' --NotebookApp.notebook_dir='{}'".format(IP_ADDRESS, port, token, path), enter=True)

        t.set_description("Starting {} environment".format(str(i + 1)))
        result.append("Window id: {}, Virtual Environment id: {}, Port: {}, Token: {}".format(str(i + 1), venv, port, token))
        t.refresh()

    return result
    

def stop(sessions, num):
    """
    @:param sessions: Name of tmux-session, where are working environment
    @:param num: number of environment which could be killed
    """

    sessions.kill_window(str(num))

    #Additional: remove path with environemnt with number = num 
    shutil.rmtree(PATH + "/" + VENV + str(num), ignore_errors=True)


def stop_all():
    """
    Stop all working environment
    """

    server = libtmux.Server()
    server.find_where({"session_name" : SESSION_NAME}).kill_session()
    
    #Additional: remove path with all environemnt
    shutil.rmtree(PATH, ignore_errors=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Linux & Tmux exercise 1")
    parser.add_argument('command',help="start - start environment, stop - stop environment, stop_all - stop all environment")
    parser.add_argument('N', nargs='?', type=int, help="quantity of environment")

    args = parser.parse_args()
    N = args.N
    command = args.command

    if not os.path.exists(PATH):
        os.mkdir(path=PATH)

    server = libtmux.Server()
    sessions = None

    if not server.has_session(SESSION_NAME):
        sessions = server.new_session(SESSION_NAME, attach=False)
    else:
        sessions = server.find_where({"session_name" : SESSION_NAME})

    if command == 'start':       
        l = start(sessions=sessions, num_users=N)

        for i in l:
            print(i)

    if command == 'stop':
        stop(sessions=sessions, num=N)

    if command == 'stop_all':
        stop_all()