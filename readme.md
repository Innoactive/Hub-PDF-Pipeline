# HOLOCLOUD PDF Conversion Pipeline

Asset Pipeline to be connected to the holocloud® and used to prepare pdf files
to be loaded at runtime in Unity Engine. This pipeline splits a pdf document
into its pages and outputs all of them as images (jpgs). These images can then
be easily rendered in any 3D engine.

## Requirements

### Windows

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

After having installed all the dependencies as lined out above, run the pdf pipeline like:
(Don't forget to activate your virtual environment; `config.ini` needs to contain all required
settings.

```
python command_line.py -c config.ini
```


### Usage inside a docker container

This container can be run together with the Innoactive Hub's containers after building it 
using `docker build . -t hub_pdf_pipeline`.When building make sure to have access to the 
following repository: [Hub-Base-Asset-Pipeline](https://github.com/Innoactive/Hub-Base-Asset-Pipeline.git). 
If anonymous access is not granted, you'll have to build the image without pip installing the
requirements, then run the image once (using `docker run -it --name hub_pdf_pipeline-container hub_pdf_pipeline ash`)
, manually install the dependencies, providing credentials when prompted and tag 
the modified container as the actual image (using `docker commit hub_pdf_pipeline-container hub_pdf_pipeline`) in the end.

Afterwards, it can be e.g. run like the following:

```
docker run --rm --net backend_default --name hub_pdf_pipeline-run hub_pdf_pipeline python command_line.py -c config.ini -H hub_channels
```

Sample SystemD task taking care of starting the pdf pipeline automatically: 

```
[Unit]
Description=InnoactiveHub Pdf Pipeline Converter Service
After=innoactivehub.service
Requires=innoactivehub.service

[Service]
ExecStart=-/usr/local/bin/docker run --rm --net backend_default --name hub_pdf_pipeline-run hub_pdf_pipeline python command_line.py -c config.ini -H hub_channels
ExecStop=-/usr/local/bin/docker stop hub-pdf-pipeline

[Install]
WantedBy=multi-user.target
```


### Configuration

The pdf pipeline can be configured through a provided `config.ini` file. 
See [config.sample.ini](config.sample.ini) as an example.

The following options are available to you:

#### `[Pdf]`

All pdf pipeline specific settings go into the **[Pdf]** section of the configuration file.

##### `resolution`

The maximum number of pixels a resulting image of a page within the pdf should have in the end.

E.g. if this value is `1024`, the resulting images will be resized to have a maximum width (or height)
of 1024px. Resizing to match this condition will not transform the page in any way. Scaling will
be uniform.

##### `dpi`

*dots per inch* resolution when reading in the original pdf file. The higher this value is, the
better the results. However, increasing this value will also increase the time the conversion takes.

A reasonable value will be around 300.
