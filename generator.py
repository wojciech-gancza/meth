#--------------------------------------------------------------------------

import meth
import generatortools
#from inspect import currentframe, getmodule
import inspect

#--------------------------------------------------------------------------

class PlainOldDataTypes:

    def __init__(self, soluton_path):
        self.environment = generatortools.Environment()
        self.soluton_path = generatortools.AbsolutePath(soluton_path)
        self.output_path = soluton_path
        self.generator = meth.Metamorph(self.environment.patterns_path.get_as_directory())

    def set_output_path(self, output_path):
        self.output_path = generatortools.AbsolutePath(output_path)

    def generate_integer(self, properties):
        extended_properties = self._enrich_properies(properties)
        extended_properties["code_body_pattern"] = "integer.h.body.pattern"
        extended_properties["file_path"] = self.output_path.create_changed_by(extended_properties["header_file_name"]) 
        output_file_name = extended_properties["output_path"].get_as_directory() + extended_properties["header_file_name"]
        self.generator.generate("source.file.pattern",  output_file_name, extended_properties)

    def _enrich_properies(self, properties):
        name = generatortools.Name(properties["name"])
        frame = inspect.currentframe().f_back.f_back
        generator_code_line = frame.f_lineno
        generator_code_file = generatortools.AbsolutePath(inspect.getmodule(frame).__file__)
        extended_properties = { **properties, 
                 "format": generatortools.ListFormatter(),
                 "name": name, 
                 "class_name": name.UppercaseCamelName(),
                 "object_name": name.lowercase_name(),
                 "header_file_name": name.lowercase_namespace_and_name() + ".h",
                 "source_file_name": name.lowercase_namespace_and_name() + ".cpp",
                 "namespaces": name.UppercaseCamelsNamespaces(),
                 "generator_path": generator_code_file,
                 "generator_line_number": generator_code_line,
                 "solution_path": self.soluton_path,
                 "pattern_file_path": self.environment.patterns_path.create_changed_by("source.file.pattern"),
                 "pattern_directory_path": self.environment.patterns_path,
                 "output_path": self.output_path }
        return extended_properties

#--------------------------------------------------------------------------


