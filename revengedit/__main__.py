#!/usr/bin/env python3
"""
  Copyright (c) 2022 Shambles_SM

  Permission is hereby granted, free of charge, to any person obtaining
  a copy of this software and associated documentation files (the
  "Software"), to deal in the Software without restriction, including
  without limitation the rights to use, copy, modify, merge, publish,
  distribute, sublicense, and/or sell copies of the Software, and to
  permit persons to whom the Software is furnished to do so, subject to
  the following conditions:

  The above copyright notice and this permission notice shall be
  included in all copies or substantial portions of the Software.

  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
  CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
  TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
  SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import os, argparse, re
from revengedit.value_routines import arg_bool, view_values, edit_values

helpDescription = """
View (or edit) a Zuma's Revenge! *.dat file level settings, such as amount
of ball colors, chances of same-colored balls or speed of balls.
"""

editHelpDescription = """
Both value-taking and boolean properties will require a value to be passed to.
If a property is not defined (i.e. None), it will not be modified.
Examples: `--score 1280`, `--speed 0.8`, `--dieatend True`, `--showskull 0`
"""

def main():
    parser = argparse.ArgumentParser(prog="revengedit",
                                 description=helpDescription,
                                 formatter_class=argparse.RawDescriptionHelpFormatter,)
    subparsers = parser.add_subparsers(help='sub-command help')

    parser_view = subparsers.add_parser('view')
    parser_view.add_argument('file', type=str, help="path to a *.dat file")
    parser_view.set_defaults(func=view_values)
    
    parser_edit = subparsers.add_parser('edit', description=editHelpDescription,
                                 formatter_class=argparse.RawDescriptionHelpFormatter,)
    parser_edit.add_argument('file', type=str, help="path to a *.dat file")
    parser_edit.set_defaults(func=edit_values)

    parser_edit.add_argument('--start', type=int, metavar='<int>', help="Where the balls arrive after the path sparkles")
    parser_edit.add_argument('--repeat', type=int, metavar='<int>', help="Chance of next ball being the same color as the previous one")
    parser_edit.add_argument('--single', type=int, metavar='<int>', help="Chance of ball being a single, independent of `repeat`")
    parser_edit.add_argument('--colors', type=int, metavar='<int>', help="""How much colors the level should have; minimum of 3 or
                                                        the game crashes, maximum of 6 before the game reads "colors"
                                                        from other directories other than `balls`""")
    parser_edit.add_argument('--speed', type=float, metavar='<float>', help="How fast the balls normally are")
    parser_edit.add_argument('--score', type=int, metavar='<int>', help="The amount of points the player has to reach in order to fill the Zuma bar")
    parser_edit.add_argument('--destroyallDisabled', metavar='<bool>', type=arg_bool, help="""If any remaining balls shouldn't be destroyed
                                                                    after the Zuma bar has been filled up""")
    parser_edit.add_argument('--showskull', metavar='<bool>', type=arg_bool, help="If the skull should be shown at the end of the path")
    parser_edit.add_argument('--dieatend', metavar='<bool>', type=arg_bool, help="""If set to `00`, any balls that enter the skull will not
                                                              trigger a level fail. Instead, the ball will be destroyed
                                                              (no points). The warning skulls will also not show up
	                                                            when the balls enter the danger zone.""")
    parser_edit.add_argument('--crashonload', metavar='<bool>', type=arg_bool, help="Don't enable this.")

    args = parser.parse_args()
    if ("func" in args) == False:
        parser.parse_args(["-h"])
    args.func(args)

if __name__ == '__main__':
    main()