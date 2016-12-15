import repository
import config
import database


def main():
    configuration = config.parse('config.toml')
    repository.get_instance(configuration)
    database.get_instance(configuration)


if __name__ == '__main__':
    main()
