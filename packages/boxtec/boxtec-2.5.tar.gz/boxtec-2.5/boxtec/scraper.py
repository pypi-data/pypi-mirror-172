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

def choose_random(user_agents):
    return choices(population=[ua['user_agent'] for ua in user_agents],
                    weights=[ua['percent'] for ua in user_agents])