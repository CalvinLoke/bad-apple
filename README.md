# bad-apple
 Bad Apple printed out on the console with Python!

![Bad apple!!](bad_apple_gif.gif)

# Preface
A word of disclaimer, while the final code is somewhat original, this project is an amalgamation of different code snippets that I found online. As the main YouTube Video begins to gain traction, I feel the need to inform the audience that this code is NOT ENTIRELY ORIGINAL. 

The concept of playing Bad Apple!! on a Command Line Interface (CLI) is not a novel idea and I am definitely not the first. 

There are many iterations and versions around YouTube and I wanted to give it a shot. The intent of posting the video on YouTube was to show a few friends of a simple weekend project that I whipped up in Python. 

My own video can be found [here](https://www.youtube.com/watch?v=AZfrXrk3ZHc).

# Running this code/Pre-requisites
Thanks to [TheHusyin](https://github.com/TheHusyin) for adding a `requirements.txt` file for easier installs.

You can either `git clone` or download a ZIP of this repository. 

`git clone https://github.com/CalvinLoke/bad-apple`

Then, ensure that you set your terminal to the directory of this repository. 

`cd bad-apple`

Install the necessary dependencies and packages by using:

`pip install -r requirements.txt`

And to run the code:

`python touhou_bad_apple_v4.0.py`

And just follow the on-screen prompts. 

# Performance optimizations
Currently, my implementation of a rudimentary static `time.sleep()` function results in an incremental error over time. 
This thus leads to the frame accuracy drifting. 

**UPDATE on 22/04/21** 

With the replacement of the `playsound` library with `pygame`, the error over time seemed to have been fixed. Though, 
further improvements and optimizations to the code can still be done. As of current, performance is still not optimal.
A major bottleneck lies in the IOPS when dealing with the .txt files, am still trying to find a better implementation. 

I am also looking into improving frame extraction and generation times.

**UPDATE ON 23/04/21**

It seems that frame extraction is heavily bottle-necked by the drive's IOPS, and adding threads did not seem to expediate
frame extraction further. I have created some rudimentary code for process-based and threading-based frame extraction,
am looking to implement it for the ASCII generation soon. 

**UPDATE ON 25/04/21**

I got about to implementing multi-processing for both frame extraction and ASCII generation. Though it seems that my implementation of threading/processing is still very botchy and thus asset generation is still sub-optimal. Not too sure on how far I would want to take this project, though my main priority right now would be to adjust frame timings. 

**SECOND UPDATE ON 25/04/21**

Simply by replacing the primitive `time.sleep()` function with the `fpstimer` library, frame-time accuracy has been drastically improved, will be slowing down my code optimizations for playback from now onwards. 

Though the main concern right now is trying to optimize asset generation times. 

**THIRD UPDATE ON 25/04/21**

Changed the approach of storing assets. Should significantly reduce asset generation times, averaging arond 10 ~ 15 seconds using single thread. Will still look into threading to further expedite asset generation. However, with `touhou_bad_apple_v4.0.py`, progress will now slow down as I finally close the chapter of this project. 

**UPDATE ON 27/04/21**

It looks like most of the issues have been rectified, and the code has reached desirableh performance. While I could further boost ASCII generation and add new functionality to the code, I feel that it would be over-engineering such a simple project. What started out as a weekend project blew up to such proportions, and led me to learn many new and interesting concepts along the way. 

I really would like to thank [JasperTecHK](https://github.com/JasperTecHK) for his recommendations and suggestions along the way. His input was what really led me to return to this project after two dead weeks. 

As such, major updates to the code would come much slower now, as the current iteration of the project has far exceeded my orginal goal. Though, it would be interesting to further develop `v4.5` to have color support, but I would presume that requires its own development cycle. Once again, I really would like to thank all the contributors to this simple and dumb piece of code that I wrote in 24 hours. 

Cheers!

# Current known issues and bugs
Despite being a somewhat simple program, my crappy implementation has led to a lot of unresovled bugs and issues. I am currently
looking at fixing some of them. 

1) block=False is not supported in Linux (Only for v2.0 and below)

~~I am currently trying to find alternatives to the `playsound` library. Using two different threads is not an option currently as
I was running into desynchronization issues~~

This issue has been fixed in ~~v3~~ v2.5, alongside other performance improvements. 

2) No such file or directory: 'ExtractedFrames/BadApple_1.jpg' (Only for v3.0 and v2.5)

~~Not really sure how this is happening, but will be looking into fixing it. I was unable to replicate the error but I assume it is 
due to my botchy implementation of file directories for the assets~~

Issue could be due to host machine not having ffmpeg installed. Ensure that you have ffmpeg installed and run the script again. v4 and v4.5 will not return this error, though will need to do some limit testing to figure it out. 

# Version descriptor
1) touhou_bad_apple_v1.py

