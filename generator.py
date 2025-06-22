#--------------------------------------------------------------------------

import meth
import math
import generatortools
import inspect

#--------------------------------------------------------------------------

class PlainOldDataTypes:

    def __init__(self, soluton_path, tools_target_path = None):
        if not tools_target_path:
            tools_target_path = soluton_path
        self.environment = generatortools.Environment()
        self.soluton_path = generatortools.AbsolutePath(soluton_path)
        self.output_path = soluton_path
        self.tools_output_path = generatortools.AbsolutePath(tools_target_path)
        self.generator = meth.Metamorph(self.environment.patterns_path.get_as_directory())

    def set_output_path(self, output_path):
        self.output_path = generatortools.AbsolutePath(output_path)

    def generate_integer(self, properties):
        # required properties:
        # - name - fully qualified type name defined as single string where words are name elements ( example: "common : severity"),
        # - int_class - name of type used to store the value internally (example: "uint16_t")
        # optional properties:
        # - compareable - adds "==", "=!" , ... operators. When not defined True is assumed
        # - ordered - adds "<", ">" , ... operators. When set to true also sets compareable. When not defined False is assumed
        # - default - default value. When not defined - 0 is assumed
        extended_properties = self._extend_property_list(properties)
        self._set_int_class_size(extended_properties)
        self._set_default_value(extended_properties, "default", 0)
        extended_properties["h_std_includes"].append( "cstdint" )
        extended_properties["cpp_std_includes"].append( "sstream" )
        extended_properties["simple_base_type"] = extended_properties["int_class"]
        self._generate_files("integer.h.body.pattern", "integer.cpp.body.pattern", extended_properties)

    def generate_string(self, properties):
        # required properties:
        # - name - fully qualified type name defined as single string where words are name elements ( example: "common : severity"),
        # - max_size - maximum size of string. Used to deduct size type used also in serialization
        # optional properties:
        # - compareable - adds "==", "=!" , ... operators. When not defined True is assumed
        # - ordered - adds "<", ">" , ... operators. When set to true also sets compareable. When not defined False is assumed
        # - default - default value. When not defined - empty string us used as default
        # - compare_type - how the strings are compared. Default is "strcmp"
        extended_properties = self._extend_property_list(properties)
        self._set_int_type_by_count_of_values(extended_properties, extended_properties["max_size"])
        self._set_default_value(extended_properties, "default", "")
        self._set_default_value(extended_properties, "compare_class", "common : strcmp compare")
        extended_properties["compare_class"] = generatortools.Name(extended_properties["compare_class"])
        extended_properties["h_includes"] = [ self.tools_output_path.create_changed_by(extended_properties["compare_class"].lowercase_namespace_and_name() + ".h"), \
                                              self.tools_output_path.create_changed_by("common_conversion_error.h") ]
        extended_properties["h_std_includes"].append( "cstdint" )
        extended_properties["cpp_std_includes"].append( "sstream" )
        extended_properties["simple_base_type"] = "const std::string&"
        extended_properties["default"] = "\"" + extended_properties["default"].replace("\\", "\\\\").replace("\"", "\\\"") + "\""
        self._generate_files("string.h.body.pattern", "string.cpp.body.pattern", extended_properties)

    def generate_floating_point(self, properties):
        # required properties:
        # - name - fully qualified type name defined as single string where words are name elements ( example: "common : severity"),
        # - float_class - name of type used to store the value internally (example: "uint16_t")
        # optional properties:
        # - compareable - adds "==", "=!" , ... operators. When not defined True is assumed
        # - ordered - adds "<", ">" , ... operators. When set to true also sets compareable. When not defined False is assumed
        # - default - default value. When not defined - 0.0
        # - accuracy - value used to compare - when difference is less the accuracy assume equal. Default = 0.0001
        # - format - format of string the value is converted to
        extended_properties = self._extend_property_list(properties)
        self._set_default_value(extended_properties, "default", "0.0")
        self._set_default_value(extended_properties, "accuracy", "0.0001")
        self._set_default_value(extended_properties, "format", ".4f")
        extended_properties["h_std_includes"] = ["format"]
        extended_properties["cpp_std_includes"] = ["sstream"]
        extended_properties["simple_base_type"] = extended_properties["float_class"]
        self._generate_files("float.h.body.pattern", "float.cpp.body.pattern", extended_properties)

    def generate_enum(self, properties):
        # required properties:
        # - name - fully qualified type name defined as single string where words are name elements ( example: "common : severity"),
        # - values - list of values (example: [ "data", "memo", "notice", "info", "trace", "debug"])
        # optional properties:
        # - default - default value. When not defined - first value is default
        # - compareable - adds "==", "=!" , ... operators. When not defined True is assumed
        # - ordered - adds "<", ">" , ... operators. When set to true also sets compareable. When not defined False is assumed
        extended_properties = self._extend_property_list(properties)
        self._set_int_type_by_count_of_values(extended_properties, len(extended_properties["values"]))
        extended_properties["first_value"] = "E_" + extended_properties["values"][0].UPPERCASE_NAME()
        extended_properties["last_value"] = "E_" + extended_properties["values"][-1].UPPERCASE_NAME()
        extended_properties["simple_base_type"] = "e" + extended_properties["class_name"]
        extended_properties["code_converting_from_string"] = generatortools.EnumCodeGenerator(extended_properties["values"]).generate_code()
        self._set_default_value(extended_properties, "default", properties["values"][0])
        extended_properties["default"] = "E_" + generatortools.Name(extended_properties["default"]).UPPERCASE_NAME()
        extended_properties["h_std_includes"].append( "cstdint" )
        extended_properties["cpp_std_includes"].append( "sstream" )
        self._generate_files("enum.h.body.pattern", "enum.cpp.body.pattern", extended_properties)

    def generate_bitflags(self, properties):
        # required properties:
        # - name - fully qualified type name defined as single string where words are name elements ( example: "common : severity"),
        # - values - list of values (example: ["audio input l", "audio input r", "radio transmit", "driver handphone" ])
        # optional properties:
        # - compareable - adds "==", "=!" , ... operators. When not defined True is assumed
        # remarks: In this version the default is always no bit set. Bitsets cannot be ordered
        extended_properties = self._extend_property_list(properties)
        extended_properties["ordered"] = False
        self._set_int_type_by_count_of_bits(extended_properties, len(extended_properties["values"]))
        hex_format = "0x{:0" + str(math.ceil(len(properties["values"]) / 4)) + "x}"
        extended_properties["first_value"] = hex_format.format(1)
        extended_properties["last_value"] = hex_format.format(pow(2, len(extended_properties["values"]) - 1))
        extended_properties["code_converting_from_string"] = generatortools.EnumCodeGenerator(extended_properties["values"]).generate_code()
        extended_properties["default"] = "0"
        extended_properties["simple_base_type"] = "e" + extended_properties["class_name"]
        extended_properties["h_std_includes"] = ["cstdint"]
        extended_properties["cpp_std_includes"].append( "sstream" )
        self._generate_files("bitflags.h.body.pattern", "bitflags.cpp.body.pattern", extended_properties)

    def generate_timepoint(self, properties):
        # required properties:
        # - name - fully qualified type name defined as single string where words are name elements ( example: "common : severity"),
        # - text_output_format - format used to convert to string and from string
        # optional properties:
        # - compareable - adds "==", "=!" , ... operators. When not defined True is assumed
        # - ordered - adds "<", ">" , ... operators. When set to true also sets compareable. When not defined False is assumed
        extended_properties = self._extend_property_list(properties)
        extended_properties["h_std_includes"] =  [ "chrono" ]
        extended_properties["cpp_includes"] =  [ self.tools_output_path.create_changed_by("common_text_converter.h") ]
        time_format_code_generator = generatortools.TimeFormatCodeGenerator(extended_properties["text_output_format"], extended_properties)
        extended_properties["decompose_string_code"] = time_format_code_generator.generate_decompose_string_code()
        extended_properties["compose_output_code"] = time_format_code_generator.generate_compose_output_code()
        extended_properties["default"] = "ClockType::now()"
        extended_properties["simple_base_type"] = "TimePointType"
        self._generate_files("time.point.h.body.pattern", "time.point.cpp.body.pattern", extended_properties)

    def generate_time_duration(self, properties):
        # required properties:
        # - name - fully qualified type name defined as single string where words are name elements ( example: "common : severity"),
        # - text_output_format - format used to convert to string and from string
        # optional properties:
        # - compareable - adds "==", "=!" , ... operators. When not defined True is assumed
        # - ordered - adds "<", ">" , ... operators. When set to true also sets compareable. When not defined False is assumed
        # - default - default value
        extended_properties = self._extend_property_list(properties)
        extended_properties["h_std_includes"] =  [ "chrono" ]
        extended_properties["cpp_includes"] =  [ self.tools_output_path.create_changed_by("common_text_converter.h") ]
        duration_code = generatortools.TimeDurationCodeGenerator(extended_properties["text_output_format"])
        extended_properties["decomposition_code"] = duration_code.get_decomposition_code()
        extended_properties["serialization_code"] = duration_code.get_serializatrion_code()
        extended_properties["deserialization_code"] = duration_code.get_deserializatrion_code()
        extended_properties["simple_base_type"] = "TimeDurationType"
        self._generate_files("time.duration.h.body.pattern", "time.duration.cpp.body.pattern", extended_properties)

    def generate_record(self, properties):
        # required properties:
        # - name - fully qualified type name defined as single string where words are name elements ( example: "common : severity"),
        # - values - list of types of record elements ["common : severity", "acoustic : selected output ids", "common : network : port number"]
        # optional properties:
        # - compareable - adds "==", "=!" , ... operators. When not defined True is assumed
        # - ordered - adds "<", ">" , ... operators. When set to true also sets compareable. When not defined False is assumed
        extended_properties = self._extend_property_list(properties)
        extended_properties["values"] = [ generatortools.Name(value) for value in properties["values"] ]
        extended_properties["h_includes"] = [ self.output_path.create_changed_by(name.lowercase_namespace_and_name() + ".h") for name in extended_properties["values"] ]
        extended_properties["cpp_includes"] =  [ self.tools_output_path.create_changed_by("common_record_fields_comparision.h") ]
        extended_properties["cpp_std_includes"].append( "sstream" )
        self._generate_files("record.h.body.pattern", "record.cpp.body.pattern", extended_properties)

    def generate_collection(self, properties):
        # required properties:
        # - name - fully qualified type name defined as single string where words are name elements ( example: "common : severity"),
        # - element_type - type of collection elment
        # optional properties:
        # - compareable - adds "==", "=!" , ... operators. When not defined True is assumed
        # - ordered - adds "<", ">" , ... operators. When set to true also sets compareable. When not defined False is assumed
        extended_properties = self._extend_property_list(properties)
        extended_properties["element_type"] = generatortools.Name(extended_properties["element_type"]) 
        extended_properties["h_std_includes"].append( "vector" )
        extended_properties["cpp_includes"].append( self.output_path.create_changed_by(extended_properties["element_type"].lowercase_namespace_and_name() + ".h") )
        extended_properties["cpp_std_includes"].append( "sstream" )
        extended_properties["h_forward_declare"].append( extended_properties["element_type"] )
        self._generate_files("collection.h.body.pattern", "collection.cpp.body.pattern", extended_properties)

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    def _generate_files(self, header_pattern, cpp_pattern, properties):
        properties["includes"] = properties["h_includes"] + [ self.tools_output_path.create_changed_by("serialization_binary_serialization.h") ]
        properties["std_includes"] = properties["h_std_includes"] + ["string", "iostream"]
        properties["forward_declare"] = properties["h_forward_declare"]
        properties["once"] = True
        properties["code_body_pattern"] = header_pattern
        self._generate("common.main.pattern", "header_file_name", properties)
        properties["includes"] = [ self.output_path.create_changed_by( properties["name"].lowercase_namespace_and_name() + ".h" ), \
                                   self.tools_output_path.create_changed_by("common_conversion_error.h") \
                                  ] + properties["cpp_includes"]
        properties["code_body_pattern"] = cpp_pattern
        properties["std_includes"] = properties["cpp_std_includes"]
        properties["forward_declare"] = properties["cpp_forward_declare"]
        properties["once"] = False
        self._generate("common.main.pattern", "source_file_name", properties)

    def _generate(self, pattern_file_name, output_type, properties):
        pattern_file_path = self.environment.patterns_path.create_changed_by(pattern_file_name)
        properties["pattern_file_path"] = self.environment.patterns_path.create_changed_by(properties["code_body_pattern"])
        properties["pattern_wrapper_file_path"] = pattern_file_path
        output_file_name = properties[output_type]
        properties["output_file_name"] = output_file_name
        self.generator.generate(pattern_file_name, str(output_file_name), properties)

    def _set_default_value(self, properties, name, default_value):
        if name not in properties.keys():
            properties[name] = default_value

    def _extend_property_list(self, properties):
        name = generatortools.Name(properties["name"])
        frame = inspect.currentframe().f_back.f_back
        generator_code_line = frame.f_lineno
        generator_code_file = generatortools.AbsolutePath(inspect.getmodule(frame).__file__)
        extended_properties = { **properties, 
                 "format": generatortools.ListFormatter(),
                 "name": name, 
                 "class_name": name.UppercaseCamelName(),
                 "object_name": name.lowercase_name(),
                 "header_file_name": self.output_path.create_changed_by(name.lowercase_namespace_and_name() + ".h"),
                 "source_file_name": self.output_path.create_changed_by(name.lowercase_namespace_and_name() + ".cpp"),
                 "namespaces": name.UppercaseCamelsNamespaces(),
                 "generator_path": generator_code_file,
                 "generator_line_number": generator_code_line,
                 "solution_path": self.soluton_path,
                 "cpp_includes": [],
                 "cpp_std_includes": [],
                 "h_includes": [],
                 "h_std_includes": [],
                 "h_forward_declare": [],
                 "cpp_forward_declare": []}
        if "values" in extended_properties.keys():
            extended_properties["values"] = [generatortools.Name(value) for value in extended_properties["values"] ]
        self._set_default_value(extended_properties, "compareable", True)
        self._set_default_value(extended_properties, "ordered", False)
        if extended_properties["ordered"]:
            extended_properties["compareable"] = True
        return extended_properties

    def _set_int_class_size(self, properties):
        if properties["int_class"] in ["int8_t", "uint8_t"]:
            properties["int_class_size"] = 1
        elif properties["int_class"] in ["int16_t", "uint16_t"]:
            properties["int_class_size"] = 2
        elif properties["int_class"] in ["int32_t", "uint32_t"]:
            properties["int_class_size"] = 4
        elif properties["int_class"] in ["int64_t", "uint64_t"]:
            properties["int_class_size"] = 8

    def _set_int_type_by_count_of_values(self, properties, cout_values):
        if cout_values <= 255:
            properties["int_class"] = "uint8_t"
            properties["int_class_size"] = 1
        elif cout_values <= 65535:
            properties["int_class"] = "uint16_t"
            properties["int_class_size"] = 2
        else:
            properties["int_class"] = "uint32_t"
            properties["int_class_size"] = 4

    def _set_int_type_by_count_of_bits(self, properties, count_of_bits):
        if count_of_bits <= 8:
            properties["int_class"] = "uint8_t"
            properties["int_class_size"] = 1
        elif count_of_bits <= 16:
            properties["int_class"] = "uint16_t"
            properties["int_class_size"] = 2
        elif count_of_bits <= 32:
            properties["int_class"] = "uint32_t"
            properties["int_class_size"] = 4
        elif count_of_bits <= 64:
            properties["int_class"] = "uint64_t"
            properties["int_class_size"] = 4

#--------------------------------------------------------------------------


