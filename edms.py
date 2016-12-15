import repository
import config


def main():
    configuration = config.parse('config.toml')
    repository.get_instance(configuration)


if __name__ == '__main__':
    main()
