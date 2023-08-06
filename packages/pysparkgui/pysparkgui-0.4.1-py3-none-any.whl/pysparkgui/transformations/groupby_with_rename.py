# Copyright (c) Databricks Inc.
# Distributed under the terms of the DB License (see https://databricks.com/db-license-source
# for more information).

import ipywidgets as widgets

from pysparkgui.helper import (
    Transformation,
    list_to_string,
    DF_OLD,
    DF_NEW,
    PysparkguiError,
    string_to_code,
)

from pysparkgui.widgets import Multiselect, Singleselect, Text

from pysparkgui.transformations.base_components import (
    SelectorGroupMixin,
    SelectorMixin,
    SingleColumnSelector,
)

AGGREGATION_OPTIONS = [
    ("Count", "count"),
    ("Count distinct values", "countDistinct"),
    ("Sum", "sum"),
    ("Mean/Average", "mean"),
    ("Min", "min"),
    ("Max", "max"),
    ("First value", "first"),
    ("Last value", "last"),
    # ("Count (size)", "size"),  # with missing values
    # ("Count (excl. missings)", "count"),

    # ("Median", "median"),
    # distribution metrics
    # ("Standard deviation - std", "std"),
    # ("Variance", "var"),
    # ("Standard error of the mean - sem", "sem"),
    # ("Mean absolute deviation - mad", "mad"),
    # ("Skew", "skew"),
    # ("Group number - 0 to n", "ngroup"),
    # ("All (boolean operator)", "all"),
    # ("Any (boolean operator)", "any"),
    # ("Index of max value", "idxmax"),
    # ("Index of min value", "idxmin"),
    # ("Product of all values", "prod"),
]

class AggregationSelector(SelectorMixin, widgets.HBox):
    """
    Manages one (<column to aggregate>, <aggregation function>, <new column name>) group plus the
    delete button to remove itself.
    """

    def __init__(self, df_columns, show_delete_button=True, **kwargs):
        super().__init__(show_delete_button=show_delete_button, **kwargs)

        self.aggregation_dropdown = Singleselect(
            options=AGGREGATION_OPTIONS,
            focus_after_init=show_delete_button,
            placeholder="Choose aggregation",
            set_soft_value=True,
            width="sm",
        )

        self.column_dropdown = SingleColumnSelector(options=df_columns, width="md")

        self.new_column_name = Text(
            placeholder="Column name (optional)",
            execute=self.selector_group,
            width="md",
        )

        self.children = [
            self.aggregation_dropdown,
            widgets.VBox(
                [
                    widgets.HBox([widgets.HTML(" of "), self.column_dropdown]),
                    widgets.HBox([widgets.HTML("as"), self.new_column_name]),
                ]
            ),
            self.delete_selector_button,
        ]

    def has_valid_value(self):
        column_is_missing = not self.column_dropdown.value
        aggregation_function_is_missing = not self.aggregation_dropdown.value
        if column_is_missing:
            raise PysparkguiError(
                """You didn't specify a <b>column</b> what you want to aggregate.
                Please select a column to aggregate."""
            )
        elif aggregation_function_is_missing:
            raise PysparkguiError(
                """You didn't specify an <b>aggregation function</b> (e.g. sum or mean)
                for your column(s)."""
            )
        else:
            return True

    def get_aggregation_code(self):
        # e.g. f.sum("n").alias("n_sum")
        aggregation = self.aggregation_dropdown.value
        column = self.column_dropdown.value

        code = f"f.{aggregation}({string_to_code(column)})"
        
        new_column_name = self.new_column_name.value
        if new_column_name:
            code += f".alias({string_to_code(new_column_name)})"
        return code

    # def test_select_aggregation_functions(
    #     self, aggregation_function: str, column_name: str, new_column_name: str
    # ):
    #     self.aggregation_dropdown.value = aggregation_function
    #     self.column_dropdown.value = column_name
    #     self.new_column_name.value = new_column_name


