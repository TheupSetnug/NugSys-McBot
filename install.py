import pip
import sys

def install_required_libraries():
    import pip
    try:
        pip.main(['install', '-r', 'requirements.txt'])
        print('Successfully installed required libraries')
    except Exception as e:
        print(e)
        print('Error installing required libraries, please install them manually')
        sys.exit(1)