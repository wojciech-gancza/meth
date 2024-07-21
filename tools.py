# -------------------------------------------------------------------

# matagenerator 
# WGan 2022
# Open source
# freeware

import os

# tools classes and objects
# some nice to use tools which could be usefull when generating the code

from .meth import code_block

# class transforming string to identifier with variours notations
class general_name:

    def __init__(self, name):
        self.bare_name = name.split()
        
    def CamelCase(self):
        return "".join([x.capitalize() for x in self.bare_name])
        
    def lowercaseCamel(self):
        if len(self.bare_name):
            first = self.bare_name[0].lower()
            return first + "".join([x.capitalize() for x in self.bare_name[1:]])
        else:
            return ""
        
    def lowercase(self):
        return "_".join([x.lower() for x in self.bare_name])
        
    def UPPERCASE(self):
        return "_".join([x.upper() for x in self.bare_name])
 
class file_name:
    
    def __init__(self, file_with_path):
        file_with_path = self._change_directory_separators(file_with_path)
        if not self._is_full_path(file_with_path):
            file_with_path = self._get_cwd() + "/" + file_with_path;
        result_path = []
        path_elements = file_with_path.split("/")
        while path_elements:
            if path_elements[0] == "" or path_elements[0] == ".":
                pass
            elif path_elements[0] == "..":
                result_path = result_path[:-1]
            else:
                result_path.append(path_elements[0])
            path_elements = path_elements[1:]
        self.full_file_name = "/".join(result_path)
        if (file_with_path[0] == "/" and self.full_file_name[0] != "/"):
            self.full_file_name = "/" + self.full_file_name
    
    def get_name_and_path_relative_to(self, base_path):
        if base_path[-1] == "/":
            base_path = base_path[:-1]
        file = self.full_file_name.split("/")
        path = base_path.split("/")
        while file and path and file[0] == path[0]:
            file = file[1:]
            path = path[1:]
        file_name = "/".join(file)
        if path:
            file_name = ("../" * len(path)) + file_name
        else:
            file_name = "./" + file_name
        return file_name
        
    def get_full_file_name(self):
        return self.full_file_name
        
    def _get_cwd(self):
        cwd = self._change_directory_separators(os.getcwd()) + "/"
        return cwd
        
    def _change_directory_separators(self, path):
        return path.replace("\\", "/")
        
    def _is_full_path(self, path):
        if len(path) == 0:
            return False
        if path[0] == "/":
            return True
        if len(path) > 3 and path[1:3] == ":/":
            return True
        return False
        
# ----------------------------------------------------------

