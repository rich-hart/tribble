import os
import subprocess
import argparse
BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'tribble')

def main(argv=None):
#    import ipdb; ipdb.set_trace()
    parser = argparse.ArgumentParser(
        description='Return a list of related pages between two pdfs.')
    parser.add_argument('-min_h', '--min_hue', type=int, default=100)
    parser.add_argument('-min_s', '--min_saturation', type=int, default=80)
    parser.add_argument('-min_v', '--min_value', type=int, default=70)
    parser.add_argument('-max_h', '--max_hue', type=int, default=185)
    parser.add_argument('-max_s', '--max_saturation', type=int, default=255)
    parser.add_argument('-max_v', '--max_value', type=int, default=190)
    args = parser.parse_args(argv)
    settings = vars(args)


    for filename in os.listdir(BASE_DIR):
        if '.cr2' in filename.lower() or '.jpg' in filename.lower():
            outfile = os.path.basename(filename).split('.')[0]
            command = "python convert_img.py /vagrant/src/tribble/{0} " \
                          "--output /vagrant/src/tribble/converted_{1}.png".format(filename,outfile)
            subprocess.call(command.split(' '))
            command = "python greenscreen_remove.py /vagrant/src/tribble/converted_{0}.png".format(outfile)
            for k,v in settings.items():
                command = command + " --{0} {1} ".format(k,v)
            subprocess.call([ a for a in command.split(' ') if a]) 

            command = "python resize_img.py /vagrant/src/tribble/converted_{0}.png --output /vagrant/src/tribble/resized_{0}.png".format(outfile)
            subprocess.call([ a for a in command.split(' ') if a]) 

    return None

if __name__ == "__main__":
    main()
