from __future__ import print_function, division

import os
import shutil
from os import path

import requests
from asset_pipeline import BaseRemoteAssetPipeline, AbstractAssetPipeline
from asset_pipeline import logger
from wand.image import Image

TMP_FILES_PATH = path.abspath(
    path.join(
        path.dirname(path.realpath(__file__)),
        'tmp'
    )
)


class PdfAssetPipelineMixin(object):
    """
    Mixin for asset pipelines working fbx files
    """
    supported_filetypes = ['.pdf']


class PdfAssetPipeline(PdfAssetPipelineMixin, AbstractAssetPipeline):
    # pdf page resolution
    resolution = 256
    # pdf dots per inch (when reading in pdf)
    dpi = 100

    def __init__(self, config=None, *args, **kwargs):
        # call parent logic
        super(PdfAssetPipeline, self).__init__(config=config, *args, **kwargs)
        # store dpi and resolution configuration
        if 'dpi' in config:
            self.dpi = int(config['dpi'])
        if 'resolution' in config:
            self.resolution = int(config['resolution'])

    def validate_configuration(self, config):
        # check that the resolution is sane
        if 'resolution' not in config:
            logger.error("Please provide an image resolution for the output")
            return False
        if 'dpi' not in config:
            logger.error("Please provide a scanning resolution for the input pdf (dpi)")
            return False
        # if we got here, everything's fine
        return True

    def execute(self, asset_data):
        # convert posix path to whatever system we're on
        input_path = asset_data.get('input', {}).get('path', None)
        logger.info('now starting conversion progress for file {}'.format(input_path))
        images = self.split_pdf_into_images(input_path)
        logger.info('converted to {}'.format(images))
        # enrichen the asset data with the conversion result
        asset_data['images'] = images

    def split_pdf_into_images(self, input_file):
        # make sure the file exists
        if not path.isfile(input_file):
            raise Exception("Provided pdf file does not exist")
        # 0. clean the staging area
        if path.exists(TMP_FILES_PATH):
            shutil.rmtree(TMP_FILES_PATH)
        os.makedirs(TMP_FILES_PATH)
        # 1. copy the pdf into the staging area
        copy_dst = os.path.join(TMP_FILES_PATH, os.path.basename(input_file))
        shutil.copy(input_file, copy_dst)
        filename = os.path.splitext(os.path.basename(copy_dst))[0]
        # filename of the converted images
        conv_dst = os.path.join(TMP_FILES_PATH, "%s" % filename)
        # 2. run the conversion script
        result = []
        with Image() as dst_image:
            with Image(filename=copy_dst, resolution=self.dpi) as src_image:
                for frame in src_image.sequence:
                    # disable alpha before resizing, else we got problems
                    frame.alpha_channel = False
                    # get the current size of the image
                    size = frame.size
                    # calculate the new size based on the max resolution (in x / y direction)
                    new_size = (int(size[0] * (self.resolution / size[1])), self.resolution)
                    if size[0] >= size[1]:
                        new_size = (self.resolution, int(size[1] * (self.resolution / size[0])))
                    # resample.
                    frame.resize(*new_size)
                    dst_image.sequence.append(frame)
                # operations to a jpeg image...
                dst_image.save(filename='{0}.{1}'.format(conv_dst, 'jpg'))
                if len(src_image.sequence) > 1:
                    result = ['{0}-{1.index}.{2}'.format(conv_dst, x, 'jpg') for x in src_image.sequence]
                else:
                    result = ['{0}.{1}'.format(conv_dst, 'jpg')]
        # 3. return the list of images
        return result


class PdfRemoteAssetPipeline(PdfAssetPipeline, BaseRemoteAssetPipeline):
    def post_execute(self, asset_data):
        logger.info("Now uploading converted images for pdf {}".format(asset_data['images']))
        self.upload_conversion_result(asset_data)

    def upload_conversion_result(self, asset_data):
        """
        uploads the converted model back to the holocloud
        :param asset_data: all the working data about the asset
        :return:
        """
        url = '{proto}://{host}:{port}/{path}/'.format(proto=self.protocol, host=self.host,
                                                       port=self.port,
                                                       path='api/pdf-pages')
        for idx, image_path in enumerate(asset_data['images']):
            logger.info('Uploading image to %s' % url)
            # attach the conversion result as a file to the post request
            # also set the state to finished
            payload = {
                'image': open(image_path, 'rb'),
                # the empty string in the tuple will prevent of setting a filename for this non file value
                # see https://stackoverflow.com/questions/12385179/how-to-send-a-multipart-form-data-with-requests-in-python
                'parent': ('', str(asset_data.get('id'))),
                'pos': ('', str(idx + 1))
            }
            response = requests.request("POST", url, files=payload)
            # if we get an error, show it.
            response.raise_for_status()
