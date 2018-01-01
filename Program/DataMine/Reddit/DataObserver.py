# BOF

# Import necessary modules.
import pandas



class DataObserver:
    """
    The DataObserver class generates the data structures for appropriate observation and analysis.
    """





# noinspection PyCompatibility
def main():

    df = pandas.DataFrame()

    df = pandas.read_json(
        '/Users/admin/Documents/Work/AAIHC/AAIHC-Python/Program/DataMine/Reddit/json_data/DF-version_2/DF_v2.json')

    print(df.info())

    return 0





main()

# EOF