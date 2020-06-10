import bottle
from bottle import response, request
import datetime, os, pathlib, pprint


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
VALID_EXTENSIONS = (
    '.png', '.jpeg', '.jpg',
    '.tar.gz', '.tar.xz', '.tar.bz2'
)


@bottle.hook('after_request')
def enable_cors():
    """
    You need to add some headers to request.
    Don't use the wildcard '*' for Access-Control-Allow-Oirgin in production.
    """
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Request-With, X-CSRF-Token'


@bottle.get('/')
def root(): return {'api': 'api/'}


@bottle.post('/api')
def upload():
    # get all file keys
    # request.files.keys()

    upload = request.files.get('file')
    # print(upload.filename)

    client_ip = request.environ.get('HTTP_X_FORWARDED_FOR') \
        or request.environ.get('REMOTE_ADDR')
    # print(f'request is coming from ip {client_ip}')

    if not upload.filename.endswith(VALID_EXTENSIONS):
        bottle.abort(400, 'File extension not allowed.')

    # print(request.forms.get('username'))
    # print(request.forms.get('clustername'))

    filepath = '/'.join((
        ROOT_DIR, 
        'results',
        client_ip,
        '-'.join((
            workload_type(request),
            datetime.datetime.now().strftime('%Y-%m-%d_%H.%M.%S'),
            trial_name(request)
        ))
    ))
    print(filepath)

    pathlib.Path(filepath) \
        .mkdir(parents=True, exist_ok=True)
    
    # appends upload.filename automatically
    upload.save(destination = filepath) 
    return 'OK'


def workload_type(request):
    env_var = request.environ.get('WORKLOAD_TYPE')
    if env_var and len(env_var) > 0: # exists
        return env_var
    # else    
    bottle.abort(400, 'Missing environment variable WORKLOAD_TYPE.')


def trial_name(request):
    env_var = request.environ.get('TRIAL_NAME')
    if env_var and len(env_var) > 0: # exists
        return env_var
    # else    
    bottle.abort(400, 'Missing environment variable TRIAL_NAME.')


def compose_filepath():
    return ''

    
if __name__ == '__main__':
    bottle.run(host='0.0.0.0', port=7070, debug=True)
