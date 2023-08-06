# -*- coding: utf-8 -*-
""" All about zipping files



"""
from fileinput import filename
from lib2to3.pgen2.token import OP
import os, glob, sys, math, string, time, json, logging, functools, random, yaml, operator, gc
import shutil, tarfile, zipfile
from typing import Optional, Union
import wget, yaml


from utilmy import to_file


#################################################################
from utilmy.utilmy_base import log, log2

def help():
    """function help
    """
    from utilmy import help_create
    ss = help_create(__file__)
    print(ss)


#####################################################################
def test_all():
    """ python  utilmy/util_zip.py test_all
    """
    test1()
    test2()


def test1():
    """function test1.
    Doc::

            Args:
            Returns:

    """

    import utilmy as uu
    drepo, dirtmp = uu.dir_testinfo()


    log("####### dataset_download_test() ..")
    test_file_path = dataset_donwload("https://github.com/arita37/mnist_png/raw/master/mnist_png.tar.gz", './testdata/tmp/test/dataset/')
    f = os.path.exists(os.path.abspath(test_file_path))
    assert f == True, "The file made by dataset_download_test doesn't exist"

    # dataset_donwload("https://github.com/arita37/mnist_png/raw/master/mnist_png.tar.gz", './testdata/tmp/test/dataset/')




    log("####### os_extract_archive() ..")
    #Testing os_extract_archive() extracting a zip file
    path1    = dirtmp + "/dirout/"
    path_zip = path1 + "test.zip"

    uu.to_file("Dummy test", path1 + "/zip_test.txt")

    ### https://docs.python.org/3/library/zipfile.html
    ### https://stackoverflow.com/questions/16091904/how-to-eliminate-absolute-path-in-zip-archive-if-absolute-paths-for-files-are-pr
    zf       = zipfile.ZipFile(path_zip, "w")
    zf.write(path1 + "/zip_test.txt", "zip_test.txt")
    zf.close()

    is_extracted  = os_extract_archive(
        file_path = path_zip,
        path      = drepo + "testdata/tmp/zip_test"
        #,archive_format = "auto"
        )
    assert is_extracted == True, "The zip wasn't extracted"

    # os_extract_archive("./testdata/tmp/test/dataset/mnist_png.tar.gz","./testdata/tmp/test/dataset/archive/", archive_format = "auto")


def test2():
    """function test2.
    Doc::

            Args:
            Returns:

    """

    import utilmy as uu
    import filecmp
    from os.path import exists

    _, dirtmp = uu.dir_testinfo()

    log("####### zip() ..")

    file_name = "zip_test.txt"
    path_zip = dirtmp + "test_zip"

    uu.to_file("zip() function test", dirtmp + file_name)

    zip(dirin=file_name, dirout=path_zip, root_dir=dirtmp)

    assert exists(path_zip + '.zip'), "FAILED -> zip(); Zip file haven't been created"

    log("####### gzip() ..")

    file_name = "gzip_test.txt"
    path_zip = "test_gzip.tar"

    uu.to_file("gzip() function test", dirtmp + file_name)

    gzip(dirin=file_name, dirout=path_zip, root_dir=dirtmp)

    assert exists(path_zip), "FAILED -> gzip(); Tar file haven't been created"

    log("####### unzip() ..")

    file_name = "unzip_test.txt"

    file_path = dirtmp + file_name
    unzipped_file_path = dirtmp + "unzipped/"

    path_zip = dirtmp + "test_unzip.zip"

    uu.to_file("unzip() function test", file_path)

    zf       = zipfile.ZipFile(path_zip, "w")
    zf.write(file_path, file_name)
    zf.close()

    unzip(path_zip, unzipped_file_path)

    assert filecmp.cmp(file_path, unzipped_file_path + file_name), "FAILED -> unzip(); Unzipped file is not equal to initial"





##########################################################################################
def unzip(dirin, dirout):
    """function unzip.

    Unzip a zip file.
    
    Docs::
            
        Args:
            dirin (string): Zip file to unzip.
            dirout (string): Directory to save the content of the zip file.
        
        Returns: None.

        Example:
            from utilmy import util_zip

            dirin = "/tmp/dataset.zip"

            dirout = "/tmp/dataset"


            util_zip.unzip(
                dirin = dirin,
                dirout = dirout
            )   
                
    """
    import zipfile
    with zipfile.ZipFile(dirin, 'r') as zip_ref:
        zip_ref.extractall(dirout)


def zip(dirin:str="mypath", dirout:str="myfile.zip", root_dir:Optional[str]='/', format='zip'):
    """ zip a full dirin folder into dirout file starting from the root directory.

    Docs::
            
        https://stackoverflow.com/questions/1855095/how-to-create-a-zip-archive-of-a-directory
        
        Args:
            dirin (string) : Directory to zip.
                Default to "mypath"
            dirout (string): Path to save the zipped file.
                Default to "myfile.zip".
            root_dir (string): The root dir of the system.
                Default to "/".
            format (string): Format of the zipped file. It can be "zip", "tar", "gztar", or any other registered format.
        
        Returns: None.

        Example:
            from utilmy import util_zip

            dirin = "/tmp/dataset"

            dirout = "/tmp/result"

            util_zip.zip(
                dirin = dirin,
                dirout = dirout
            )   
    """
    import shutil
    shutil.make_archive(base_name=dirout, format=format, root_dir=root_dir, base_dir=dirin)



