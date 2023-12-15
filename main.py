import checking_topic_table
import settings
import option


def main():
    args = option.Parse()
    config = settings.Read(args['config'])

    checking_topic_table.check(config['hostname'], config['user_name'], config['user_password'],
                               config['database_name'])


if __name__ == '__main__':
    main()
