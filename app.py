from flask import Flask
from dash import Dash, html, Input, Output
import dash_ag_grid as dag
from dataiku import use_plugin_libs, import_from_plugin

PROJECT_KEY = "COMPANY_RECONCILIATION"
ORIGINAL_DS_NAME = "matches_uncertain"
PRIMARY_KEYS = ["id"]
EDITABLE_COLUMN_NAMES = ["ext_id", "reviewed", "comments"]

use_plugin_libs("editable-via-webapp")
EditableEventSourced = import_from_plugin("editable-via-webapp", "EditableEventSourced")
ees = EditableEventSourced.EditableEventSourced(
    original_ds_name=ORIGINAL_DS_NAME,
    primary_keys=PRIMARY_KEYS,
    editable_column_names=EDITABLE_COLUMN_NAMES,
    project_key=PROJECT_KEY)
df = ees.get_edited_df()

# original_ds = Dataset(original_ds_name)
# df = original_ds.get_dataframe()
# df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/solar.csv")

server = Flask(__name__)
app = Dash(__name__, server=server)
app.enable_dev_tools(debug=True, dev_tools_ui=True)

grid = dag.AgGrid(
    id="quickstart-grid",
    rowData=df.to_dict("records"),
    columnDefs=[{"field": i} for i in df.columns],
    defaultColDef={"editable": True, "resizable": True, "sortable": True, "filter": True, "minWidth": 125},
    columnSize="sizeToFit",
)

app.layout = html.Div([grid, html.Div(id="quickstart-output")])


@app.callback(
    Output("quickstart-output", "children"),
    Input("quickstart-grid", "cellValueChanged"),
    prevent_initial_call=True
)
def log_edit(cell):
    """Record edit in editlog, once a cell has been edited"""
    return ees.update_row(cell["data"], cell["colId"], cell["newValue"])


if __name__ == "__main__":
    app.run_server(debug=True)