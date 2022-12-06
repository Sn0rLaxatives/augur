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
        begin_date = '1970-1-1 00:00:01'
    if not end_date:
        end_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    comment_lines_SQL = None

    if repo_id:
        comment_lines_SQL = s.sql.text(
            """
        SELECT date(rl_analysis_date), SUM(total_lines) AS nr_total_lines, SUM(code_lines) AS nr_code_lines, SUM(comment_lines) AS nr_comment_lines,
            (SUM(code_lines) * 100 / NULLIF(CAST(SUM(total_lines) AS FLOAT), 0)) AS Percentage_of_code_lines, 
            (SUM(comment_lines) * 100 / NULLIF(CAST(SUM(total_lines) AS FLOAT), 0)) AS Percentage_of_comment_lines  
        FROM repo_labor
        WHERE repo_id = :repo_id
            AND rl_analysis_date BETWEEN :begin_date AND :end_date
        GROUP BY date(rl_analysis_date)
        ORDER BY date(rl_analysis_date);

            """
        )
    else:
        comment_lines_SQL = s.sql.text(
            """
        SELECT date(rl_analysis_date), SUM(total_lines) AS nr_total_lines, SUM(code_lines) AS nr_code_lines, SUM(comment_lines) AS nr_comment_lines,
        (SUM(code_lines) * 100 / NULLIF(CAST(SUM(total_lines) AS FLOAT), 0)) AS Percentage_of_code_lines, (SUM(comment_lines) * 100 / NULLIF(CAST(SUM(total_lines) AS FLOAT), 0)) AS Percentage_of_comment_lines  
            FROM repo_labor, repo 
            WHERE repo_labor.repo_id = repo.repo_id
            AND repo_group_id = :repo_group_id
        AND rl_analysis_date BETWEEN :begin_date AND :end_date
        GROUP BY date(rl_analysis_date)
        ORDER BY date(rl_analysis_date);     
            """
        )

    results = pd.read_sql(comment_lines_SQL, engine, params={'repo_id': repo_id, 
        'repo_group_id': repo_group_id,'begin_date': begin_date, 'end_date': end_date, 'period':period})

    return results
