
# -------------------------------------------------------------------

# matagenerator 
# WGan 2022
# Open source
# freeware

# Data objects C++ class generator. Generated classes are serializable 
# and have all necessary comparision and can be constructed from string
# text format as well as could be dumped in human readable form
# Generated data objects could be used as normal, but highly specialized 
# types providing full usage type controll of C++ compiler.

from .meth import code_generator
from .tools import general_name, file_name
from inspect import currentframe, getmodule

class data_types_generator:

    def __init__(self, solution_root_folder, target_folder):
        self.generated_files = []
        self.solution_root_folder = file_name(solution_root_folder).get_full_file_name()
        self.target_folder = file_name(target_folder)
        self.meth_directory = file_name(__file__ + "/..");
        self.template_folder = file_name(self.meth_directory.get_full_file_name() + "/templates/data_types")
        self.generator = code_generator( {} )
        self.generator.define("meth_directory",self.meth_directory.get_name_and_path_relative_to(self.solution_root_folder))
        self.cpp_headers_folder = file_name(self.meth_directory.get_full_file_name() + "/cpp_headers")
        self.generator.define("meth_headers_directory",self.cpp_headers_folder.get_name_and_path_relative_to(self.target_folder.get_full_file_name()))

    def create_integer_type(self, namespace, name, *, base_type="int", default_value=0, min_value=None, max_value=None, compareable=False, ordered=False):
        self._set_name(namespace, name)
        self._set_base_type(base_type, default_value)
        self._set_range(min_value, max_value)
        self._set_comparision(compareable, ordered)
        self._set_template("integer_type.h.template")
        self._set_trace()
        created_file_location = self._generate()
        self.generated_files.append(created_file_location)

    def _set_name(self, namespace, name):
        self.namespace = general_name(namespace)
        self.generator.define("namespace",self.namespace.CamelCase())

        self.type_name = general_name(name)
        self.generator.define("class_name",self.type_name.CamelCase())
        self.generator.define("field_name",self.type_name.lowercase())

        self.output_file_name = file_name(self.target_folder.get_full_file_name() + "/" + self.namespace.lowercase() + "_" + self.type_name.lowercase() + ".h")
        self.generator.define("file_name", self.output_file_name.get_name_and_path_relative_to(self.solution_root_folder))

    def _set_base_type(self, base_type, default_value):
        self.base_type = base_type
        self.generator.define("base_type", base_type)
        self.default_value = default_value
        self.generator.define("default_value", str(default_value))

    def _set_range(self, min_value, max_value):
        if not min_value is None and not max_value is None:
            self.generator.define("min_value", str(min_value))
            self.generator.define("max_value", str(max_value))
            self.generator.define("range_controll", True)
        else:
            self.generator.define("min_value", 0)
            self.generator.define("max_value", 0)
            self.generator.define("range_controll", False)

    def _set_comparision(self, compareable, ordered):
        if ordered:
            self.generator.define("compareable", True)
            self.generator.define("ordered", ordered)
            self.generator.define("compareable_flag_text", "true")
            self.generator.define("ordered_flag_text", "true")
        elif compareable:
            self.generator.define("compareable", compareable)
            self.generator.define("ordered", False)
            self.generator.define("compareable_flag_text", "true")
            self.generator.define("ordered_flag_text", "false")
        else:
            self.generator.define("compareable", False)
            self.generator.define("ordered", False)
            self.generator.define("compareable_flag_text", "false")
            self.generator.define("ordered_flag_text", "false")

    def _set_template(self, template_name):
        self.template_name = file_name(self.template_folder.get_full_file_name() + "/" + template_name)
        self.generator.define("template_location", self.template_name.get_name_and_path_relative_to(self.solution_root_folder))

    def _set_trace(self):
        frame = currentframe().f_back.f_back
        generator_code_line = frame.f_lineno
        generator_code_file = file_name(getmodule(frame).__file__)
        self_generator_location = generator_code_file.get_name_and_path_relative_to(self.solution_root_folder) + " [" + str(generator_code_line) + "]"
        self.generator.define("generator_location", self_generator_location)

    def _generate(self):
        self.generator.set_template(self.template_name.get_full_file_name())
        self.generator.generate(self.output_file_name.get_full_file_name())
        return self.output_file_name.get_full_file_name()
    
# -------------------------------------------------------------------
