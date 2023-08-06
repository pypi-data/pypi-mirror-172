# Commandsheet: display catalog of commands user uses often

![image](commandsheet.png)

What does it do? Exactly what the title says! (Or maybe more like: display
catalog of commands you never remember how to use).

I came up with this project for one reason: there's always some of those
commands I never remember how to use.

Commandsheet to the rescue! With it, you can document the commands of your
liking (i.e. the commands you never know how to use) and what they do to a
config file, which Commandsheet then reads and prints nicely to the screen for
you. Nice and simple!

## Installation
Commandsheet is available in PyPi!
``` sh
python -m pip install commandsheet
```

## Usage
You should have a basic config file set up before you can use Commandsheet.
Check the next section to set up the config.

After setting up the config file, using Commandsheet is as easy as running:
``` sh
commandsheet
```

## Configuration
Below is an example config file for Commandsheet. Copy the contents, create the
file `~./config/commandsheet/commandsheet.ini` and paste the contents there.

The name between the brackets denotes the start of a section. The name can be
anything useful for you, for example '[my commands]'. To add entries under a
section, separate the key and value with a '=', where the key on the left of
the '=' is supposed to be a command or a command-sequence, and the value on
the right a description for that command / command-sequence.

``` ini
# commandsheet.ini

[ffmpeg]
ffmpeg -i input.mp4 output.avi = convert input.mp4 to output.avi

[zipfiles]
unzip filename.zip -d <dir> = unzip filename.zip to <dir>
zip archive.zip file1 file2 = zip files to archive.zip
zip -r archive.zip dir1 dir2 = zip dirs into archive.zip
zip -r archive.zip dir1 dir2 file1 file2 = zip dirs & files into archive.zip

[filesystem]
ls -l = list in long format
cp -v = copy and show what is happening

[networking]
ip a = show interface configuration
ping <address> = ping address <address>
```
