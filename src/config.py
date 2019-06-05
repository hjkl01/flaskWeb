import ruamel.yaml as yaml


class ConfigMeta(object):
    def __getattr__(self, key):
        try:
            with open('settings.yaml', 'r') as file:
                self.con = yaml.safe_load(file)
        except BaseException:
            warning_info = 'using default param , please read readme.md and touch settings.yaml '
            print(warning_info)
        return self.con.get(key)


config = ConfigMeta()
