A European long-term combined investment and dispatch model: elesplan-m. It reflects the model that was used in my dissertation and
 is built with oemof.
 
 # Installation
 
 It's recommended to use a virtual environment!
 
 Clone the repo
 ```
 git clone git@github.com:gplssm/elesplan_m_EMP-2018.git
 ```
 and install from local files
 
```
pip3 install <path-to-repo> --process-dependency-links
```

# Use it

Download data for a specific [scenario](https://github.com/gplssm/elesplan-m_EMP-2108/wiki/Scenarios).

Unzip data to your favorite location, let's call is `<data-folder>`.

A command-line is installed by pip. Pass the `<data-folder>` as argument

```
elesplan_m <data-folder>
```

# License

Copyright (C) 2018  @gplssm

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version. 

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License along with this program. If not, see <http://www.gnu.org/licenses/>.