def gzip(dirin='/mydir', dirout="./", root_dir:Optional[str]='/'):
    """function gzip.
    
    Compress a file to a gz file.
    
    Docs::
        
        Args:
            dirin (string): Directory to compress to a gz file.
                Default to "/mydir".   
            dirout (string): Path to save the gz file. It must end in ".gz".
                Default to "./".
            root_dir (string): The root dir of the system.
                Default to "/".  

        Returns: None.
        
        Example:

            from utilmy import util_zip

            dirin = "/tmp/dataset"

            dirout = "/tmp/data.gz"

            util_zip.gzip(
                dirin = dirin,
                dirout = dirout
            )   
    """
    os.chdir(root_dir)
    os.system(f'tar -cvzf {dirout} {dirin}')


def dir_size(dirin="mypath", dirout="./save.txt"):
    """function dir_size.

    Get the size of a directory and its content.

    Docs::
            
            Args:
                dirin (string) : Directory path to get its size.   
                    Default to "mypath".
                dirout (string) : Text file path to save the size of the directory.
                    Default to "./save.txt".

            Returns: None.

            Example:

                from utilmy import util_zip

                path = "/tmp/dataset/mnist_png.tar.gz"

                util_zip.dir_size(path,dirout = "/tmp/dataset/size.txt")
                                
    """
    os.system( f" du -h --max-depth  13   '{dirin}'  | sort -hr  > '{dirout}'  ")

    
def dataset_donwload(url, path_target):
    """Donwload on disk the tar.gz file.
    
    Docs::
            
            Args:
                url (string) : URL of the tar.gz file to download.
                path_target (string) : Directory path to save the file.
            
            Returns:
                Path of the saved file.
            
            Example:
            from utilmy import util_zip

            path_target = "/tmp/dataset"

            url = "https://github.com/arita37/mnist_png/raw/master/mnist_png.tar.gz"

            path = util_zip.dataset_donwload(
                url=url, 
                path_target=path_target
            )

            print(path)#Displays the path of the saved file
        
    """
    log(f"Donwloading mnist dataset in {path_target}")
    os.makedirs(path_target, exist_ok=True)
    wget.download(url, path_target)
    tar_name = url.split("/")[-1]
    os_extract_archive(path_target + "/" + tar_name, path_target)
    log2(path_target)
    return path_target + tar_name


def dataset_get_path(cfg: dict):
    """function dataset_get_path.
    Doc::
            
            Args:
                cfg (  dict ) :   
            Returns:
                
    """
    #### Donaload dataset
    # cfg = config_load()
    name = cfg.get("current_dataset", "mnist")
    cfgd = cfg["datasets"].get(name, {})
    url = cfgd.get("url", None)
    path = cfgd.get("path", None)
    path_default = os.path.expanduser("~").replace("\\", "/") + f"/.mygenerator/dataset/{name}/"

    if path is None or path == "default":
        path_target = path_default
    else:
        path_target = path

    #### Customize by Dataset   #################################
    if name == "mnist":
        ### TODO hardcoded per dataset source
        path_data = path_target + "/mnist_png/training/"
        fcheck = glob.glob(path_data + "/*/*")
        log2("n_file: ", len(fcheck))
        if len(fcheck) < 1:
            dataset_donwload(url, path_target)

        return path_data

    else:
        raise Exception("No dataset available")


def os_extract_archive(file_path, path=".", archive_format="auto"):
    """Extracts an archive if it matches tar, tar.gz, tar.bz, or zip formats..
    Doc::
            
            Args:
                file_path: path to the archive file
                path: path to extract the archive file
                archive_format: Archive format to try for extracting the file.
                    Options are 'auto', 'tar', 'zip', and None.
                    'tar' includes tar, tar.gz, and tar.bz files.
                    The default 'auto' is ['tar', 'zip'].
                    None or an empty list will return no matches found.
            Returns:
                True if a match was found and an archive extraction was completed,
                False otherwise.
            
            Example:
                from importlib.resources import path
                from utilmy import util_zip

                file_path = "/tmp/mnist_png.tar.gz"
                dir_path = "/tmp/mnist_png"

                is_extracted = util_zip.os_extract_archive(
                    file_path=file_path,
                    path=path
                )

                print(is_extracted)
    """
    if archive_format is None:
        return False
    if archive_format == "auto":
        archive_format = ["tar", "zip"]
    if isinstance(archive_format, str):
        archive_format = [archive_format]

    file_path = os.path.abspath(file_path)
    path = os.path.abspath(path)

    for archive_type in archive_format:
        if archive_type == "tar":
            open_fn = tarfile.open
            is_match_fn = tarfile.is_tarfile
        if archive_type == "zip":
            open_fn = zipfile.ZipFile
            is_match_fn = zipfile.is_zipfile

        if is_match_fn(file_path):
            with open_fn(file_path) as archive:
                try:
                    archive.extractall(path)
                except (tarfile.TarError, RuntimeError, KeyboardInterrupt):
                    if os.path.exists(path):
                        if os.path.isfile(path):
                            os.remove(path)
                        else:
                            shutil.rmtree(path)
                    raise
            return True
    return False


        
        
        

###################################################################################################
if __name__ == "__main__":
    import fire
    fire.Fire()


