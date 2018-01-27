# coding=utf-8

import sqlite3
import os
import logging


class Exporter(object):
    def __init__(self, db, md_dir):
        self.db = db
        self.md_dir = md_dir
        self.conn = conn = sqlite3.connect(self.db)
        self.logger = logging.getLogger('exporter')

        if self.md_dir != "" and not os.path.isdir(self.md_dir):
            raise Exception("md path configured and dir not exists!")

    def export_to_importable_md(self):
        '''
        export_to_md do export from ghost and generates markdowns.
        '''
        if self.md_dir == "":
            raise Exception("md path not configured yet!")

        all_posts = self.conn.execute('''SELECT title, markdown FROM posts''')
        for post in all_posts:
            title = post[0]
            body = post[1]
            md_file_path = os.path.join(self.md_dir, u"{name}.md".format(name=title))
            with open(md_file_path, 'w') as fp:
                fp.write(body.encode('utf8'))

            self.logger.debug(u"successfully export {} to {}..".format(
                title, md_file_path)
            )
        self.logger.info("completed export_to_md task!")


def main():
    exp = Exporter(db="./ghost.db", md_dir="/tmp/markdowns")
    exp.export_to_importable_md()


if __name__ == '__main__':
    main()
