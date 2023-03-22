# FundiScintTutorial2023

To start with, use psrflux to get the dynamic spectrum from a pulsar archive: eg.  psrflux archivename.ar

If you just want to take a quick look at a pulsar's dynamic spectrum, one can do this simply with psrplot: eg.  psrplot -pj -D /xw archivename.ar

The main tutorial notebook goes through the steps of inspecting dynamic spectra, and deriving timescales, bandwidths, and arc curvatures.  Some handy functions are found in dynspectools.py - as shown in the tutorial notebook, with these functions one can write a very simple, general script to run on any archive or dynspec without the intermediate steps

Some handy background, and other useful packages are:

https://screens.readthedocs.io/en/latest/

https://github.com/danielreardon/scintools
