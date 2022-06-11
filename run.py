import argparse
from app import app

from processing import read_txt_file, processing
from filters import fuzzy_string_matching

#sbert_model = "dangvantuan/sentence-camembert-large"
#sbert_model = "./augSbert"
#sbert_model = "./camembert_nli_stsb"
sbert_model = "distiluse-base-multilingual-cased-v1"


arg_desc = '''
        Let's load text or file to the command line!
        --------------------------------------------
          This program extract keywords from text
        '''

# Args check
import argparse
import os.path
import mimetypes

def text_check(text):
    if type(text) is str:
        if len(text)>512:
            raise argparse.ArgumentTypeError('Input text is longer than 512 tokens')
    else:
        raise argparse.ArgumentTypeError('Input is not string type')

def file_check(path):
    if not os.path.exists(path):
        raise argparse.ArgumentTypeError('The file entered is not exist')
    else:
        name, extension = os.path.splitext(path)
        if extension != '.txt':
            guess = mimetypes.guess_extension(path)
            if guess != '.txt':
                raise argparse.ArgumentTypeError('Only txt file is supported at the moment')
    return(path)

# CLI arguments
parser = argparse.ArgumentParser(description=arg_desc)
group = parser.add_mutually_exclusive_group()
group.add_argument('--text',
                    help='Input a text of maximum 512 tokens',
                    type=text_check,
                    required=False)
group.add_argument('-t',
                    '--txt',
                    help='Input txt file path',
                    type=file_check,
                    required=False)
parser.add_argument('-s',
                    '--server',
                    action='store_true',
                    help='Using server')
args = vars(parser.parse_args())

# Input & processing
if args['text']:
    print('Keywords from the text:')
    X = processing(args['text'])
    print('NER:', fuzzy_string_matching(X[0], threshold=4))
    print('KEYS:', fuzzy_string_matching(X[1], threshold=7))
    #print(X)
elif args['txt']:
    try:
        read_txt_file(args['txt'])
    except UnicodeDecodeError:
        print('Your file is not Unicode UTF-8 format. Check and try again !')
        pass
    else:
        text = read_txt_file(args['txt'])
        print('Keywords from txt file:')
        X = processing(text)
        print('NER:', fuzzy_string_matching(X[0], threshold=4))
        print('KEYS:', fuzzy_string_matching(X[1], threshold=7))
        #print(X)
elif args['server']:
    print('Server start')
    app.run(host='localhost', port=5000, debug=True)
else:
    print('Not supported')