# This file is part of eltuxusb.
#
# eltuxusb is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# eltuxusb is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with eltuxusb.  If not, see <http://www.gnu.org/licenses/>.

from distutils.core import setup
setup(name='eltuxusb',
      version='dev',
      author = 'Romain Aviolat',
      author_email = 'r.aviolat@gmail.com',
      maintainer = 'David Strauss',
      maintainer_email = 'david@davidstrauss.net',
      url = 'http://github.com/eltuxusb/eltuxusb',
      install_requires = ['matplotlib', 'pyusb'],
      packages = ['eltuxusb'],
      scripts = ['eltuxusb/eltuxusb'],
      data_files = [('/etc/udev/rules.d/', ['10-local.rules'])],
      package_data = {'eltuxusb': ['*.glade', '*.png']}
      )
