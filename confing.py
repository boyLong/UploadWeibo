import configparser


class Config(object):
    def __init__(self, ini='conf\\config.ini'):
        self.config = configparser.ConfigParser()
        self.config.read(ini,encoding="utf-8")

    def __new__(cls, *args, **kwargs):
        if not hasattr(Config, "_instance"):
            Config._instance = object.__new__(cls)
        return Config._instance

    @staticmethod
    def read_account(type_=True):
        try:
            if type_:
                with open('conf\\account.txt', 'r') as r:
                    return r.read()
        except:
            with open('conf\\account.txt', 'w') as r:
                return ''
        with open('conf\\account.txt', 'r') as r:
            accounts = r.read().split("\n")
            all_account = {}
            for account in accounts:
                item = account.split("|")
                all_account[item[0]] = item
            return all_account

    @staticmethod
    def write_account(account='', type_='w'):
        with open('conf\\account.txt', type_) as w:
            w.write(account+"\n")


if __name__ == '__main__':
    # a = Config()
    # print(a.config['code']['path'])
    # a.config.add_section("qwewe")
    # a= Config()
    # print(a.config.sections())
    print(Config.read_account(type_=False))