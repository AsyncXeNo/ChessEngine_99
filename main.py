from my_logging import get_logger
from game.board import Board


def main():
    logger = get_logger(__name__)
    logger.info('Starting application.')

    b = Board()
    b.test()


if __name__ == '__main__':
    main()
