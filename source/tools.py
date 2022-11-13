# -------------------------------------------------------------------

# matagenerator 
# WGan 2022
# Open source
# freeware

# tools classes and objects
# some nice to use tools which could be usefull when generating the code

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
        
# ----------------------------------------------------------

