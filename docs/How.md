# How

The script uses the schema library to validate the configuration file, during the validation, the script checks if the files exist in the specified locations. This is done only __once__ at every initialization of the script, if a file does not exist during the initialization, the script will exit, raising an error. If a file is removed after the initialization, the outcome depends on the Window manager that's being used.

Then the script creates a list of files and the datetime until the wallpaper gets replaced by the next.

To set the wallpaper, the script uses part of [WeatherDesk](https://github.com/bharadwaj-raju/WeatherDesk) module, written by [Bharadwaj Raju](github.com/bharadwaj-raju) <bharadwaj.raju777@gmail.com>.

Through Bharadwaj's [desktop](/dynpaper/desktop.py) script, all of the following configurations are available:

## Linux

* AfterStep
* Awesome WM
* Blackbox
* Cinnamon
* Enlightenment
* Fluxbox
* Gnome 2
* Gnome 3
* i3
* IceWM
* JWM
* KDE
* LXDE
* LXQt
* Mate
* Openbox
* Pantheon
* Razor-Qt
* Trinity
* Unity
* Windowmaker
* XFCE
