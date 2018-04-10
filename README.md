# Modeling a Snowflake's growth
This is a Python project for the university of Lille 1 
The program shall display a snowflake obtained via an algorithm. It will be able to either show the final output or the progressive growth of the crystal

The generation of a crystal depends on a number of parameters. And obviously, different parameters produce different outcomes.

## Prerequisites
You must have Python 3 (or newer) installed on your machine.
You also must install the imageio and Pillow libraries.
using pip you can just run this snippet of code in the terminal:
```
$pip install imageio
``` 
or
```
$python3 -m pip install imageio
``` 
(if you have multiple python version installed).

Note: Pillow should come installed with imageio

## Installation
Download [snowflake_growth.py](snowflake_growth.py) file either directly from the code or from the [release page](https://github.com/Saauan/modeling-snow-crystal-growth/releases/latest) and put it in a folder

## How To Use
You can run the script via the terminal of your machine using:
```
$python snowflake_growth.py
```
And it will automatically run the simulation using the defaults parameters.

When ran, the script will automatically create a folder whose name contains the parameters used for this simulation. Inside this folder, there will be an `hexa` and a `pixel` folder. In these folders, the script will save the states of the snowflake as it goes on. In hexa, the cells of the snowflake will be represented as hexagons whereas in pixel, they will be pixels.

### Using Parameters
You can put some parameters in the console to change the way the simulation will work. For instance, doing `$python snowflake_growth.py -h` will display the help for the script and the definitions of all parameters.

Doing `$python snowflake_growth.py -a 0.5 -b 0.8 -approximation 20` will run the simulation using 0.5 as Alpha, 0.8 as Beta and an approximation of 20

All help on the parameters can be found on the website linked to this repository and on the included help of the script

## Built With
* [Pillow](https://pillow.readthedocs.io/en/5.1.x/) - Used for saving images
* [imageio](https://imageio.github.io/) - Used for saving the animated gif

## Authors
* **Tristan Coignion** - [Saauan](https://github.com/Saauan)
* **Logan Becquembois** - [LianhuaB](https://github.com/LianhuaB)
* **Ajwad Tayebi** - [Ragyan](https://github.com/Ragyan)


## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