First rudimentary version that accomplishes basic frame extraction and animation. Utilizes threads, but suffers from heavy
synchronization issues.

2) touhou_bad_apple_v2.py 

Extended version that includes a "GUI", some basic file I/O. Suffers from slight synchronization issues. Core program 
logic was completed in 24 hours with some minor tweaks and comments afterwards. 

3) ~~touhou_bad_apple_v3.py~~ ==> Renamed to touhou_bad_apple_v2.5.py

~~Current development version. Improved frame time delay and better file I/O. Looking to implement threading to expedite frame extraction and ASCII conversion. Play-testing version to use py-game. Doesn't really warrant a full version increment, will be updating the name to v2.5 or something like that once the new v4 is ready~~

Slightly better version due to incorporation of `pygame` for music playing. Rectifies issue when attempting to play on Linux based environments since the older `playsound` library did not support `blocking=False` on said environments. 

Still has rudimentary frame extraction and ASCII generation on single thread/process, which makes asset generation significantly longer.

4) ~~touhou_bad_apple_v4.py~~ ==> Renamed to touhou_bad_apple_v3.0.py

~~(Almost) re-written as the previous code was getting to messy to work with. Functions from previous versions are still used though.~~

~~Will be renamed to v3 once I improve asset generation times with better threading code. However, "v4" is currently the most frame-accurate version thanks to the `fpstimer` library. And subsequent changes are only for smaller performance optimizations.~~

Rewritten to incorporate multiprocess, though implementation is very janky. Overall program structure was also refactored a bit to clean up `main()` function. Asset generation times were reduced a bit, but the double `for` loop meant that it generation times are close to a minute. 

5) ~~touhou_bad_apple_v4-5.py~~ ==> Renamed to touhou_bad_apple_v4.0.py

Once again my dumb naming schemes kick in again. After some toying around, I decided to scrap the .txt file generation
and skip right storing ASCII within memory. This version completely rewrites the asset generation algorithm. Instead of the old 

Video => Extracted_Images (stored in storage) => ASCII Characters (stored in memory) => .txt (stored in storage)

process, ASCII generation is done on the image stored within memory, so 

Video => Extracted_Images (stored in memory) => ASCII Characters (stored in memory) => Internal list (stored in memory)

Makes more sense as compared to older iterations and significantly cuts down asset generation times. 

While this means that 10 or 20 seconds is required for ASCII generation,
it eliminates storage IO bottleneck. Also frees up a lot of storage space on host system. Overall probably the best one yet? 


6) ~~touhou_bad_apple_v5.py~~ ==> Renamed to touhou_bad_apple_v4.5.py

Honestly I should not even get a job at file versioning. This version essentially allows the user to ASCII-fy any video
provided that they have the video file in the root directory. 
 


# Functions
The main functions will be listed here. 

## play_video()
Reads the files from the previously generated ASCII .txt files and prints it out onto the console. 

## play_audio()
Plays the bad apple audio track. 

## progress_bar(current, total, barLength=25)
A simple progress bar function that generates the status of both frame extraction and ASCII frame generation. 
This code was taken from a [StackOverflow thread](https://stackoverflow.com/questions/6169217/replace-console-output-in-python).

`current` is the current value/progress of the process. 

`total` is the desired/intended end value of the process.

`barLength=25` sets the length of the progress bar. (Default is 25 characters)

## ASCII Frame generation
Not a particular function, but a group of functions.

```
resize_image()

greyscale()

pixels_to_ascii()
```
These functions are called in the `ascii_generator()` function to convert image files to ASCII format and stores them into .txt files. 

Note that the ASCII conversion code is not original, and was taken from 
[here](https://github.com/kiteco/python-youtube-code/blob/master/ascii/ascii_convert.py).

# Words of acknowledgements
I should give credit where credit is due, and here is a section dedicated to that. 

ZUN, and this incredible work on the Touhou project over the past decades.

[Alstroemeria Records](https://www.youtube.com/channel/UCQ2uGVzfIbcqvZvrS0BVucw), 
for making the original [Bad Apple!! MV](https://www.youtube.com/watch?v=i41KoE0iMYU). 

[Ronald Macdonald](https://www.youtube.com/channel/UC3UIoTx99V9MQIkTh8ocUnQ), for making the 
[MIDI Arrangement](https://www.youtube.com/watch?v=ANRzDT1pU8c) of the Bad-Apple!! used.

GitHub users [karoush1](https://github.com/karoush1), [JasperTecHK](https://github.com/JasperTecHK), 
[TheHusyin](https://github.com/TheHusyin),  [Mirageofmage](https://github.com/Mirageofmage) for their
comments and bugfixes. 
 

 

