import checking_topic_table
import getting_topic_id
import settings
import option


def main():
    args = option.Parse()
    config = settings.Read(args['config'])

    # checking_topic_table.check(config['hostname'], config['user_name'], config['user_password'],
    #                            config['database_name'])

    getting_topic_id.get(1, 3, config['cookie'])


if __name__ == '__main__':
    main()
