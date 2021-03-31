##### File Contents #####
    # 1. Required Packages
    # 2. Classes

##### 1. Required Packages #####
import os, re, inspect

##### 2. Classes #####

    # Class Layout:
        # 1. Class Variables
        # 2. Special Methods
        # 3. Getters and Setters
        # 4. Attribute Methods: Methods extending the functionality of getters and setters
        # 5. Utility Methods: Methods for use in Primary Methods
        # 6. Primary Methods: Methods expected to be used by the end user

    # Argument Key
        # Name as a string = 'name' OR 'target_name'
        # Text as a string = 'text'
        # Object = 'class_name_obj'
        # Dictionary = 'expected_content_dict'
        # List = 'expected_element_type_list'
        # Tuple = 'target_variable_tup'
        # String = 'target_variable_str'
        # Integer = 'target_variable_int'
        # Boolean = 'target_variable_bool'
        # Argument Value = 'argument_name_value'
        # Other = 'targetvariable_expectation'

    # Classes:
        # 1. BaseClass: Explanation of BaseClass

class BaseClass:
    ##### Class Variables #####

    class_name = 'BaseClass'

    ##### Special Methods #####

    def __init__(self, profile='default', name=None):
        self.attributes = ["profile", "name"]
        self.path = os.path.abspath(__file__)
        self.root = os.path.dirname(self.path)
        self.config = os.path.join(self.root, 'config.py')
        self.profile = profile
        self.name = name

    def __str__(self):
        return 'BaseClass'

    def __repr__(self):
        return f"< BaseClass | Name: {self.name} >"

    ##### Getters and Setters #####

    def set_profile(self, profile_name):
        self.profile = profile_name

    def get_profile(self):
        return self.profile

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    ##### Attribute Methods #####

    # Return the attributes of this object as a dictionary
    def to_dict(self):
        # The keys of the following dictionary are the names of this object's properties
        # The values of the following dictionary are the values of this object's properties
        attribute_dict = {
            "attributes" : self.attributes,
            "path" : self.path,
            "root" : self.root,
            "config" : self.config,
            "profile" : self.profile,
            "name" : self.name
        }

        return attribute_dict

    # Set the value of a single attribute of this object
    def set_attribute(self, attribute_name, attribute_value):
        # The list in the following loop contains the names of all attributes of this object
        for attribute in self.attributes:
            if attribute == attribute_name:
                setattr(self, attribute, attribute_value)
                break

    # Set the value of one or more attributes of this object
    def set_attributes(self, attribute_dict):
        for attribute in self.attributes:
            if attribute in attribute_dict:
                setattr(self, attribute, attribute_dict[attribute])

    # Set the value of an attribute to 'None'
    # If the 'attribute_name' argument is 'all', do it for all attributes
    def clear_attribute(self, attribute_name):
        if attribute_name == "all":
            for attribute in self.attributes:
                setattr(self, attribute, None)
        else:
            self.set_attribute(attribute_name, None)

    ##### Utility Methods #####

        # Error Handling #

    # Print a message with information about an error
    # If the 'get_return' argument is 'True', return the error message
    def error_message(self, error_dict=None, get_return=False):
        message_components = []

        start = "Error Encountered"
        message_components.append(start)

        object_info = f"{self.__repr__()} : {self.path}"
        message_components.append(object_info)

        if error_dict is not None:
            for key, value in error_dict.items():
                new_component = f"{key} : {value}"
                message_components.append(new_component)
        
        error_message = " | ".join(message_components)
        print(error_message)

        if get_return == True:
            return error_message

    # Return a dictionary of frame data
    def get_frame_data(self):
        return inspect.stack()

        # Configuration #

    # Return a string to be used as lines for a configuration file variable
    def as_config_variable(self, variable_name, target_variable):
        return f"{variable_name} = {target_variable.__repr__}"

    # Return a list of lines representing a section of a configuration file
    def create_config_section(self, section_name, section_dict=None):
        section_start = f"# Start {section_name} #"
        section_declaration = f"{section_name} = "
        variable_open = "{"
        variable_declaration = section_declaration + variable_open
        variable_close = "}"
        section_end = f"# End: {section_name} #"

        section_lines = []
        section_lines.append(section_start)

        if section_dict is not None:
            section_lines.append(variable_declaration)
            for key, value in section_dict:
                opening_whitespace = "\t"
                section_variable_content = self.as_config_variable(key.__repr__(), value)
                line_terminal = ","
                section_line_format = [opening_whitespace, section_variable_content, line_terminal]
                section_line = "".join(section_line_format)
                section_lines.append(section_line)
            section_lines.append(variable_close)

        section_lines.append(section_end)

        return section_lines

    ##### Primary Methods #####
    
        # Configuration #

    # Create a new 'config.py' file
    def update_config_file(self):
        try:
            # Create the lines to write to the config file
            profile_dict = {}

            current_profile = self.to_dict()
            empty_profile = {}
            default_profile = {}
            for key, value in current_profile.items():
                empty_profile[key] = None
                default_profile[key] = value

            # If there are any default values to set, do it here
            # default_profile[attribute] = attribute_value

            profile_dict["current"] = current_profile
            profile_dict["empty"] = empty_profile
            profile_dict["default"] = default_profile

            profile_section = self.create_config_section("profiles", profile_dict)

            # Write the lines to the config file
            config_file = open(self.config, "a")
            config_file.write(f"##### {self.class_name} config #####")
            config_file.write("\n")
            for line in profile_section:
                config_file.write(line)
                config_file.write("\n")
            config_file.close()

        except:
            self.error_message()
        
    # Set attributes from data in the 'config.py' file
    def load_profile(self, profile_name):
        # Search for the config file
        # It not found, create one
        if not os.path.exists(self.config):
            self.update_config_file()
        # Try to import the config variable and match keys with attributes
        try:
            profile_import = f".config.profiles.{profile_name}"
            selected_profile = __import__(profile_import)
            self.set_profile(profile_name)
            self.set_attributes(selected_profile)
        except:
            self.error_message()

    def save_profile(self, profile_name):
        pass


    def default_attribute(self, attribute_name, replace=False, return_value=True):
        # Try to import the 'default' config from 'config.py'
        try:
            default_config = __import__("config.default")
            # Try to set the object attribute from the 'default_config' data
        except:
            self.error_message()
        if replace == True:
            self.set_attribute(attribute_name, default_config[attribute_name])
        if return_value == True:
            return default_config[attribute_name]
