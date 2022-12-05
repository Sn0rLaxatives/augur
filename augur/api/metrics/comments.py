#SPDX-License-Identifier: MIT
"""
Metrics that provides data about comments in a repository
"""

import datetime
import sqlalchemy as s
import pandas as pd
from augur.api.util import register_metric

from augur.application.db.engine import create_database_engine
engine = create_database_engine()

@register_metric()
def number_of_comment_lines(repo_group_id, repo_id=None, begin_date=None, end_date=None, period='month'):
    """Returns the total number of comment lines in a repository
    :param repo_group_id: The repository's repo_group_id
    :param repo_id: The repository's repo_id, defaults to None
    :param period: To set the periodicity to 'day', 'week', 'month' or 'year', defaults to 'day'
    :param begin_date: Specifies the begin date, defaults to '1970-1-1 00:00:00'
    :param end_date: Specifies the end date, defaults to datetime.now()
    :return: DataFrame number of total issues
    """
    if not begin_date:
        begin_date = '1970-1-1 00:00:00'
    if not end_date:
        end_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    issues_new_SQL = ''

    if not repo_id:
        issues_new_SQL = s.sql.text("""
        """)

        results = pd.read_sql(issues_new_SQL, engine, params={'repo_group_id': repo_group_id, 'period': period,
                                                               'begin_date': begin_date, 'end_date': end_date})

        return results

    else:
        issues_new_SQL = s.sql.text("""
        """)

        results = pd.read_sql(issues_new_SQL, engine, params={'repo_id': repo_id, 'period': period,
                                                               'begin_date': begin_date, 'end_date': end_date})
        return results
