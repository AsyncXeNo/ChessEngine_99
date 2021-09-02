from my_logging import get_logger
from application import Application
from game.board import Board


def main():
    logger = get_logger(__name__)
    logger.info('Starting application.')
    Application(1, 640, 640, Board())


if __name__ == '__main__':
    main()
