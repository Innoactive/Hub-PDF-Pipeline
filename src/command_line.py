import asset_pipeline.arguments as arguments
from pdf_pipeline import PdfRemoteAssetPipeline


def main():
    # parse all available configuration information
    config = arguments.parse()
    # create new RemoteAssetPipeline instance
    # and connect to socket.io server
    asset_pipeline = PdfRemoteAssetPipeline(
        config=config
    )
    asset_pipeline.start()


if __name__ == "__main__":
    main()
