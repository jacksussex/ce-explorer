# from assets.state import State
# import solara
# @solara.component
# def TextSearchView():
#     results = State.search_results.value
#     num_dfs = len(results)
#     with solara.Card():
#         for i in range(0, num_dfs):
#             with solara.Row():
#                 with solara.Card("Documents matched"):
#                     solara.Markdown(str(len(results[i][1])))
#             with solara.Row():
#                 with solara.Card(results[i][0]):
#                     solara.DataFrame(results[i][1])