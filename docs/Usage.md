# Usage

1. Install through pip3.
    > At the moment, only `python ^3.6` is supported.  

    `pip3 install --user dynpaper`

2. Do one of the following:  
    *   Download one of the configuration files from [here](../sample_configs) to a folder  
    *   Do `dynpaper --init` or `dynpaper -i`.
        > A configuration file has been created in `$HOME/.config/dynpaper/config`

3. Modify the configuration file so it fits your usecase.

4. Run dynpaper:  
    `dynpaper -f <path to config> &`
    > If you want dynpaper to run in the beginning of the session, simply add the line above to your `.profile` or `.zsh_profile`.

## Configuration

Dynpaper reads a yaml formatted list. Each element in the list is a dictionary/mapping.  
The dictionary contains __2__ keys, `time` and `files`. The key `time` indicates the time this list of papers starts to show.  
The value for `time` is in this format: `HH:mm`. The value of `files` is a list of strings or dictionary objects.  
The string object is a __direct__ path to file.  
The dictionary is in this form:
```Yaml
    - template:
        path: ~/Pictures/Wallpapers/wallpaper{}.jpeg
        range: X, Y
```
Range indicates the numbers that will replace `{}` in the string, the numbers are in `[X,Y)`. After processing, the template with `range:13, 16 ` gets replaced by a generated list of files.  
In this case, the template is replaced by:
```Yaml
    ~/Pictures/Wallpapers/wallpaper13.jpeg
    ~/Pictures/Wallpapers/wallpaper14.jpeg
    ~/Pictures/Wallpapers/wallpaper15.jpeg
```
The generated files start from first element and go up to the last, excluding the last.  

