def read_yml(file_name: str):
    import yaml
    with open(file_name, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def read_active_config(file_name: str):
    local_config = read_yml(file_name=file_name)
    active_profile = local_config['active']
    return local_config['profiles'][active_profile]


if __name__ == '__main__':
    config = read_active_config("others/application.yml")
    print(config)
