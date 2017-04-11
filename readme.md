# HOLOCLOUD PDF Conversion Pipeline

Asset Pipeline to be connected to the holocloud® and used to prepare pdf files
to be loaded at runtime in Unity Engine. This pipeline splits a pdf document
into its pages and outputs all of them as images (pngs). These images can then
be easily rendered in any 3D engine.

## Requirements

- **Python 2.7.12** (Python 2.7.13 got a bug with the bindings for ImageMagick)
- An ssh key with access rights to this repository on the machine you're 
  trying to run the FBX pipeline on
- ImageMagick installed on your system. Please check the instrcutions for your
  platform. E.g. for Windows, see [here](http://docs.wand-py.org/en/0.4.4/guide/install.html#install-imagemagick-on-windows)
- Ghostscript installed on your system (to open pdf files)
  See [here](https://ghostscript.com/download/gsdnld.html)

Alternatively, all this can be set up on a Linux platform, e.g. in a docker container.

## Setup

Use `virtualenv` to install all dependencies locally like so:

```sh
# create a new virtual environment in this folder
virtualenv venv
# activate the virtual environment
./venv/Scripts/activate.bat
# install the requirements locally using pip
pip install -U -r requirements.txt
```

## Usage

After having installed all the dependencies as lined out above, run the Unity fbx pipeline like:
(Don't forget to activate your virtual environment).  `config.ini` needs to contain all required
settings.

```
python command_line.py -c config.ini
```

### Configuration

The Unity fbx pipeline can be configured through a provided `config.yml` file. 
See [config.sample.ini](config.sample.ini) as an example.

The following options are available to you:
