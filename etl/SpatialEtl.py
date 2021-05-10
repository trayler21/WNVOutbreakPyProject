class SpatialEtl:
    """
    This class is written in order to define the Extract, Transform, and Load, or ETL,
    method to be used for the final project code.
    """

    def __init__(self, config_dict):
        """
        A configuration dictionary can be incredibly useful in programming. It allows use of a
        short-cut of sorts, rather than requiring the input of complex and often long paths.
        :param config_dict:
        """
        self.config_dict = config_dict

    def extract(self):
        """
        Extracting involves getting the data to be worked on from its original location in order to
        make it available for transforming, which occurs in the next step in this ETL process.
        :return:
        """
        print(f"Extracting data from {self.config_dict.get('remote_url')}"
              f" to {self.config_dict.get('proj_dir')}")

    def transform(self):
        """
        Transforming involves taking the extracted data and performing some supplementation or
        improvement to the code. Transformation allows you to specify or clarify rules specific to the
        prescribed task.
        :return:
        """
        print(f"Transforming {self.config_dict.get('remote_url')}"
              f" to {self.config_dict.get('proj_dir')}")

    def load(self):
        """
        Load involves determining the desired destination for the transformed data, namely, placing the
        data that was transformed into the location which is desired by the programmer or end user.
        :return:
        """
        print(f"Loading data into {self.config_dict.get('remote_url')}"
              f" to {self.config_dict.get('proj_dir')}")
