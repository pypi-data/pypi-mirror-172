# azcam-testers

*azcam-testers* is an *azcam* extension used for image sensor characterization. It provides acquisition and analysis programs to characterize sensor performace such as:

 - quantum efficiency
 - gain and read noise
 - charge transfer efficiency
 - photon transfer
 - dark signal
 - photo-response non-uniformity
 - extended pixel edge response
 - bias frame analysis
 - defect analysis
 - response calibration
 - linearity
 - metrology
 - superflats

## Documentation

See https://mplesser.github.io/azcam-testers/

## Installation

`pip install azcam-testers`

Or download from github: https://github.com/mplesser/azcam-testers.git.

## Usage Example

```python
qe.acquire()  # acquire QE image sequence 
qe.analyze()  # analyze the QE image sequence
```
