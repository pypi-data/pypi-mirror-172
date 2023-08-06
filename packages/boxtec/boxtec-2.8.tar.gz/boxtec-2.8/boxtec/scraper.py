import mysql.connector
from random import choices

def user_agents(cur):
    sql = f"""
            SELECT
                percent, user_agent
            FROM
                user_agents
            WHERE
                ts = (
                    SELECT
                        MAX(ts)
                    FROM
                        user_agents)
            """
    cur.execute(sql)
    return cur.fetchall()

def random_uas(cur, count):
    uas = user_agents(cur)
    return choices(population=[ua['user_agent'] for ua in uas],
                    weights=[ua['percent'] for ua in uas], k=count)