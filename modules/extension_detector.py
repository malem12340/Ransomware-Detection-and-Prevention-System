class ExtensionDetector:

    SUSPICIOUS_EXTENSIONS = [

        ".locked",

        ".encrypted",

        ".crypt",

        ".ryk",

        ".wncry",

        ".locky",

        ".cerber"

    ]

    def is_suspicious(self, filename):

        filename = filename.lower()

        for extension in self.SUSPICIOUS_EXTENSIONS:

            if filename.endswith(extension):

                return True

        return False