class AggregationSection(SelectorGroupMixin, widgets.VBox):
    """Manages a group of `AggregationSelector`s."""

    def __init__(self, transformation):
        super().__init__()
        self.transformation = transformation
        self.df_columns = list(self.transformation.get_df().columns)

        self.init_selector_group("add calculation")

        self.children = [
            widgets.HTML("<h4>and Calculate</h4>"),
            self.selector_group,
            self.add_selector_button,
        ]

    def create_selector(self, show_delete_button=None, **kwargs):
        return AggregationSelector(
            self.df_columns, selector_group=self, show_delete_button=show_delete_button
        )

    def get_aggregation_code(self):
        return ", ".join([selector.get_aggregation_code() for selector in self.get_selectors() if selector.has_valid_value()])

    def execute(self):
        self.transformation.execute()

    # def test_select_aggregation_functions(
    #     self, aggregation_function: str, column_name: str, new_column_name: str
    # ):
    #     self.get_selectors()[-1].test_select_aggregation_functions(
    #         aggregation_function, column_name, new_column_name
    #     )


class SparkGroupbyWithRename(Transformation):
    """
    Group rows by columns and calculate a SINGLE aggregation that can be named.

    Manages the whole transformation.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.groupby_columns = Multiselect(
            options=list(self.get_df().columns),
            placeholder="Choose column(s)",
            focus_after_init=True,
            width="lg",
        )

        self.aggregation_section = AggregationSection(self)

        self.merge_result = Singleselect(
            placeholder="Choose style",
            options=[("New Table", False), ("New Columns", True)],
            set_soft_value=True,
            width="md",
        )

    def render(self):
        self.set_title("Group by with column rename")
        self.set_content(
            widgets.VBox(
                [
                    widgets.HTML("<h4>Group By</h4>"),
                    self.groupby_columns,
                    widgets.HTML("<br>"),
                    self.aggregation_section,
                    widgets.HTML("and store result as"),
                    self.merge_result,
                    self.rename_df_group,
                ]
            )
        )

    def get_description(self):
        columns_list = list_to_string(self.groupby_columns.value, quoted=False)
        description = (
            f"<b>Group by</b> {columns_list} <b>and calculate new column(s)</b>"
        )

        if self.merge_result.value:
            description = f"<b>Add new column(s)</b> based on {description}"
        return description

    def is_valid_transformation(self):
        if len(self.groupby_columns.value) == 0:
            raise PysparkguiError(
                "You did not select any columns to group by.<br>Please select some groupby column(s)"
            )
        return True

    def get_code(self):
        aggregations_code = self.aggregation_section.get_aggregation_code()
        groupby_df = f"{DF_OLD}.groupby({self.groupby_columns.value}).agg({aggregations_code})"

        if self.merge_result.value:
            return f"""{DF_NEW} = {DF_OLD}.join({groupby_df}, on={self.groupby_columns.value}, how='left')"""
        else:
            return f"""{DF_NEW} = {groupby_df}"""

    def get_pyspark_chain_code(self):
        if self.merge_result.value:
            return None  # this statement cannot be expressed in chain style as far as Flo knows as of 2022-10-20
        else:
            aggregations_code = self.aggregation_section.get_aggregation_code()
            return f".groupby({self.groupby_columns.value}).agg({aggregations_code})"

    # def get_metainfos(self):
    #     return {
    #         "groupby_type": self.merge_result.label,
    #         "groupby_columns_count": len(self.groupby_columns.value),
    #     }

    # def reset_preview_columns_selection(self):
    #     if self.merge_result.value:
    #         return False
    #     else:  # create new table
    #         return True

    # def test_select_groupby_columns(self, groupby_columns: list):
    #     self.groupby_columns.value = groupby_columns
    #     return self  # allows method chaining

    # def test_select_aggregation(
    #     self,
    #     aggregation_function: str = "",
    #     column_name: str = "",
    #     new_column_name: str = "",
    # ):
    #     self.aggregation_section.test_select_aggregation_functions(
    #         aggregation_function, column_name, new_column_name
    #     )

    # def test_select_merge_result(self, merge_result: bool):
    #     self.merge_result.value = merge_result
