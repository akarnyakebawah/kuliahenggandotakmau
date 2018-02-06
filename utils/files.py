def get_extension(filename):
    return filename.split('.')[-1]


def s3_upload_path(top_level, second_level, name):
    return lambda instance, filename: "{}/{}/{}.{}".format(
        top_level,
        second_level,
        filename,
        get_extension(filename)
    )
