"""Main module for the application."""

import readline  # pylint: disable=unused-import

from .cli import parser
from .command import practice, show_progress
from .persistence import load_quizzes, load_progress


def main():
    """Main program."""
    namespace = parser.parse_args()
    quizzes = load_quizzes(namespace.language, namespace.deck)
    progress = load_progress()
    if namespace.command == "practice":
        practice(quizzes, progress)
    else:
        show_progress(namespace.language, quizzes, progress)
