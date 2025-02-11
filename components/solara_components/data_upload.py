from assets.state import State
import solara

drag_and_drop = "Drag and drop data to be upload or try out the tool with an inbuilt sample."
@solara.component
def DataUpload():
    with solara.Card("Data upload", margin=1, elevation=1):
        with solara.Row(margin=3):
            if 0 < State.upload_progress.value < 100:
                solara.ProgressLinear(value=State.upload_progress.value)
            else:
                solara.ProgressLinear(False)
        with solara.Tooltip(drag_and_drop, color='black'):
            with solara.Column():
                with solara.Row():
                    solara.Button("Sample dataset", color="primary", text=True, outlined=True, on_click=State.load_sample,
                                  disabled=len(State.dataframes.value) > 0)
                    solara.Button("Clear datasets", color="primary", text=True, outlined=True, on_click=State.reset,
                                  disabled=len(State.dataframes.value) <= 0)
                solara.FileDrop(on_file=State.load_data_from_file, on_total_progress=State.upload_progress.set,
                                label=State.path.value)