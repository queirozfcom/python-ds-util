import pandas as pd

from sklearn.base import TransformerMixin, BaseEstimator


class ToDummiesTransformer(BaseEstimator, TransformerMixin):
    """ Create dummies and drop the original column
    """

    def __init__(self, columns=None):

        if columns is None:
            pass
        elif type(columns) is not list:
            columns = [columns]
            
        self.columns = columns

    def transform(self, in_df, columns=None):
        """

        :param in_df:
        :param columns:
        :return:
        """


        if self.columns is None:
            columns = in_df.columns.values
        else:
            columns = self.columns

        cpy_df = in_df.copy()

        for column_name in columns:
            cpy_df = pd.concat([cpy_df, pd.get_dummies(cpy_df[column_name], prefix=column_name)], axis=1)
            cpy_df.drop([column_name], axis=1, inplace=True)

        return cpy_df

    def fit(self, X, y=None, **fitparams):
        return self


class SelectColumnsTransfomer(BaseEstimator, TransformerMixin):
    """ Select dataframe columns
    """

    def __init__(self, columns=None):

        if type(columns) is not list:
            columns = [columns]
        elif columns is None:
            columns = []

        self.columns = columns

    def transform(self, X, **transform_params):
        cpy_df = X[self.columns].copy()
        return cpy_df

    def fit(self, X, y=None, **fit_params):
        return self
