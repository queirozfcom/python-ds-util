# -*- coding: utf-8 -*-

import pandas as pd


def encode_categorical_columns(in_df, categorical_column_names):
    out_df = in_df.copy()

    for col_name in categorical_column_names:
        column = out_df[col_name].astype(pd.api.types.CategoricalDtype())
        out_df = pd.concat([out_df, pd.get_dummies(column, prefix=col_name, dummy_na=True)], axis=1).drop([col_name],
                                                                                                          axis=1)

    return out_df
