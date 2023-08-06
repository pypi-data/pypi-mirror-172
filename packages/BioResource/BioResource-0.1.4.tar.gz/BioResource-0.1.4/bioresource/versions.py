def get_versions():
    return versions[0]["number"]


versions = [
    {
        "number": "0.1.4",
        "features": [
            "1. Consider the case where the MD5 in NCBI does not match the file, but gzip can be decompressed;",
        ],
    },    {
        "number": "0.1.3",
        "features": [
            "1. debug;",
        ],
    },
    {
        "number": "0.1.2",
        "features": [
            "1. debug error caused by NA ftp_path;",
        ],
    },
    {
        "number": "0.1.1",
        "features": [
            "1. add ncbi_genome_chooser;",
        ],
    },
    {
        "number": "0.1.0",
        "features": [
            "1. ncbi genome source;",
        ],
    },
]