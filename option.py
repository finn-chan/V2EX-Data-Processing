from argparse import ArgumentParser


def Parse() -> dict:
    parser = ArgumentParser(description='V2EX 数据获取与预处理')
    parser.add_argument(
        '--config', '-c', type=str,
        default='./config.json',
        help='配置文件路徑',
    )
    return vars(parser.parse_args())
