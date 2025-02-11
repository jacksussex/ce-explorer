from assets.state import State
import solara

dataview = "Choose a dataset and/or column to view and check the uploaded data."

def DataView(df, multiselect=False):
    with solara.Tooltip(dataview, color="black"):
        with solara.Card("Data view", margin=1, elevation=1):
            if len(State.dataframes.value) > 0:
                solara.Select("Dataset", values=State.dataframe_names.value, value=State.chosen_dataframe,
                              on_value=State.reset_column)
            if df is not None:
                columns = df.columns.tolist()
                if multiselect:
                    solara.SelectMultiple(label="Columns",values=State.chosen_columns, all_values=columns)
                else:
                    solara.Select("Column", values=columns, value=State.chosen_column)

                with solara.Row(margin=3):
                    solara.Button("Reset data-view", color="primary", text=True, outlined=True,
                                  on_click=State.reset_view)