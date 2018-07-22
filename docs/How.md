# How

The script uses the schema library to validate the configuration file, during the validation, the script checks if the files exist in the specified locations. This is done only __once__ at every initialization of the script, if a file does not exist during the initialization, the script will exit, raising an error. If a file is removed after the initialization, the outcome depends on the Window manager that's being used.

Then the script creates a list of files and the time each will wallpaper will change to the next.

To set the wallpaper, the script uses part of 'WeatherDesk' module, written by Bharadwaj Raju <bharadwaj.raju777@gmail.com>.
