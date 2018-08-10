# -*- coding: utf-8 -*-

import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

class ToDenseTransformer(BaseEstimator,TransformerMixin):
    # here you define the operation it should perform
    def transform(self, X, y=None, **fit_params):
        return X.todense()

    # just return self
    def fit(self, X, y=None, **fit_params):
        return self

class SelectColumnsTransfomer(BaseEstimator, TransformerMixin):
    """ Select dataframe columns
    """

    def __init__(self, columns=None, ravel=None):

        if columns is None:
            self.columns = []
        elif type(columns) is not list:
            self.columns = [columns]
        else:
            self.columns = columns

        if ravel is None:
            self.ravel = False
        else:
            self.ravel = ravel

    def transform(self, X, **transform_params):

        cpy_df = X[self.columns].copy()

        if self.ravel:
            return cpy_df.values.ravel()
        else:
            return cpy_df

    def fit(self, X, y=None, **fit_params):
        return self


class DataframeFunctionTransformer(BaseEstimator, TransformerMixin):
    """
    Apply an arbitrary function to a Dataframe column, as you would use a `map` funcion
    """

    def __init__(self, column_name, func, none_treatment=None):
        """

        :param column_name: the name of the dataframe column to which the function will be applied
        :param func: the function object, e.g. lambda
        :param none_treatment: what to do with NaN, Nones, etc. Default behaviour is to perform no
            special treatment, i.e. the function itself should treat nulls. Other options: 'return_none',
            returns the input itself in case it's null-lie (as per pd.isnull)
        """
        self.column_name = column_name
        self.func = func
        self.none_treatment = none_treatment

    def transform(self, in_df, **transform_params):
        cpy_df = in_df.copy()

        if self.column_name not in cpy_df.columns.values:
            raise ValueError('Provided column name is not part of the dataframe: "{}" '.format(self.column_name))

        if self.none_treatment is None:
            cpy_df[self.column_name] = cpy_df[self.column_name].map(self.func)
        elif self.none_treatment.upper() == "RETURN_NONE":
            cpy_df[self.column_name] = cpy_df[self.column_name].map(lambda x: x if pd.isnull(x) else self.func(x))
        else:
            raise ValueError(
                'Provided none treatment is invalid. Expected one of {}, got: '.format((None, 'return_none'),
                                                                                       self.none_treatment))

        return cpy_df

    def fit(self, X, y=None, **fit_params):
        return self
