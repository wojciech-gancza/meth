#--------------------------------------------------------------------------

import os

#--------------------------------------------------------------------------

class Environment:

    def __init__(self):
        self.script_path = AbsolutePath(__file__).parent()
        self.patterns_path = self.script_path.create_changed_by("patterns")

#--------------------------------------------------------------------------

class AbsolutePath:

    def __init__(self, path):
        full_path = os.path.abspath(str(path))
        self.full_path = full_path.replace("\\", "/")

    def parent(self):
        path = os.path.dirname(self.full_path)
        return AbsolutePath(path)

    def create_changed_by(self, local_path):
        return AbsolutePath( self.full_path + "/" + local_path )

    def get_relative_to(self, absolute_path):
        absolute_path = AbsolutePath(absolute_path)
        return os.path.relpath(self.full_path, absolute_path.full_path).replace("\\", "/")

    def __str__(self):
        return self.full_path

    def get_as_directory(self):
        return self.full_path + "/"

#--------------------------------------------------------------------------

class Name:

    def __init__(self, name_as_space_separated_text):
        name_blocks = name_as_space_separated_text.split(":")
        namespaces = name_blocks[:-1]
        undecorated_name = name_blocks[-1]
        self.namespace = [ self._convert_to_word_list(namespace) for namespace in namespaces]
        self.undecorated_name = self._convert_to_word_list(undecorated_name)

    def lowercaseCamelName(self): # objects, variables
        return self.undecorated_name[0] + self._convert_to_camelcase_text(self.undecorated_name[1:])

    def UppercaseCamelName(self): # classes
        return self._convert_to_camelcase_text(self.undecorated_name)

    def lowercase_name(self): # objects, fields, parameters, variables
        return self._convert_to_lowercase_text(self.undecorated_name)

    def UPPERCASE_NAME(self): # defines, macrodefinitions, constants
        return self.lowercase_name().upper()

    def UppercaseCamelsNamespaces(self): # list of namespaces
        return [self._convert_to_camelcase_text(element) for element in self.namespace]

    def lowercase_namespace_and_name(self, default_namespace = None): # file names
        if self.namespace:
            elements = [self._convert_to_lowercase_text(namespace) for namespace in self.namespace]
            elements.append(self.lowercase_name())
            return self._convert_to_lowercase_text(elements)
        elif default_namespace:
            namspace = Name(default_namespace)
            elements = [namspace.lowercase_namespace_and_name(), self.lowercase_name()]
            return self._convert_to_lowercase_text(elements)
        else:
            return self.lowercase_name()

    def _convert_to_word_list(self, name):
        return [word.strip() for word in name.split(" ") if word.strip() ]

    def _convert_to_lowercase_text(self, array_of_words):
        return "_".join( [word.lower() for word in array_of_words] )

    def _convert_to_camelcase_text(self, array_of_words):
        return "".join( [word.capitalize() for word in array_of_words] )

#--------------------------------------------------------------------------

