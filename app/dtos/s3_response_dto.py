class S3UploadResponse:
    def __init__(self, key: str|None = None, public_url: str|None =None):
        self.key = key
        self.public_url = public_url