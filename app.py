from flask import Flask
from dash import Dash, html, Input, Output
import dash_ag_grid as dag
import pandas as pd

# df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/solar.csv")
from os import getenv
from dataiku import Dataset
original_ds_name = getenv("ORIGINAL_DATASET")
original_ds = Dataset(original_ds_name)
df = original_ds.get_dataframe()

server = Flask(__name__)
app = Dash(__name__, server=server)
app.enable_dev_tools(debug=True, dev_tools_ui=True)

grid = dag.AgGrid(
    id="quickstart-grid",
    rowData=df.to_dict("records"),
    columnDefs=[{"field": i} for i in df.columns],
    defaultColDef={"resizable": True, "sortable": True, "filter": True, "minWidth":125},
    columnSize="sizeToFit",
)

app.layout = html.Div([grid, html.Div(id="quickstart-output")])


@app.callback(
    Output("quickstart-output", "children"), Input("quickstart-grid", "cellClicked")
)
def display_cell_clicked_on(cell):
    if cell is None:
        return "Click on a cell"
    return f"clicked on cell value:  {cell['value']}, column:   {cell['colId']}, row index:   {cell['rowIndex']}"


if __name__ == "__main__":
    app.run_server(debug=True)