# Voltage Proccessor
### Made by Sai Sursala & updated by Conor Sheridan
Used for 4 polarization voltages aquired from I-LOFAR in *.zst compression format. Produces intermediary uncompressed .dada file that is usually x4 times the size of all four .zst files (in the same directory as the 4pol script!!), then converts that to a filterbank file (deleting the dada file automatically when finished)

For help run _bash 4pol_generate.sh -h_

To Do:
* Add output flag so you don't accidentally zip-bomb your home directory
