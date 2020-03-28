from os import mkdir
from shutil import rmtree
from os.path import join as pjoin
from os.path import exists
def create_folders(sess_id):
    temp_path = pjoin("temp",sess_id)
    input_path = pjoin(temp_path,"input")
    output_path = pjoin(temp_path,"output")
    if not exists("temp"):
        mkdir("temp")
    mkdir(temp_path)
    mkdir(input_path)
    mkdir(output_path)


def delete_folders(sess_id):

    temp_path = pjoin("temp",sess_id),

    rmtree(temp_path)