import sqlite3
import re
from flask_api import FlaskAPI
from flask_api import exceptions as flask_e
from flask import request, json, Response
from jinja2 import Environment

app = FlaskAPI(__name__)

# Set response to json only (globally)
app.config['DEFAULT_RENDERERS'] = [
    'flask_api.renderers.JSONRenderer'
]


# Handle 404 errors (Not found)
@app.errorhandler(404)
def not_found():
    return {'error': 'endpoint is not found'}, 404

# initialization of sqlite database
def init_sqlite_db():
    # SQLite database
    sqlite_file = 'demo.sqlite'  # name of the sqlite database file

    # Connecting to the database file
    global conn
    conn = sqlite3.connect(sqlite_file)
    global cursor
    cursor = conn.cursor()

    # Creating a new SQLite table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cars (
            make varchar(50),
            model varchar(50),
            chassis_id varchar(50),
            year int, 
            id int,
            last_updated datetime,
            price double 
        );
    """)
    conn.commit()

    rows = cursor.execute("""
      SELECT 
        * 
      FROM 
        cars ;    
    """).fetchall()

    if len(rows) < 1:
        # also could have read the CSV file with pandas and exported it to SQLite
        conn.execute("""
            INSERT INTO cars VALUES  
                ('Nissan','Micra',2004,'12345A',1,'2017-02-01 00:00:00', 500.0), 
                ('Nissan','Micra',2004,'12425A',1,'2017-03-01 00:00:00', 400.0),
                ('Ford','Fiesta',2002,'12345B',2,'2017-03-01 00:00:00', 300.0),
                ('Audi','A3',NULL,'12345C',3,'2017-04-01 00:00:00',NULL),
                ('Nissan','Micra',2004,'12345D',4,'2017-05-01 00:00:00', 200.0), 
                ('Peugeot' ,'308',1998,'12345E',5,'2017-06-01 00:00:00', 100.0) ;
        """)
    conn.commit()


# API 1
@app.route('/car/<int:id>', methods=['GET'])
def get_car_data(id):
    # quick check if table name is valid
    if re.match("[0-9]+", str(id)):
        # query data
        result_set = cursor.execute("""
            SELECT 
                make, model, year, id, last_updated, price 
            FROM 
                cars 
            WHERE id = {0}
            """.format(id))

        column_names = list(map(lambda x: x[0], cursor.description))
        rows = result_set.fetchall()

        if len(rows) > 0:
            results = []
            for row in rows:
                t = {}
                for i in range(0, len(row)):
                    t[column_names[i]] = row[i]
                results.append(t)
            output = json.dumps(results)
        else:
            raise flask_e.NotFound("Car not found")

        return Response(output, status=200, content_type='application/json')

    else:
        raise flask_e.NotFound("Please enter a proper car id")


# API 2
@app.route('/car/', methods=['GET'])
def get_all_car_data():
    # quick check if table name is valid
    result_set = cursor.execute("""
        SELECT 
            make, model, year, id, last_updated, price 
        FROM 
            cars 
        """)

    column_names = list(map(lambda x: x[0], cursor.description))
    rows = result_set.fetchall()

    if len(rows) > 0:
        results = []
        for row in rows:
            t = {}
            for i in range(0, len(row)):
                t[column_names[i]] = row[i]
            results.append(t)
        output = json.dumps(results)
    else:
        raise flask_e.NotFound("No cars stored")

    return Response(output, status=200, content_type='application/json')


# API 3
@app.route('/avgprice/', methods=['POST'])
def get_avg_price():
    json_request_data = request.get_json()

    sql_template = """
        SELECT 
            AVG(price)
        FROM 
            cars 
        WHERE 
        {%- for i in input %}
            {{i.0}} = '{{i.1}}'
            {%- if not loop.last %} AND {% endif -%}
        {%- endfor -%}
    """

    get_average_statement = Environment() \
        .from_string(sql_template) \
        .render(input=json_request_data.items())

    result = round((cursor.execute(get_average_statement).fetchone()[0]), 2)

    return {'avg_price': result}
    # the below written Response did not return the data to curl for some reason
    # return Response( {'avg_price': result}, status=200, content_type='application/json')

# API 4
@app.route('/car/', methods=['POST'])
def create_car():
    json_request_data = request.get_json()

    sql_template = """
        INSERT INTO cars ( 
        {%- for i in input %}
            {{i.0}} 
            {%- if not loop.last %} , {% endif -%}
        {%- endfor -%}
        ) 
        VALUES (
        {%- for i in input %}
            '{{i.1}}' 
            {%- if not loop.last %} , {% endif -%}
        {%- endfor -%}
        );
    """

    insert_statement = Environment() \
        .from_string(sql_template) \
        .render(input=json_request_data.items())

    try:
        cursor.execute(insert_statement)
    except:
        raise flask_e.ParseError("Data not in proper format")

    return Response('Successfully inserted', status=201)


# Run App
if __name__ == "__main__":
    init_sqlite_db()
    app.run(debug=False, host="0.0.0.0")
