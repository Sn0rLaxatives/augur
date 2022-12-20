#SPDX-License-Identifier: MIT
"""
Metrics that provides data about downloads of a repository
"""

import datetime
import sqlalchemy as s
import pandas as pd
from augur.api.util import register_metric

from augur.application.db.engine import create_database_engine
engine = create_database_engine()

@register_metric()
def number_of_downloads(repo_group_id, repo_id=None, begin_date=None, end_date=None, period='month'):
    """Returns the total number of downloads of a repository within a time period
    :param repo_group_id: The repository's repo_group_id
    :param repo_id: The repository's repo_id, defaults to None
    :param period: To set the periodicity to 'day', 'week', 'month' or 'year', defaults to 'day'
    :param begin_date: Specifies the begin date, defaults to '1970-1-1 00:00:00'
    :param end_date: Specifies the end date, defaults to datetime.now()
    :return: DataFrame number of total issues
    """
    if not begin_date:
        begin_date = '1970-1-1 00:00:01'
    if not end_date:
        end_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    comment_lines_SQL = None

    if repo_id:
        comment_lines_SQL = s.sql.text(
            """
            SELECT SUM(downloads) as Total_Number_Of_Downloads, 
	                  :begin_date AS Begin_Date, :end_date AS End_Date 
            FROM repo_labor
            WHERE repo_id = :repo_id
	          AND rl_analysis_date BETWEEN :begin_date AND :end_date              
            """
        )
    else:
        comment_lines_SQL = s.sql.text(
            """
            SELECT SUM(downloads) as Total_Number_Of_Downloads, 
                   :begin_date AS Begin_Date, :end_date AS End_Date 
            FROM repo_labor, repo 
            WHERE repo_labor.repo_id = repo.repo_id
                AND repo_group_id = :repo_group_id
                AND rl_analysis_date BETWEEN :begin_date AND :end_date
            """
        )

    results = pd.read_sql(comment_lines_SQL, engine, params={'repo_id': repo_id, 
        'repo_group_id': repo_group_id,'begin_date': begin_date, 'end_date': end_date, 'period':period})

    return results
