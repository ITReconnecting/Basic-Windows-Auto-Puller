# Basic Windows Auto Puller
A python program to pull information from a raw (dd) Windows forensics image. The program automates gathering information on an image, collating this information and then pulling information from the image in a way that does not tamper with the contents. It will produce:
- A list of sha256 hashes for each partition on the image
- The recovered files that were deleted and in the recycling bin (hash list for these aswell_
- A html file of all images recovered that were deleted
- A main report file of the basic information gathered
- A command history
