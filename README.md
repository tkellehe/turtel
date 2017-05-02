# Turtel

_Turtel_ is an esoteric programming language designed around ASCII art/animations through turtle graphics. It is designed to be used
for code golfing challenges and is currently under construction. This will hopefully out do my other language _Noodel_ in these types
of challenges. Although _Noodel_ did well, it would completely fail if there was any kind of complicated string manipulation needed.

You can visit the [wiki page](https://github.com/tkellehe/turtel/wiki) for more information.

## Compiling

_Turtel_ first gets translated into _Python_ which is then executed. This simplifies debugging more than anything. Now to simply run a
_Turtel_ script, use the following:

    turtel -e script.tel

This will translate the _Turtel_ script into _Python_ then executes the script. To pass in parameters it must be in a string array
object thing:)

    turtel -e script.tel "[100, 'string']"

If you need the _Python_ file generated use the `-p` option and specify the file to write it to:

    turtel -p script.tel script.py

Note that currently, the _Python_ file must be executed where it can have access to modules within _Turtel_.
