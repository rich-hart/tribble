import os
import subprocess
import argparse
BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'tribble')

def main(argv=None):
#    import ipdb; ipdb.set_trace()
    parser = argparse.ArgumentParser(
        description='Return a list of related pages between two pdfs.')
    parser.add_argument('-min_h', '--min_hue', type=int, default=200)
    parser.add_argument('-min_s', '--min_saturation', type=int, default=80)
    parser.add_argument('-min_v', '--min_value', type=int, default=20)
    parser.add_argument('-max_h', '--max_hue', type=int, default=280)
    parser.add_argument('-max_s', '--max_saturation', type=int, default=255)
    parser.add_argument('-max_v', '--max_value', type=int, default=190)
    args = parser.parse_args(argv)
    settings = vars(args)


    for filename in os.listdir(os.getcwd()):
        if '.cr2' in filename.lower() or '.jpg' in filename.lower():
            outfile = os.path.basename(filename).split('.')[0]
            command = "python {0}/convert_img.py {1} --output converted_{2}.png".format(BASE_DIR, filename,outfile)
            subprocess.call(command.split(' '))

            command = "python {0}/greenscreen_remove.py converted_{1}.png".format(BASE_DIR,outfile)
            for k,v in settings.items():
                command = command + " --{0} {1} ".format(k,v)
            subprocess.call([ a for a in command.split(' ') if a]) 

            command = "python {0}/resize_img.py converted_{1}.png --output resized_{1}.png".format(BASE_DIR, outfile)
            subprocess.call([ a for a in command.split(' ') if a]) 

            command = "python {0}/merge_layers.py {0}/WALL.png "\
                      "{0}/BACK_TRIBBLES.png " \
                      "resized_{1}.png " \
                      "{0}/FRONT_TRIBBLES.png " \
                      "{0}/LOGO.png " \
                      "{0}/DATE.png " \
                      "{0}/BORDER.png " \
                      "--output merged_{1}.png".format(BASE_DIR,outfile)
            subprocess.call([ a for a in command.split(' ') if a]) 

    return None

if __name__ == "__main__":
    main()
