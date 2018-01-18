## Python Flask API demo 

In this project I implemented a simple **flask** server that serves REST API requests on top of a SQLite database.

## Dependencies:  
- python 3 (tested on 3.6)
- sqlite3  
- re  
- flask_api  
- flask  
- jinja2  


## Deployment

The falsk server can be started using a single command:  
`python flask_server.py
`

The relevant sqlite database named 'demo.sqlite' will be created and populated in the same folder as the file. 

## Testing

You can view sample requests made using cURL in the **request.sh** shell script. 

You first have to give the script executable permission:  
`chmod +x request.sh`

To run the script simply execute:  
`./request.sh`

