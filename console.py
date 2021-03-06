#!/usr/bin/python3
# Displays prompt to take in user input


import cmd
import sys
from models.base_model import BaseModel
from models.__init__ import storage
from models.user import User
from models.place import Place
from models.city import City
from models.review import Review
from models.state import State
from models.amenity import Amenity


class HBNBCommand(cmd.Cmd):
    # Creates prompt as (hbnb)
    intro = ''
    prompt = '(hbnb) '
    file = None
    classes = {
            'BaseModel': BaseModel,
            'User': User,
            'Place': Place,
            'City': City,
            'Review': Review,
            'State': State,
            'Amenity': Amenity,
              }

    # Define method of objects
    def do_quit(self, arg):
        'Quit command to exit the program'
        print('')
        return True

    def do_EOF(self, arg):
        'Exits shell upon End of File'
        print('')
        return True

    def do_create(self, arg):
        'Creates a new instance of BaseModel, saves it and prints the id'
        if arg is '':
            print("** class name missing **")
        elif arg not in HBNBCommand.classes:
            print("** class doesn't exist **")
        else:
            new = HBNBCommand.classes[arg]()
            storage.save()
            print("{}".format(new.id))

    def do_show(self, arg):
        'Prints the string rep of an instance based on class name and id'
        args = arg.split(" ")
        obj_dict = storage.all()
        if arg is '':
            print("** class name missing **")
        elif args[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
        elif len(args) < 2:
            print("** instance id missing **")
        else:
            key = args[0] + '.' + args[1]
            try:
                print(obj_dict[key])
            except:
                print("** no instance found **")

    def do_destroy(self, arg):
        'Delete an object based on class name and id'
        args = arg.split(" ")
        if arg is '':
            print("** class name missing **")
        elif args[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
        elif len(args) < 2:
            print("** instance id missing **")
        else:
            key = args[0] + '.' + args[1]
            obj_dict = storage.all()
            try:
                del(obj_dict[key])
                storage.save()
            except:
                print("** no instance found **")

    def do_all(self, arg):
        'Prints all string reps of all instaces, with or without class'
        obj_dict = storage.all()
        if not arg:
            for key, value in obj_dict.items():
                print("{}".format(obj_dict[key]))
        else:
            for key, value in obj_dict.items():
                skey = key.split(".")
                if skey[0] == arg:
                    print("{}".format(obj_dict[key]))

    def do_update(self, arg):
        obj_dict = storage.all()
        args = arg.split(" ")
        if arg is '':
            print("** class name missing **")
        elif args[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
        elif len(args) < 2:
            print("** instance id missing **")
        else:
            for key, value in obj_dict.items():
                skey = key.split(".")
            if skey[0] != args[0]:
                print("** no instance found **")
            else:
                if len(args) < 3:
                    print("** attribute name missing **")
                elif len(args) < 4:
                    print("** value missing **")
                else:
                    for key, value in obj_dict.items():
                        skey = key.split(".")
                        if skey[1] == args[1]:
                            val = args[3]
                            updater = {args[2]: val.replace('"', '')}
                            (obj_dict[key].__dict__).update(updater)
                    storage.save()

    def do_count(self, arg):
        obj_dict = storage.all()
        count = 0
        args = arg.split(" ")
        _class = args[0]
        if arg:
            for key, val in obj_dict.items():
                skey = key.split(".")
                if _class == skey[0]:
                    count += 1
            print(count)

    def default(self, line):
        if "." not in line:
            return cmd.Cmd.default(self, line)
        syntax = line.split(".")
        _class = syntax[0]
        method = syntax[1]
        obj_dict = storage.all()

        if _class in HBNBCommand.classes:
            if method[0:5] == 'all()':
                HBNBCommand.do_all(self, _class)
            if method[0:8] == 'count()':
                HBNBCommand.do_count(self, _class)
            arg_split = method.split('"')
            method_id = arg_split[0]
            if method_id[0:5] == 'show(':
                class_id = arg_split[1]
                arg = _class + " " + class_id
                HBNBCommand.do_show(self, arg)
            if method_id[0:8] == 'destroy(':
                class_id = arg_split[1]
                arg = _class + " " + class_id
                HBNBCommand.do_destroy(self, arg)
            if method_id[0:7] == 'update(':
                arg_split2 = method.split(",")
                class_id = arg_split2[0].split("(")[1].replace('"', "")
                print(class_id)
                att_name = arg_split2[1].replace('"', "")
                print(att_name)
                att_val = arg_split2[2].replace(")", "")
                print(att_val)
                arg = _class + " " + class_id + " " + att_name[1:] + att_val
                print(arg)
                HBNBCommand.do_update(self, arg)

    def emptyline(self):
        'Empties last command'
        pass

    # Ovewrites help message
    def help_help(self):
        'Help message for help'
        print("Prints messages with information of command")

    def help_create(self):
        'Creates instance of object'
        print("For a new instance of an obj saves it and prints id")

    def help_quit(self):
        'Help message for quit'
        print('Exits the shell')

    def help_EOF(self):
        'Help message for EOF'
        print('Upon end of file, exits shell')

    def help_create(self):
        'Help message for create'
        print('Creates a new instance of BaseModel,\
saves it (to the JSON file) and\
prints the id. Ex: $ create BaseModel')

    def help_show(self):
        'Help message for show'
        print('Prints the string representation of an instance\
based on the class name and id.\
Ex: $ show BaseModel 1234-1234-1234.')

    def help_destroy(self):
        'Help message for destroy'
        print('Deletes an instance based on the class name\
and id (save the change into the JSON file).\
Ex: $ destroy BaseModel 1234-1234-1234.')

    def help_all(self):
        'Help message for all'
        print('Prints all string representation of all\
instances based or not on the class name.\
Ex: $ all BaseModel or $ all.')

    def help_update(self):
        'Help message for update'
        print('Updates an instance based on the class name and \
id by adding or updating attribute (save the change \
into the JSON file). Ex: $ update BaseModel \
1234-1234-1234 email "aibnb@holbertonschool.com".')

    def help_count(self):
        'Help message for count'
        print('retrieve the number of instances of a class')

if __name__ == '__main__':
    HBNBCommand().cmdloop()
