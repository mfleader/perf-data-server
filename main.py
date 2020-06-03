from bottle import route, run, hook, response, request
import json
import os, pathlib


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


@hook('after_request')
def enable_cors():
    """
    You need to add some headers to request.
    Don't use the wildcard '*' for Access-Control-Allow-Oirgin in production.
    """
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Request-With, X-CSRF-Token'


@route('/', method='GET')
def root():
    return {
        'api': 'api/'
    }


def suffix():
    return 'smoke'


@route('/api', method='POST')
def upload():
    # get all file keys
    # request.files.keys()

    upload = request.files.get('file')
    print(upload.filename)

    client_ip = request.environ.get('HTTP_X_FORWARDED_FOR') \
        or request.environ.get('REMOTE_ADDR')
    print(f'request is coming from ip {client_ip}')

    name, ext = os.path.splitext(upload.filename)
    if ext not in {'.png', '.tar.gz', '.jpeg', '.jpg'}:
        return 'File extension not allowed.'

    # shell timestamp
    # $(date '+%Y-%m-%d_%H.%M.%S')

    filepath = '/'.join((
        ROOT_DIR, 
        'results',
        client_ip,
        '-'.join((
            request.environ.get('WORKLOAD_TYPE'),
            'timestamp', # add timestamp
            suffix()
        ))
    ))
    print(filepath)

    pathlib.Path(filepath) \
        .mkdir(parents=True, exist_ok=True)
    
    # appends upload.filename automatically
    # upload.save(
    #     destination = filepath
    # ) 
    return 'OK'

    
if __name__ == '__main__':
    run(host='0.0.0.0', port=8080, debug=True)
