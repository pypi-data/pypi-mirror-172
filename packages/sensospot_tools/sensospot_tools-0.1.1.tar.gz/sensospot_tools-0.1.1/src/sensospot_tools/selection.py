from typing import Any, Iterator

import pandas


def select(
    data: pandas.DataFrame, column: str, value: Any
) -> pandas.DataFrame:
    """Selects rows of a dataframe based on a value in a column

    Examples:
        >>> print(data)
          category  value
        0      dog      1
        1      cat      2
        2    horse      3
        3      cat      4
        >>> print(select(data, "category", "cat"))
          category  value
        1      cat      2
        3      cat      4


    Args:
        data:    a data DataFrame to select from
        column:  name of a column in a dataframe
        value:   rows with this value in the column will be selected

    Returns:
        a copy of the DataFrame that has the value in the column
    """
    selector = data[column] == value
    return data.loc[selector].copy()


def split(
    data: pandas.DataFrame, column: str
) -> Iterator[tuple[Any, pandas.DataFrame]]:
    """Splits a data frame on unique values in a column

    returns an iterator where each result is key-value-pair. The key is the
    unique value used for the split, the value is a slice of the dataframe
    selected by the unique value contained in the column

    Examples:

        >>> print(data)
          category  value
        0      dog      1
        1      cat      2
        2    horse      3
        3      cat      4
        >>> result = dict( split(data, column="category") )
        >>> print(result["dog"])
          category  value
        0      dog      1
        >>> print(result["cat"])
          category  value
        1      cat      2
        3      cat      4
        >>> print(result["horse"])
          category  value
        2    horse      3

    Args:
        data:   DataFrame to process
        column: column identifier to split on unique values
    Yields:
        key-value-pairs of one unique value of the column as key and the
            corresponding slice of the dataframe as value
    """
    unique_values = data[column].unique()
    return ((value, select(data, column, value)) for value in unique_values)
