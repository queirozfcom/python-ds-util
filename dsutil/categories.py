import pandas as pd

from sklearn.base import TransformerMixin, BaseEstimator


class ToDummiesTransformer(BaseEstimator, TransformerMixin):
    """ Create dummies and drop the original column
    """

    def __init__(self, column_names=None, category_values=None):
        """

        :param column_names: list of column names to extract dummies for.
            if not given, all columns in the dataframe are used.

        :param category_values: a dict mapping column names to all possible values
            that categorical column can take. If not given, all values are used,
            in whatever order they appear in the dataframe.

        """

        if column_names is None:
            self.column_names = None
        elif type(column_names) is not list:
            self.column_names = [column_names]
        else:
            self.column_names = column_names

        if category_values is not None and (not isinstance(category_values, dict)):
            raise ValueError('category_values parameters must be None or a dict, got {}'.format(type(category_values)))
        else:
            self.category_values = category_values

    def transform(self, in_df):
        """

        :param in_df:
        :return:
        """

        if self.column_names is None:
            column_names = in_df.columns.values
        else:
            column_names = self.column_names

        if self.category_values is None:
            cpy_df = in_df.copy()
        else:
            # user has provided category values so we must set those
            cpy_df = in_df.copy()

            for column_name in self.column_names:

                # maybe not all column_names have been set values
                if self.category_values.get(column_name, None) is not None:

                    provided_category_values = self.category_values[column_name]
                    cpy_df[column_name] = cpy_df[column_name].astype(
                        pd.api.types.CategoricalDtype(provided_category_values))
                else:
                    # user hasn't provided values, maybe the column is already category type?
                    if isinstance(cpy_df[column_name].type, pd.api.types.CategoricalDtype):
                        pass  # then leave it alone
                    else:
                        cpy_df[column_name] = cpy_df[column_name].astype(pd.api.types.CategoricalDtype())

        # after all columns have been properly converted to categorical types, do the actual conversions
        for column_name in column_names:
            cpy_df = pd.concat([cpy_df, pd.get_dummies(cpy_df[column_name], prefix=column_name, dummy_na=True)], axis=1)
            cpy_df.drop([column_name], axis=1, inplace=True)

        return cpy_df

    def fit(self, X, y=None, **fitparams):
        return self
