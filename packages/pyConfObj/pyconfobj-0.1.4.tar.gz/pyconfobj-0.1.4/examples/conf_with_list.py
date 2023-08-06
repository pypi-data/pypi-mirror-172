from numbers import Number
from pyConfObj import ConfObj, ConfObjList


class PgServerConf(ConfObj):
    ip: str = ""
    port: Number = 5432
    username: str = ""
    password: str = ""

    def check_pass(self) -> bool:
        for el in [self.ip, self.username, self.password]:
            if el in ["", None]:
                return False
        if self.port in [0, None]:
            return False
        return True


class MainConf(ConfObj):
    servers: ConfObjList = ConfObjList(PgServerConf)
    timezone: str = "UTC"


if __name__ == "__main__":
    conf = MainConf()
    pg_server1 = PgServerConf()
    pg_server2 = PgServerConf()
    conf.servers.append(pg_server1)
    conf.servers.append(pg_server2)
    print("Default configuration:")
    print(conf.as_json())
    print(f"Valid configuration: {conf.check()}")
    conf.servers[0].username = "admin"
    conf.servers[0].ip = "1.1.1.1"
    conf.servers[0].password = "qwerty"
    conf.servers[1].username = "admin"
    conf.servers[1].ip = "1.1.1.1"
    conf.servers[1].password = "qwerty"
    print("Modified configuration for pg: ")
    print(conf.servers.as_json())
    print(f"Valid configuration: {conf.check()}")
