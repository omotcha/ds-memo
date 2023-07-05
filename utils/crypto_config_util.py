import os
from configs.common import crypto_config_dir

# this util is solely based on path walking, so make sure the file structure is correct


def get_orgs_name() -> list:
    return os.listdir(crypto_config_dir)


def get_orgs_num() -> int:
    return len(get_orgs_name())


def get_cas_path() -> list:
    result = []
    for org_name in get_orgs_name():
        cacrt = os.path.join(crypto_config_dir, org_name, "ca", "ca.crt")
        result.append(cacrt)
    return result


def get_users_name(org_name: str) -> list:
    return os.listdir(os.path.join(crypto_config_dir, org_name, "user"))


def get_users_num(org_name: str) -> int:
    return len(get_users_name(org_name))


def get_user_certs_path(org_name, user_name):
    base_dir = os.path.join(crypto_config_dir, org_name, "user", user_name)
    return {
        "sign.crt": os.path.join(base_dir, f"{user_name}.sign.crt"),
        "sign.key": os.path.join(base_dir, f"{user_name}.sign.key"),
        "tls.crt":  os.path.join(base_dir, f"{user_name}.tls.crt"),
        "tls.key":  os.path.join(base_dir, f"{user_name}.tls.crt")
    }


def test_crypto_config_util():
    test_org_name = get_orgs_name()[0]
    test_user_name = get_users_name(test_org_name)[0]
    print(get_user_certs_path(test_org_name, test_user_name))


if __name__ == '__main__':
    test_crypto_config_util()
