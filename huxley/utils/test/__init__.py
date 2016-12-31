# Copyright (c) 2011-2016 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

import csv
import StringIO


class TestFiles():
    @staticmethod
    def new_csv(content=[], filename='test.csv'):
        f = StringIO.StringIO()
        f.name = filename

        writer = csv.writer(f)
        for row in content:
            writer.writerow(row)
        f.seek(0)

        return f
