#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/6 9:58
# @Author  : fangjie
# @email   : 838379742@qq.com
# @File    : tools.py
__metaclass__ = type

import os
import platform
import sys
reload(sys)
sys.setdefaultencoding('utf8')


class ProfileName:
    LINUX_FILE = "/etc/profile.d/blog.sh"
    WINDOWS_FILE = "app/scripts/blog.bat"


class SetProfile:
    @staticmethod
    def _create_windows_command(path_name, path_value):
        if os.environ.get(path_name) is None:
            return "setx " + path_name + " "+ path_value + "\n"
        else:
            return "setx "+path_name+" %"+path_name+"%;"+path_value+"\n"

    @staticmethod
    def _create_linux_command(path_name, path_value):
        return "export "+path_name+"="+path_value+"\n"

    @staticmethod
    def write_file(command,filename):
        with open(filename,'a') as file:
            file.write(command)

    @staticmethod
    def profile( path_name, path_value):
        sysstr = SetProfile.get_system_name()
        if(sysstr == "Windows"):
            command = SetProfile._create_windows_command(path_name,path_value)
            filename = ProfileName.WINDOWS_FILE
        elif(sysstr == "Linux"):
            command = SetProfile._create_linux_command(path_name,path_value)
            filename = ProfileName.LINUX_FILE
        return (command, filename)

    @staticmethod
    def get_system_name():
        return platform.system()


class SetPersonalIntroduction:
    @staticmethod
    def setTel(configer,tel,telNum):
        if configer.has_section('tel') is not True:
            configer.add_section('tel')
        configer.set('tel', 'telNum', telNum)
        for telName,telValue in tel.items():
            if configer.has_option('tel',telName):
                configer.remove_option('tel',telName)
            configer.set('tel',telName,telValue)
        return configer

    @staticmethod
    def setNormal(configer,name,introduction):
        if configer.has_section('normal') is not True:
            configer.add_section('normal')

        if configer.has_option('normal',name):
            configer.remove_option('normal',name)
        configer.set('normal','name',name)

        if configer.has_option('introduction',introduction):
            configer.remove_option('introduction',introduction)
        configer.set('normal','introduction',introduction)

        return configer



    @staticmethod
    def setTech(configer,tech,techNum):
        if configer.has_section('tech') is not True:
            configer.add_section('tech')
        configer.set('tech','techNum',techNum)
        for techName,techProportion in tech.items():
            if configer.has_option('tech',techName):
                configer.remove_option('tech',techName)
            configer.set('tech',techName,techProportion)
        return configer

    @staticmethod
    def setImage(configer,image):
        if configer.has_section('image') is not True:
            configer.add_section('image')

        if configer.has_option('image','image'):
            configer.remove_option('image','image')
        configer.set('image','image',image)
        return configer

if __name__=='__main__':
    #re()
    #print os.path.abspath('a.bat')
    os.system('a.bat')

