import os
import sys
import logging
import psycopg2
from config import config, convertTuple
from flask import Flask, jsonify

app = Flask(__name__)

logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.DEBUG)
stdout_handler.setFormatter(formatter)
file_handler = logging.FileHandler('application.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.addHandler(stdout_handler)

# assist to debug when flask web server 
# unable to connect postgresSQL container
returnString = "Return has not been initialized"

@app.route('/outperformers/<month>')
def getOuterPerformer(month=0):
    conn = None
    global resp

    if int(month) > 0 and int(month) <= 12:
        try:
            params = config()
            logger.info('getOuterPerformer:Connecting to the PostgreSQL database...')
            conn = psycopg2.connect(**params)
            logger.info('getOuterPerformer:connection successful')
            cur = conn.cursor()
            sql = 'SELECT ticker, tri_return FROM monthly_market_outperformer WHERE MONTH = '+ str(month) +' AND outperform = TRUE ORDER BY ticker ASC'
            cur.execute(sql)
            logger.info('getOuterPerformer:' + sql)
            outperformRs = cur.fetchall()

            resultDict = {}
            for row in outperformRs:
                resultDict[row[0]] = str(row[1])

            message = {
                "month": month,
                "field": "outperformers",
                "results":[resultDict]
            }    
            resp = jsonify(message)
            resp.status_code = 200
            logger.info("getOuterPerformer:" + str(len(resultDict)) + " numbers of message" )
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            resp.status_code = 500
            logger.error('getOuterPerformer: ' + error)
        finally:
            if conn is not None:
                conn.close()
                logger.info('getOuterPerformer:Database connection closed.')
    else:
        message = {
                "month": month,
                "field": "outperformers",
                "status": "Invalid month",
                "results":[]
            }   
        resp = jsonify(message)
        resp.status_code = 200
        logger.info("getOuterPerformer: 0 numbers of message" )
        
    return resp

@app.route('/healthCheck', methods=['POST', 'GET'])
def checkPostgresSQL():
    global returnString
    conn = None
    
    returnString = "enter func: checkPostgresSQL"
    try:
        params = config()
        logger.info('checkPostgresSQL:Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
        logger.info('checkPostgresSQL:Connection successful')
        cur = conn.cursor()
        cur.execute('SELECT version()')
        db_version = cur.fetchone()
        returnString = convertTuple(db_version)
        logger.info(returnString)

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        returnString = "return has been throwed"
        logger.error('checkPostgresSQL:' + error)
    finally:
        if conn is not None:
            conn.close()
            logger.info('checkPostgresSQL:Database connection closed.')
    
    return returnString

@app.route('/test', methods=['POST', 'GET'])
def hello():
    return "hello world!"

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5002))
    app.run(debug=True, host='0.0.0.0', port=port)