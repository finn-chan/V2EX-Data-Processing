import creating_topic_table
import getting_topic_id
import settings
import option


def main():
    args = option.Parse()
    config = settings.Read(args['config'])

    # getting_topic_id.get(1, 1, config['cookie'])


if __name__ == '__main__':
    main()
