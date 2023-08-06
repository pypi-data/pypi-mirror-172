from textwrap import wrap
from random import randint
from os.path import split, splitext

from eis1600.miu_handling.re_patterns import HEADER_END_PATTERN, SPACES_PATTERN, NEWLINES_PATTERN, POETRY_PATTERN, \
    SPACES_AFTER_NEWLINES_PATTERN, PAGE_TAG_ON_NEWLINE_PATTERN, UID_PATTERN, HEADING_OR_BIO_PATTERN, \
    POETRY_TO_PARAGRAPH, BIO_CHR_TO_NEWLINE_PATTERN


def generate12ids_iterator(iterations):
    ids = []
    for i in range(0, iterations):
        ids.append(randint(400000000000, 999999999999))
    ids = set(ids)
    return ids


def wrap_paragraph(paragraph, len_symb):
    wrapped = '\n'.join(wrap(paragraph, len_symb))
    return wrapped


def convert_to_eis1600_light(infile, output_dir=None, verbose=False):
    """Coverts a file to EIS1600TMP for review process.

    Converts mARkdown, inProgress, completed file to light EIS1600TMP for the review process. Creates the file with the
    '.EIS1600TMP' extension.

    :param str infile: Path of the file to convert.
    :param str or None output_dir: Directory to write new file to (discontinued), defaults to None.
    :param bool verbose: If True outputs a notification of the file which is currently processed, defaults to False.
    :return: None.
    """
    if output_dir:
        path, uri = split(infile)
        uri, ext = splitext(uri)
        outfile = output_dir + '/' + uri + '.EIS1600TMP'
    else:
        path, ext = splitext(infile)
        outfile = path + '.EIS1600TMP'
        path, uri = split(infile)

    if verbose:
        print(f'Convert {uri} from mARkdown to EIS1600 file')

    with open(infile, 'r', encoding='utf8') as infileh:
        text = infileh.read()

    header_and_text = HEADER_END_PATTERN.split(text)
    header = header_and_text[0] + header_and_text[1]
    text = header_and_text[2]

    # fix
    text = text.replace('~\n', '\n')
    text = text.replace('\n~~', ' ')

    # spaces
    text, n = SPACES_AFTER_NEWLINES_PATTERN.subn('\n', text)
    text, n = SPACES_PATTERN.subn(' ', text)

    # fix poetry
    text, n = POETRY_PATTERN.subn(r'\1', text)
    text, n = POETRY_TO_PARAGRAPH.subn(r'\1\n\n\2', text)

    # fix page tag on newlines
    text, n = PAGE_TAG_ON_NEWLINE_PATTERN.subn(r' \1', text)

    text = text.replace('\n###', '\n\n###')
    text = text.replace('\n# ', '\n\n')

    text = NEWLINES_PATTERN.sub('\n\n', text)

    text = text.split('\n\n')

    text_updated = []

    for paragraph in text:
        if paragraph.startswith('### '):
            paragraph = paragraph.replace('###', '#')
            paragraph = BIO_CHR_TO_NEWLINE_PATTERN.sub(r'\1\n\2', paragraph)
            text_updated.append(paragraph)
        else:
            text_updated.append(paragraph)

    text = '\n\n'.join(text_updated)

    # reassemble text
    final = header + '\n\n' + text

    with open(outfile, 'w', encoding='utf8') as outfileh:
        outfileh.write(final)


def insert_uids(infile, output_dir=None, verbose=False):
    """Insert UIDs into EIS1600TMP file and thereby convert it to EIS1600.


    :param str infile: Path of the file to convert.
    :param str or None output_dir: Directory to write new file to (discontinued), defaults to None.
    :param bool verbose: If True outputs a notification of the file which is currently processed, defaults to False.
    :return: None.
    """

    if output_dir:
        path, uri = split(infile)
        uri, ext = splitext(uri)
        outfile = output_dir + '/' + uri + '.EIS1600'
    else:
        path, ext = splitext(infile)
        outfile = path + '.EIS1600'
        path, uri = split(infile)

    if verbose:
        print(f'Insert UIDs into {uri} and convert to final EIS1600 file')

    with open(infile, 'r', encoding='utf8') as infileh:
        text = infileh.read()

    header_and_text = HEADER_END_PATTERN.split(text)
    header = header_and_text[0] + header_and_text[1]
    text = header_and_text[2]
    text = text.split('\n\n')
    text_updated = []

    ids_iter = generate12ids_iterator(3000000).__iter__()

    text_iter = text.__iter__()
    paragraph = next(text_iter)
    while paragraph:
        next_p = next(text_iter, None)
        if paragraph.startswith('#'):
            paragraph = paragraph.replace('#', f'_ء_#={next(ids_iter)}=')
            if next_p and not next_p.startswith('#'):
                heading_and_text = paragraph.split('\n', 1)
                if len(heading_and_text) > 1:
                    paragraph = heading_and_text[0] + f'\n\n_ء_={next(ids_iter)}= ::UNDEFINED:: ~\n' + \
                                heading_and_text[1]
            text_updated.append(paragraph)
        elif '%~%' in paragraph:
            paragraph = f'_ء_={next(ids_iter)}= ::POETRY:: ~\n' + paragraph
            text_updated.append(paragraph)
        else:
            paragraph = f'_ء_={next(ids_iter)}= ::UNDEFINED:: ~\n' + paragraph
            text_updated.append(paragraph)

        paragraph = next_p

    text = '\n\n'.join(text_updated)

    # reassemble text
    final = header + '\n\n' + text

    with open(outfile, 'w', encoding='utf8') as outfileh:
        outfileh.write(final)


def update_uids(infile, verbose):
    """

    TODO not finished yet

    :param str infile:
    :param bool verbose:
    :return:
    """

    path, ext = splitext(infile)
    outfile = path + '.EIS1600'
    path, uri = split(infile)

    if verbose:
        print(f'Update UIDs in {uri}')

    with open(infile, 'r', encoding='utf8') as infileh:
        text = infileh.read()

    header_and_text = HEADER_END_PATTERN.split(text)
    header = header_and_text[0] + header_and_text[1]
    text = header_and_text[2]
    text = text.split('\n\n')
    text_updated = []

    used_ids = []

    for paragraph in text:
        if UID_PATTERN.match(paragraph):
            used_ids.append(int(UID_PATTERN.match(paragraph).group('UID')))

    new_ids = generate12ids_iterator(3000000)
    ids = new_ids.difference(used_ids)
    ids_iter = ids.__iter__()

    for paragraph in text:
        if HEADING_OR_BIO_PATTERN.match(paragraph):
            paragraph = f'_ء_#={next(ids_iter)}= ' + paragraph
            text_updated.append(paragraph)
        elif not UID_PATTERN.match(paragraph):
            section_header = '' if paragraph.startswith('::') else '::UNDEFINED:: ~\n'
            paragraph = f'_ء_={next(ids_iter)}= {section_header}' + paragraph
            text_updated.append(paragraph)
        else:
            text_updated.append(paragraph)

    text = '\n\n'.join(text_updated)

    # reassemble text
    final = header + '\n\n' + text

    with open(outfile, 'w', encoding='utf8') as outfileh:
        outfileh.write(final)
