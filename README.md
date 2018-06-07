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
