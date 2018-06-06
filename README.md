A European long-term combined investment and dispatch model: elesplan-m. It reflects the model that was used in my dissertation and
 is built with oemof.
 
 # Installation
 
 It's recommended to use a virtual environment!
 
```
pip3 install elesplan_m_EMP_E_2018 --process-dependency-links
```

# Use it

Download data for a specific [scenario](https://cloud.rl-institut.de/index.php/s/vvHNXc0IsW2clwz/download) (click the link to download).

Unzip data to your favorite location, let's call is <data-folder>.

A command-line is installed by pip. Pass the <data-folder> as argument

```
elesplan_m <data-folder>
```
