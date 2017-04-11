import ConfigParser
from os import path
from unittest import TestCase

from nose.tools import raises, nottest
from wand.image import Image

from pdf_pipeline import PdfAssetPipeline


def get_config(config_name='test_config.ini'):
    config = ConfigParser.SafeConfigParser()
    config.read([path.join(
        path.dirname(path.realpath(__file__)),
        'input',
        config_name
    )])
    # store all values of the config file
    return dict(config.items("Pdf"))


class TestPdfPipeline(TestCase):
    @raises(AttributeError)
    def test_is_validating_configuration(self):
        config = {}
        pipeline = PdfAssetPipeline(config)

    def test_is_converting_pdf(self):
        config = get_config()
        pipeline = PdfAssetPipeline(config)
        conversion_result = pipeline.split_pdf_into_images(
            path.join(path.dirname(path.realpath(__file__)), 'input', 'pdf-sample.pdf'))
        assert len(conversion_result) == 1
        with Image(filename=conversion_result[0]) as converted:
            assert max(converted.size) == int(config['resolution'])

    def test_is_converting_multipage_pdf(self):
        config = get_config()
        pipeline = PdfAssetPipeline(config)
        conversion_result = pipeline.split_pdf_into_images(
            path.join(path.dirname(path.realpath(__file__)), 'input', 'pdf-multipage-sample.pdf'))
        assert len(conversion_result) == 3
        for conv_res in conversion_result:
            with Image(filename=conv_res) as converted:
                assert max(converted.size) == int(config['resolution'])

    def test_is_converting_highquality_pdf(self):
        config = get_config('test_config_high.ini')
        pipeline = PdfAssetPipeline(config)
        conversion_result = pipeline.split_pdf_into_images(
            path.join(path.dirname(path.realpath(__file__)), 'input', 'pdf-highquality-sample.pdf'))
        for conv_res in conversion_result:
            with Image(filename=conv_res) as converted:
                assert max(converted.size) == int(config['resolution'])
