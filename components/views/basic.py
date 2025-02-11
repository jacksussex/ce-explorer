# from assets.state import State
# import solara
#
# @solara.component
# def BasicView(df):
#     with solara.Card():
#         with solara.Row():
#             with solara.Card():
#                 solara.Markdown("Dataset size: " + str(len(df)))
#         with solara.Row():
#             with solara.Column():
#                 solara.DataFrame(df[[State.chosen_column.value]])