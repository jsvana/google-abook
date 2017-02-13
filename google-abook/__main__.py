import argparse
import csv
import os
import sys


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        'contacts',
        help='Google contacts CSV to import',
    )

    parser.add_argument(
        '--output',
        default='$HOME/.abook/addressbook',
        help='Location to write abook file (default: %(default)s)',
    )

    parser.add_argument(
        '--force',
        action='store_true',
        help='Overrite existing addressbook output file',
    )

    parser.add_argument(
        '--version',
        default='0.6.1',
        help=(
            'Version of abook to use (run "abook" to see its version, default'
            ' is %(default)s)'
        ),
    )

    return parser.parse_args()


def translate_row(row):
    name = row['Name']
    if not name:
        name = '{} {}'.format(row['Given Name'], row['Family Name'])
    if not name or name == ' ':
        return None

    return dict(
        name=name,
        phone=row['Phone 1 - Value'],
        email=row['E-mail 1 - Value'],
    )


def main():
    args = parse_args()

    if not os.path.exists(args.contacts):
        print('Contacts file {} does not exist'.format(args.contacts))
        return False

    if not args.force and os.path.exists(args.output):
        print('Addressbook already exists. Pass --force to overwrite.')
        return False

    output = []
    with open(args.contacts, 'r', encoding='utf-16') as f:
        for row in csv.DictReader(f):
            translated = translate_row(row)
            if not translated:
                continue
            output.append(translated)

    fields = [
        'name',
        'phone',
        'email',
    ]

    with open(os.path.expandvars(args.output), 'w') as f:
        f.writelines([
            '[format]\n',
            'program=abook\n',
            'version={}\n'.format(args.version),
        ])
        for i, row in enumerate(output):
            f.write('\n[{}]\n'.format(i))
            for field in fields:
                if row[field]:
                    f.write('{}={}\n'.format(field, row[field]))
                else:
                    f.write('\n')

    return True


if __name__ == '__main__':
    sys.exit(0 if main() else 1)
