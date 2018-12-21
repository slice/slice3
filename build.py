import argparse
import os
import shutil
from pathlib import Path

skin_components = {
    # gameplay countdown before a map
    'countdown',

    'cursor',

    'followpoints',

    # 300s/100s/50s
    'hitbursts',

    # hitcircle numbers
    'hitcirclenum',

    'hitcircles',

    'hitsounds',

    'inputoverlay',

    # mode selection icons
    'mode',

    # gameplay mod icons
    'mods',

    # 'num' should be copied as-is

    # pause screen components
    'pause',

    # grades/ranking screen stuff
    'ranking',

    # hp bar
    'scorebar',

    # song selection buttons
    'selection',

    'sliders',

    'spinner',

    # generic ui stuff
    'ui',

    # ui sound effects
    'uisfx',
}


static_components = {
    # blank image file
    '_blank.png',

    # credits
    '_README.txt',

    # menu sound origins
    'menu sound location.txt',

    # skin.ini
    'skin.ini',
}


# https://stackoverflow.com/a/12514470/2491753
def copytree(src, dst, symlinks=False, ignore=None):
    files = os.listdir(src)
    should_ignore = ignore(src, files)
    for item in filter(lambda file: file not in should_ignore, files):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)


def copy_component(output, component):
    src = str(Path(component).resolve())
    dst = str(output)

    copytree(
        src,
        dst,
        ignore=shutil.ignore_patterns(
            '*.db', '*.psd', '*.xcf', '*.pxm', '*.pdn',
            '.DS_Store',
        ),
    )


def build(output, args):
    if args.clean and output.is_dir():
        print(f'[!] Automatically cleaning {output}')
        shutil.rmtree(str(output))

    output.mkdir(parents=True, exist_ok=True)

    components = skin_components

    to_merge = args.merge
    merged = set()
    for specifier in to_merge:
        path = Path.cwd() / specifier
        if not path.is_dir():
            print(f'[-] {path} (deduced from {specifier}) does not point to a directory.')
            return
        print(f'[*] Merging {specifier}')
        merged.add(path.name)
        copy_component(output, path)

    components = components - merged

    for num, component in enumerate(components):
        progress = f'{num + 1}/{len(components)}'
        print(f'[*] Merging component {component} to {output} [{progress}]')
        copy_component(output, component)

    print(f'[*] Merging component num to {output} (*/*)')
    (output / 'num').mkdir(exist_ok=True)
    copy_component(output / 'num', 'num')

    for component in static_components:
        print(f'[*] Copying static component {component}')
        shutil.copy2(component, str(output))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('build_output', help='the dir to output the built skin to')
    parser.add_argument(
        '--clean', '-c',
        help='automatically clean output dir',
        action='store_true',
    )
    parser.add_argument(
        '--merge', '-m',
        metavar='COMPONENT',
        help='merge component (can be used multiple times)',
        action='append',
        default=[],
    )
    args = parser.parse_args()
    build(Path(args.build_output), args)
