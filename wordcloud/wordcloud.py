from __future__ import print_function 
from sys import exit, argv
import matplotlib as plt
import wordcloud 
from os import path
from docopt import docopt

def readfiles(filenames): 
    text = ""
    # Read the whole text for each file
    for filename in filenames:
        try:
            text += open(filename, 'r').read()
            text += r"\n"
        except Exception as e:
            printc("<ERROR>Error, exception: <reset>{}.".format(e))
            printc("<red>Skipping file <black>'{}'<reset>...".format(filename))
    return text

def generate(text, max_words=200, width=800, height=600):
    #Generate a word cloud image from the given file
    max_words = int(max_words) if max_words is not None else  200
    width     = int(width)     if width     is not None else  800
    height    = int(height)    if height    is not None else  600
    wc = WordCloud(max_font_size=40,
                   relative_scaling=.5,
                   max_words=max_words,
                   width=width,
                   height=height
                   )
    return wc.generate(text)

def makeimage(wordcloud,
              outname='wordcloud.png', title='Word cloud', show=False, force=False):
    """ Display or save the wordcloud as a image. """
    # Display the generated image:
    try:
        # 2. the matplotlib way:
        plt.figure()
        plt.imshow(wordcloud)
        plt.axis("off")
        if title:
            printc("<magenta>Using title<reset> <blue>'{}'<reset>.".format(title))
            plt.title(title)
        if show:
            printc("<green>Showing the generated image...<reset>")
            plt.show()
        else:
            printc("<green>Saving the generated image<reset> to <blue>'{}'<reset>...".format(outname))
            if (not force) and path.exists(outname):
                erase = raw_input("The outfile '{}' already exists, should I erase it ?  [y/N]".format(outname))
                if erase == 'y':
                    plt.savefig(outname)
                else:
                    printc("<magenta>Not erasing it...<reset>")
                    printc("<green>Showing the generated image...<reset>")
                    plt.show()
            else:
                if force:
                    printc("<WARNING> -f or --force has been used, overwriting the image '{}' <red>without<reset> asking you...".format(outname))
                plt.savefig(outname)
    except Exception as e:
        printc("<ERROR> Error, exception<reset>: {}".format(e))
        printc("<WARNING> Something went wrong with matplotlib, switching to PIL backend... (just showing the image, <red>not<reset> saving it!)")
        image = wordcloud.to_image()
        image.show()
    return True
	
	
def main(argv):
    """ Use the arguments of the command line. """
    # Use the arg parser
    args = docopt(full_docopt_text, argv=argv, version="generate-word-cloud.py v{}".format(version))
    # printc("<magenta>Arguments: {} <reset>".format(args))  # DEBUG

    # Read the files
    printc("<green>Reading the files<reset>, from: <blue>{}<reset>.".format(args['INFILE']))
    text = readfiles(args['INFILE'])
    # Decide where to save it
    outname = args['--outfile'] if args['--outfile'] else 'wordcloud.png'
    # Generate the wordcloud
    wordcloud = generate(text,
                         max_words=args['--max'],
                         width=args['--width'],
                         height=args['--height']
                         )
    # Finally, saving the image
    printc("<green>Making the image<reset> and saving it to <blue>{}<reset>.".format(outname))
    makeimage(wordcloud,
              outname=outname, title=args['--title'],
              force=args['--force'], show=args['--show']
              )
    return 0


if __name__ == "__main__":
    exit(int(main(argv[1:])))