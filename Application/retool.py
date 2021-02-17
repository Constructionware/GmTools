#gmtApp.py

from Server.server import gmTools, cnf

# run application

if __name__ == "__main__":
    print(f"{cnf.TITLE} Web Application Server Starting on PORT: {cnf.PORT}")
    gmTools.run(
        host=cnf.HOST,
        port=cnf.PORT,
        debug=cnf.DEBUG,
        limit_concurrency=cnf.CONNECTIONS,
        limit_max_requests=cnf.MAX_REQUESTS,
        loop=cnf.LOOP,
        access_log=cnf.ACCESS_LOG 

    )


