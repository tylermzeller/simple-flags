import sys

class Flags:
    class __Flags:
        def __init__(self):
            self.flag_names = {}
            self.short_names = {}
            self._define('bool', bool)
            self._define('int', int)
            self._define('string', str)
            self._define('float', float)

        def _define(self, typename, typ):
            def define_func(name, default, help_msg='', transform=None, validate=None):
                def parse_func(value):
                    try:
                        if transform and callable(transform):
                            value = transform(value)
                        value = typ(value)
                        if validate and callable(validate) and not validate(value):
                            raise Error()
                    except Error:
                        raise AttributeError('Error parsing {tn} --{n} ' +
                        'with value {v}'.format(tn=typename, n=name, v=value))
                    setattr(self, name, value)

                self.flag_names[name] = typ
                setattr(self, 'parse_' + name, parse_func)
                getattr(self, 'parse_' + name)(default)

            setattr(self, 'define_' + typename, define_func)

        def parse_cli_args(self):
            args = sys.argv[:]
            while len(args) > 0:
                arg = self.get_next_arg()
                if arg == '--': break
                if arg[0] != '-': continue
                arg_name, arg_value = self.get_arg_name_and_value(arg, args)
                getattr(self, 'parse_' + arg_name)(arg_value)

        def get_arg_name_and_value(self, arg, args):
            name = arg[1:] if arg[1] != '-' else arg[2:]
            value = None

            if '=' in name:
                name, value = arg_name.split('=')
                if len(value) == 0:
                    raise ValueError('Invalid valid for --{n}: "{val}"'.format(n=name, val=value))

            self.raise_if_flag_doesnt_exist(name)

            if self.is_negated_bool_flag(name):
                name, value = self.handle_negated_bool_flag(name, value)
            elif self.is_bool_flag(name):
                name, value = self.handle_bool_flag(name, value)
            elif value == None:
                value = self.get_next_arg(args)
                if value[0] == '-':
                    raise ValueError('Invalid value for --{n}: "{val}"'.format(n=name, val=value))
            return name, value

        def raise_if_flag_doesnt_exist(self, flag_name):
            if not flag_name in self.flag_names and flag_name[2:] not in self.flag_names:
                raise ValueError('Unknown flag --{fn}'.format(fn=flag_name))

        def is_negated_bool_flag(self, flag_name):
            return flag_name[:2] == 'no' and self.is_bool_flag(flag_name[2:])

        def is_bool_flag(self, flag_name):
            return self.flag_names[flag_name] == bool

        def handle_negated_bool_flag(self, flag_name, flag_value):
            if flag_value:
                raise ValueError('Do not use "=" format with --{n}'.format(n=name))
            return flag_name[2:], False

        def handle_bool_flag(self, flag_name, flag_value):
            if value == None or value.lower() in ['t', 'true', 'y', 'yes']:
                return flag_name, True
            elif value.lower() in  ['f', 'false', 'n', 'no']:
                return flag_name, False
            else:
                raise ValueError('Invalid value for --{fn}: "{fv}"'.format(fn=flag_name, fv=flag_value))

        def get_next_arg(self, args):
            if len(args) == 0:
                raise ValueError('Expected next arg, but reached end.')
            return args.pop(0)

    instance = None

    def __init__(self):
        if not Flags.instance:
            Flags.instance = Flags.__Flags()

    def __getattr__(self, name):
        return getattr(self.instance, name)
