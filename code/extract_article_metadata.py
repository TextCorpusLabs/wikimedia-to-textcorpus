import csv
import mwxml
import pathlib
import progressbar as pb
import utils as u
from argparse import ArgumentParser
from collections import namedtuple
from os.path import getsize
from typeguard import typechecked

# declare all the named tuples up front
WMD = namedtuple('WMD', 'id title')

@typechecked
def extract_article_metadata(mediawiki_file: pathlib.Path, metadata_file: pathlib.Path) -> None:
    """
    Extracts the metadata from a Wikimedia dump file, capturing article ID and title.
    There can be more articles in the metadata file than in the file generated by `extract_article_metadata()`.
    This is because `extract_article_metadata()` removes some of the nonsence articles.
    If you want an exact match, do an inner join

    Parameters
    ----------
    mediawiki_file : pathlib.Path
        The XML dump file from Wikimedia
    metadata_file : pathlib.Path
        The CSV of Wikimedia metadata
    """

    if metadata_file.exists():
        metadata_file.unlink()

    widgets = ['Extracting Metadata: ', pb.Percentage(), ' ', pb.Bar(marker = '.', left = '[', right = ']'), ' ', pb.ETA()]
    with pb.ProgressBar(widgets = widgets, max_value = getsize(mediawiki_file)) as bar:
        with open(mediawiki_file, 'r', encoding = 'utf-8') as mediawiki_file:            
            with open(metadata_file, 'w', encoding = 'utf-8', newline = '') as metadata_file:
                metadata_file = csv.writer(metadata_file, delimiter = ',', quotechar = '"', quoting = csv.QUOTE_ALL)
                metadata_file.writerow(['id', 'title'])
                for article in u.list_articles(mediawiki_file):
                    try:
                        wmd = __parse_wmd(article)
                        metadata_file.writerow([wmd.id.rjust(10, '0'), wmd.title])
                        bar.update(mediawiki_file.tell())
                    except Exception as ex:
                        print(article.page.title + ': ' + str(ex))

@typechecked
def __parse_wmd(article: mwxml.iteration.revision.Revision) -> WMD:
    """
    Gets the parts of the wiki markdown we care about
    """

    return WMD(str(article.page.id), article.page.title)

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument(
        '-in', '--file-in',
        help = 'The XML dump file from Wikimedia',
        type = pathlib.Path,
        required = True)
    parser.add_argument(
        '-out', '--file-out',
        help = 'The CSV of Wikimedia metadata',
        type = pathlib.Path,
        required = True)
    args = parser.parse_args()    
    print(f'in: {args.file_in}')
    print(f'out: {args.file_out}')
    extract_article_metadata(args.file_in, args.file_out)
