"""
    Pythius - Version Information

    All rights reserved, see LICENSE for details.

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    $Id: version.py,v 1.4 2002/07/08 04:09:35 ftobin Exp $
"""

project = "Pythius"
revision = '$Revision: 1.4 $'[11:-2]
release       = '0.3'

if __name__ == "__main__":
    # Bump own revision
    import os
    os.system('cvs ci -f -m "Bumped revision" version.py')
