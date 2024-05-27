#!/usr/bin/python3
"""
this module is for console to interpret
"""
import re
import cmd
import json
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State


class HBNBCommand(cmd.Cmd):
    """ this class is for console"""
    classes = ["BaseModel", "User", "Amenity",
               "City", "Place", "Review", "State"]

    def do_create(self, args):
        """Creates a new instance of BaseModel."""
        if not args:
            print("** class name missing **")
            return

        pattern = re.compile(r"(\w+)\s*([\w_]+=.*)*")
        match = pattern.match(args)

        class_name = match.group(1)
        if class_name not in self.classes:
            print("** class doesn't exist **")
            return

        try:
            obj = eval(class_name)()

            pattern2 = re.compile(r"(\w+)=(\".*?\"|-?[\d.]+|-?[\d]+)")
            matches2 = pattern2.finditer(match.group(2) or "")

            for match2 in matches2:
                key = match2.group(1)
                value = eval(match2.group(2))
                if isinstance(value, str):
                    value = value.replace("_", " ")

                if hasattr(obj, key):
                    setattr(obj, key, value)
            storage.new(obj)
            storage.save()
            print(obj.id)
        except NameError:
            print("** class doesn't exist **")

    def do_show(self, args):
        """Prints the string representation of an instance"""
        args_list = args.split()
        if not args_list:
            print("** class name missing **")
            return
        try:
            class_name = args_list[0]
            if class_name not in HBNBCommand.classes:
                print("** class doesn't exist **")
                return
            if len(args_list) < 2:
                print("** instance id missing **")
                return
            instances = storage.all()
            instance_id = args_list[1]
            key = class_name + "." + instance_id
            if key not in instances:
                print("** no instance found **")
                return
            print(instances[key])
        except Exception as e:
            print(e)

    def do_destroy(self, args):
        """ Deletes an instance based on the class name and id """
        args_list = args.split()

        if not args_list:
            print("** class name missing **")
            return
        class_name = args_list[0]
        if class_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return
        if len(args_list) < 2:
            print("** instance id missing **")
            return

        try:
            objs = storage.all()
            obj_id = args_list[1]
            key = class_name + '.' + obj_id

            if key not in objs:
                print("** no instance found **")
                return

            objs.pop(key)
            storage.save()
        except Exception as ex:
            print(ex)

    def do_all(self, args):
        """
        Prints all string representation of all
        instances based or not on the class name.
        """
        lst = []
        if not args:
            for value in storage.all().values():
                lst.append(str(value))
        elif args in HBNBCommand.classes:
            objs = storage.all()
            for value in objs.values():
                if value.to_dict()['__class__'] == args:
                    lst.append(str(value))
        else:
            print("** class doesn't exist **")
            return
        print(lst)

    def do_update(self, args):
        """ Updates an instance based on the class name and id"""
        args_list = args.split()
        if not args_list:
            print("** class name missing **")
            return
        try:
            class_name = args_list[0]
            if class_name not in HBNBCommand.classes:
                print("** class doesn't exist **")
                return
            if len(args_list) < 2:
                print("** instance id missing **")
                return
            instances = storage.all()
            instance_id = args_list[1]
            key = class_name + "." + instance_id
            if key not in instances:
                print("** no instance found **")
                return
            if len(args_list) < 3:
                print("** attribute name missing **")
                return
            if len(args_list) < 4:
                print("** value missing **")
                return
            if args_list[2] in ["id", "created_at", "updated_at"]:
                return
            attr_name = args_list[2]
            attr_value = json.loads(args_list[3])

            if isinstance(attr_value, str) and attr_value.isdigit():
                attr_value = int(attr_value)

            setattr(instances[key], attr_name, attr_value)
            storage.save()

        except Exception as e:
            print(e)

    def do_count(self, line):
        """counts number of instances of specified class"""
        count = 0
        if line:
            if line in self.classes:
                for value in storage.all().values():
                    if value.to_dict()["__class__"] == str(line):
                        count += 1
                print(count)
            else:
                print("** class doesn't exist **")
                return
        elif not line:
            print("** class name missing **")

    def default(self, line):
        """handles class methods"""
        parts = re.findall("(.*)[.](.*)[(](.*)[)]", line)
        if parts:
            args = line.split(".")
            args_2 = args[1].split("(")
            args_3 = args_2[1].split(", ")
            args_4 = args_3[len(args_3) - 1].split(")")
            final_list = [args[0], args_2[0]]
            for i in range(0, len(args_3) - 1):
                final_list.append(args_3[i])
            final_list.append(args_4[0])
            if final_list[2] == "":
                new_line = final_list[0]
            else:
                new_line = final_list[0] + " " + " ".join(final_list[2:])
            eval("self.do_{}('{}')".format(final_list[1], new_line))
        else:
            print("***COMMAND NOT FOUND****\nCommand list:\
                  \n-create\n-update\n-show\n-destroy\n*****")

    def emptyline(self):
        """Do nothing on empty line."""
        pass

    def do_EOF(self, args):
        """EOF command to exit the program"""
        return True

    def do_quit(self, args):
        """Quit command to exit the program"""
        return True


if __name__ == "__main__":
    console = HBNBCommand()
    console.prompt = "(hbnb) "
    console.cmdloop()
