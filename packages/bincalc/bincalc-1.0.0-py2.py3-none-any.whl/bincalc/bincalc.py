"""Main module."""

import sys
import re

from binary import convert_units, DecimalUnits, BinaryUnits


# *** DEFINITIONS ***
number_re = re.compile(r'([0-9.e]+)[ 	]*(.*)')   # Spaces in arguments are possible

unit_mapping = {
                 'KiB': BinaryUnits.KB,  # kibibyte
                 'MiB': BinaryUnits.MB,  # mebibyte
                 'GiB': BinaryUnits.GB,  # gibibyte
                 'TiB': BinaryUnits.TB,  # tebibyte
                 'PiB': BinaryUnits.PB,  # pebibyte
                 'EiB': BinaryUnits.EB,  # exbibyte
                 'ZiB': BinaryUnits.ZB,  # zebibyte
                 'YiB': BinaryUnits.YB,  # yobibyte
                 'B':   DecimalUnits.B,   # byte
                 'k':   DecimalUnits.KB,  # kilobyte
                 'K':   DecimalUnits.KB,  # kilobyte
                 'kB':  DecimalUnits.KB,  # kilobyte
                 'KB':  DecimalUnits.KB,  # kilobyte
                 'MB':  DecimalUnits.MB,  # megabyte
                 'M':   DecimalUnits.MB,  # megabyte
                 'GB':  DecimalUnits.GB,  # gigabyte
                 'G':   DecimalUnits.GB,  # gigabyte
                 'TB':  DecimalUnits.TB,  # terabyte
                 'T':   DecimalUnits.TB,  # terabyte
                 'PB':  DecimalUnits.PB,  # petabyte
                 'P':   DecimalUnits.PB,  # petabyte
                 'EB':  DecimalUnits.EB,  # exabyte
                 'E':   DecimalUnits.EB,  # exabyte
                 'ZB':  DecimalUnits.ZB,  # zettabyte
                 'Z':   DecimalUnits.ZB,  # zettabyte
                 'YB':  DecimalUnits.YB,  # yottabyte
                 'Y':   DecimalUnits.YB,  # yottabyte
               }


# *** FUNCTIONS ***
def unit_lookup(unit):
    try:
        return unit_mapping[unit]
    except KeyError:
        print("bincalc: ERROR: unrecognised unit: " + unit, file=sys.stderr)
        sys.exit(7)


# *** MAINLINE ***
def main():
    precision = 3
    num_args = len(sys.argv) - 1
    if num_args >= 1:
        to_unit = None
        used_args = 1  # This doesn't include the command name, i.e. arg 0
        m = number_re.match(sys.argv[used_args])
        if m:
            quantity = float(m.group(1))
            unit = DecimalUnits.B
            if m.group(2):
                unit = unit_lookup(m.group(2))
            else:
                # No match for the unit group means look at the next argument
                # (if any) for the unit, defaulting to bytes
                if num_args > used_args:
                    if not sys.argv[used_args+1] in ("in", "to"):
                        used_args += 1
                        unit = unit_lookup(sys.argv[used_args])
                        ## print(unit)

            if num_args > used_args:
                if sys.argv[used_args+1] in ("in", "to"):
                    if num_args - used_args == 2:
                        used_args += 2
                        to_unit = unit_lookup(sys.argv[used_args])
                    elif num_args - used_args < 2:
                        print("bincalc: ERROR: missing unit to convert to", file=sys.stderr)
                        sys.exit(4)
                else:
                    # A unit would have already been pulled out of the first
                    # argument or looked-ahead for
                    print("bincalc: ERROR: unrecognised argument", file=sys.stderr)
                    sys.exit(6)

            if num_args - used_args == 0:
                amount, output_unit = convert_units(quantity, unit=unit, to=to_unit)
                print("%.*f" % (precision, amount), output_unit)
            else:
                print("bincalc: ERROR: extra argument(s)", file=sys.stderr)
                sys.exit(5)
        else:
            print("bincalc: ERROR: invalid number", file=sys.stderr)
            sys.exit(2)
    else:
        # TO-DO: Read from stdin; use options instead of "in ...", provide option for input unit
        print("bincalc: ERROR: not enough arguments", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    """Not normally used; setup.py entry point calls main"""
    main()
