# slice3

my osu! skin largely based off of -GN's edit of boom 0524 and other neat skins

## building

this skin is modular. it uses components, which are basically folders with skin
elements inside of them. building the skin merges the components together,
forming a complete skin. but you can choose which components you would like to
disable in case you don't like some stuff.

in the future there will also be a way to pick "flavors" of components so that
you may easily be able to switch between variants of components, like hitcircles
or fonts or whatever

make sure you have python 3.7+

```sh
$ python3 build.py osudirectory/Skins/slice3
```

see `--help` for more information

### exclude components

add `-x COMPONENT` to the command to exclude components from being included in
the build. by doing this, it will also automatically include the component named
`no-COMPONENT` in order to stop using default skin elements (if that component
exists)

for example, this is used for followpoints. if you specify `-x followpoints`,
then the skin's followpoints will no longer be used. however, the
`no-followpoints` component will be included with a blank image for
`followpoint.png` so that no followpoints appear at all, instead of using the
default skin's `followpoint.png`.

(this isn't implemented for all components)

### clean

add `--clean` or `-c` to automatically clean the directory before building again
(this will nuke everything inside the dir, so be careful!)

## making components

just add a folder and an entry to the `skin_components` list in `build.py`.

.psd files (and some other formats) are automatically excluded from being copied
when built, so feel free to leave those in

### `num` dir

this dir is special, it's copied as a subfolder into the skin folder as it uses
that for the score/combo numbers

### static components

some static files need to be copied as-is, like `skin.ini` and some other stuff
for artists credits. those are controlled by `static_components` in the script
