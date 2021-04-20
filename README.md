# bad-apple
 Bad Apple printed out on the console with Python!

# Preface
A word of disclaimer, while the final code is somewhat original, this project is an amalgamation of different code snippets that I found online. As the main YouTube Video begins to gain traction, I feel the need to inform the audience that this code is NOT ENTIRELY ORIGINAL. 

The concept of playing Bad Apple!! on a Command Line Interface (CLI) is not a novel idea and I am definitely not the first. 

There are many iterations and versions around YouTube and I wanted to give it a shot. The intent of posting the video on YouTube was to show a few friends of a simple weekend project that I whipped up in Python. 

My own video can be found [here](https://www.youtube.com/watch?v=AZfrXrk3ZHc).

# Running this code
With 20th April 2021's revision, I have added a virtual environment with the required packages and dependencies. 

First, ensure that you set your terminal to the directory of this repository. 

`cd bad-apple`

Activate the virtual environment by running:

`.\venv\Scripts\activate`

And to run the code:

`python touhou_bad_apple_v2.py`

And just follow the on-screen prompts. 

# Performance optimizations
Currently, my implementation of a rudimentary static `time.sleep()` function results in an incremental error over time. This thus leads to the frame accucracy drifting. 

I am also looking into improving frame extraction and generation times.

# Current known issues and bugs
Despite being a somewhat simple program, my crappy implementation has led to a lot of unresovled bugs and issues. I am currently
looking at fixing some of them. 

1) block=False is not supported in Linux
I am currently trying to find alternatives to the `playsound` library. Using two different threads is not an option currently as
I was running into desynchronization issues.

2) No such file or directory: 'ExtractedFrames/BadApple_1.jpg'
Not really sure how this is happening, but will be looking into fixing it. I was unable to replicate the error but I assume it is 
due to my botchy implementation of file directories for the assets. 

# Functions
The main functions will be listed here. 

## play_video()
Reads the files from the previously generated ASCII .txt files and prints it out onto the console. 

## play_audio()
Plays the bad apple audio track. 

## Progress bar function
A simple progress bar function that generates the status of both frame extraction and ASCII frame generation. This code was taken from a [StackOverflow thread](https://stackoverflow.com/questions/6169217/replace-console-output-in-python).

## ASCII Frame generation
Not a particular function, but a group of functions.

```
resize_image()

greyscale()

pixels_to_ascii()
```
These functions are called in the `ascii_generator()` function to convert image files to ASCII format and stores them into .txt files. 

Note that the ASCII conversion code is not original, and was taken from [here](https://github.com/kiteco/python-youtube-code/blob/master/ascii/ascii_convert.py).
 

