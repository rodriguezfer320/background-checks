from flask import send_file
from os import getcwd

class File:
    _dir_file = getcwd() + r'/app/static/verification_request_files/{}.pdf'

    @staticmethod
    def get(filename):
        return send_file(File._dir_file.format(filename))

    @staticmethod
    def save(file, filename):
        file.save(File._dir_file.format(filename))
