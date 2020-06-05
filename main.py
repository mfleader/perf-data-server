import bottle
from bottle import response, request
import datetime, os, pathlib, pprint


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
os.environ['WORKLOAD_TYPE'] = 'devtest'
os.environ['TRIAL_NAME'] = 't0'


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
def root():
    return {
        'api': 'api/'
    }


def compose_filepath():
    return ''


@bottle.post('/api')
def upload():
    # get all file keys
    # request.files.keys()

    upload = request.files.get('file')
    # print(upload.filename)

    client_ip = request.environ.get('HTTP_X_FORWARDED_FOR') \
        or request.environ.get('REMOTE_ADDR')
    # print(f'request is coming from ip {client_ip}')

    name, ext = os.path.splitext(upload.filename)
    if ext not in {'.png', '.tar.gz', '.jpeg', '.jpg'}:
        # return 'File extension not allowed.'
        bottle.abort(400, 'File extennsion not allowed.')

    # print(request.forms.get('username'))
    # print(request.forms.get('clustername'))

    print(request.environ.get('WORKLOAD_TYPE'))
    print(request.environ.get('TRIAL_NAME'))

    # can get username and clustername from oc cluster-info
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
    
    # # appends upload.filename automatically
    upload.save(destination = filepath) 
    return 'OK'


def workload_type(request):
    env_var = request.environ.get('WORKLOAD_TYPE')
    if env_var: # exists
        return env_var
    # else    
    bottle.abort(400, 'Missing environment variable WORKLOAD_TYPE.')


def trial_name(request):
    env_var = request.environ.get('TRIAL_NAME')
    if env_var: # exists
        return env_var
    # else    
    bottle.abort(400, 'Missing environment variable TRIAL_NAME.')

    
if __name__ == '__main__':
    bottle.run(host='0.0.0.0', port=8080, debug=True)
