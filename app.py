import pandas as pd
import os
import plotly.io as pio
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output
import base64

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

image_filename = 'data/aei_logo.png'
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

pio.templates.default = "plotly_white"

tab_selected_style = {
    'borderTop': '2px solid #008CCC',
}

CURR_PATH = os.path.abspath(os.path.dirname(__file__))

# read output

budget_output_path = os.path.join(CURR_PATH, "data/budget_estimates.csv")
budget_df = pd.read_csv(budget_output_path)

poverty_output_path = os.path.join(CURR_PATH, "data/poverty_estimates.csv")
poverty_df = pd.read_csv(poverty_output_path)

dists_output_path = os.path.join(CURR_PATH, "data/dist_estimates.csv")
dists_df = pd.read_csv(dists_output_path)

# primary content functions

def make_content(base, reform, refund, ctc_c, u6_bonus, ps, tabs):
    """
    function to make Plotly figure and summary table
    will be called in app callback
    """
    def table_data_base(base, refund, ctc_c, u6_bonus, ps):
        if base == "cl":
            table_data_base= budget_df.loc[
                    (budget_df["type"] == "CL")
                ]
        elif base == "biden":
        	table_data_base= budget_df.loc[
                    (budget_df["type"] == "Biden")
                ]
        elif base == "wnm":
            table_data_base= budget_df.loc[
                    (budget_df["type"] == "WNM")
                ]
        elif base == "fsa":
            table_data_base= budget_df.loc[
                    (budget_df["type"] == "Romney")
                ]
        return table_data_base

    def table_data_reform(reform, refund, ctc_c, u6_bonus, ps):
        if reform == "biden":
        	table_data_reform= budget_df.loc[
                    (budget_df["type"] == "Biden")
                ]
        elif reform == "wnm":
            table_data_reform= budget_df.loc[
                    (budget_df["type"] == "WNM")
                ]
        elif reform == "fsa":
            table_data_reform= budget_df.loc[
                    (budget_df["type"] == "Romney")
                ]
        elif reform == "custom":
            table_data_reform= budget_df.loc[
                    (budget_df["type"] == refund)
                    & (budget_df["ctc_c"] == ctc_c)
                    & (budget_df["u6_bonus"] == u6_bonus)
                    & (budget_df["ps"] == ps)
                ]    
        return table_data_reform
    
    def spm_data_base(base, refund, ctc_c, u6_bonus, ps):
        if base == "cl":
            spm_data_base= poverty_df.loc[
                    (poverty_df["type"] == "CL")
                ]
        elif base == "biden":
            spm_data_base= poverty_df.loc[
                    (poverty_df["type"] == "Biden")
                ]
        elif base == "wnm":
            spm_data_base= poverty_df.loc[
                    (poverty_df["type"] == "WNM")
                ]
        elif base == "fsa":
            spm_data_base= poverty_df.loc[
                    (poverty_df["type"] == "Romney")
                ]
        return spm_data_base

    def spm_data_reform(reform, refund, ctc_c, u6_bonus, ps):
        if reform == "biden":
        	spm_data_reform= poverty_df.loc[
                    (poverty_df["type"] == "Biden")
                ]
        elif reform == "wnm": 
        	spm_data_reform= poverty_df.loc[
                    (poverty_df["type"] == "WNM")
                ]
        elif reform == "fsa":
            spm_data_reform= poverty_df.loc[
                    (poverty_df["type"] == "Romney")
                ]
        elif reform == "custom": 
        	spm_data_reform= poverty_df.loc[
                    (poverty_df["type"] == refund)
                    & (poverty_df["ctc_c"] == ctc_c)
                    & (poverty_df["u6_bonus"] == u6_bonus)
                    & (poverty_df["ps"] == ps)
                ]    
        return spm_data_reform

    def figure_data_base(base, refund, ctc_c, u6_bonus, ps):
        if base == "cl":
                figure_data_base = dists_df.loc[
                    (dists_df["type"] == "CL")
                ]
        elif base == "biden":
                figure_data_base = dists_df.loc[
                    (dists_df["type"] == "Biden")
                ]
        elif base == "wnm":
                figure_data_base = dists_df.loc[
                    (dists_df["type"] == "WNM")
                ]
        elif base == "fsa":
                figure_data_base = dists_df.loc[
                    (dists_df["type"] == "Romney")
                ]
        return figure_data_base
                
    def figure_data_reform(reform, refund, ctc_c, u6_bonus, ps):
        if reform == "biden":
                figure_data_reform = dists_df.loc[
                    (dists_df["type"] == "Biden")
                ]
        elif reform == "wnm":
                figure_data_reform = dists_df.loc[
                    (dists_df["type"] == "WNM")
                ]
        elif reform == "fsa":
                figure_data_reform = dists_df.loc[
                    (dists_df["type"] == "Romney")
                ]
        elif reform == "custom":
                figure_data_reform = dists_df.loc[
                    (dists_df["type"] == refund)
                    & (dists_df["ctc_c"] == ctc_c)
                    & (dists_df["u6_bonus"] == u6_bonus)
                    & (dists_df["ps"] == ps)
                ]
        return figure_data_reform

    def make_figure(x_base,y_base,x_reform,y_reform,title,axtitle, yaxis_range):
        """
 		make primary figures
        """
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=x_base,
            y=y_base,
            name='Baseline Policy',
            marker_color='#008CCC',
        ))
        fig.add_trace(go.Bar(
            x=x_reform,
            y=y_reform,
            name='Reform Policy',
            marker_color='#414141'
        ))
        fig.update_layout(
            title={
            'text': title,
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
            xaxis_title= 'Expanded Income Decile',
            yaxis_title= axtitle,
            yaxis_range= yaxis_range,
            font=dict(color='#414141'))
        return fig

    if tabs == "summary_tab":
        base_data = table_data_base(base, refund, ctc_c, u6_bonus, ps)
        base_all = base_data['value_all']
        base_ctc = base_data['value_ctc']
        base_spm_data = spm_data_base(base, refund, ctc_c, u6_bonus, ps)
        base_spm_all = base_spm_data['spm_all']
        base_spm_u18 = base_spm_data['spm_u18']
        base = figure_data_base(base, refund, ctc_c, u6_bonus, ps)
        base_avg = base.loc[(base["decile"] == "ALL")]
        base_mean = base_avg['mean']
        base_pcati = base_avg['pc_aftertaxinc']
        base_metr = base_avg['metr_reform']

        reform_data = table_data_reform(reform, refund, ctc_c, u6_bonus, ps)
        reform_all = reform_data['value_all']
        reform_ctc = reform_data['value_ctc']
        reform_spm_data = spm_data_reform(reform, refund, ctc_c, u6_bonus, ps)
        reform_spm_all = reform_spm_data['spm_all']
        reform_spm_u18 = reform_spm_data['spm_u18']
        reform = figure_data_reform(reform, refund, ctc_c, u6_bonus, ps)
        reform_avg = reform.loc[(reform["decile"] == "ALL")]
        reform_mean = reform_avg['mean']
        reform_pcati = reform_avg['pc_aftertaxinc']
        reform_metr = reform_avg['metr_reform']

        diff_all = round(reform_all.item() - base_all.item(),1)
        diff_ctc =  round(reform_ctc.item() -  base_ctc.item(),1)
        diff_mean = round(reform_mean.item() - base_mean.item(),1)
        diff_pcati = round(reform_pcati.item() - base_pcati.item(),1)
        diff_metr = round(reform_metr.item() - base_metr.item(),1)
        diff_spm_all = round(reform_spm_all.item() - base_spm_all.item(),1)
        diff_spm_u18 = round(reform_spm_u18.item() - base_spm_u18.item(),1)


        fig = go.Figure(data=[go.Table(
        	columnorder = [1,2,3,4],
  			columnwidth = [52,16,16,16],
            header=dict(values=['', 'Baseline Policy','Reform Policy', 'Difference'], 
            fill_color='#008CCC',
            font=dict(color='white', size=14)),
            cells=dict(values=[['Annual Value of All Child Tax Benefits (2021 $)',
                                'Annual Value of Child Tax Credit (2021 $)',
                                'Average Total Benefit - All Child Tax Benefits ($)',
                                'Average Percent Change in After-Tax Income (%)',
                                'Person Weighted Effective Marginal Tax Rate (EMTR) on Labor (%)',
                                'SPM Poverty Rate - Total U.S. (%)',
                                'SPM Poverty Rate - Children Under 18 (%)'],
            [base_all, base_ctc, base_mean, base_pcati, base_metr, base_spm_all, base_spm_u18],
            [reform_all, reform_ctc, reform_mean, reform_pcati, reform_metr, reform_spm_all, reform_spm_u18],
            [diff_all, diff_ctc, diff_mean, diff_pcati, diff_metr, diff_spm_all, diff_spm_u18]],
            fill_color='#F9F9F9',
            font=dict(color='#414141', size=12),
            align = ['left','center']))
                     ])

        fig.update_layout(
            title={
            'text': 'Comparing Selected Baseline and Reform Policies — All Child Tax Benefits',
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
            font=dict(color='#414141'))
        
    elif tabs == "mean_tab":
        title = 'Average Value of All Child Tax Benefits by Income Decile, Households with Children'
        axtitle = '2021 Dollars ($)'
        yaxis_range = [0,10000]
        x_base = figure_data_base(base, refund, ctc_c, u6_bonus, ps)
        x_base = x_base['decile']
        y_base = figure_data_base(base, refund, ctc_c, u6_bonus, ps)
        y_base = y_base['mean']
        x_reform = figure_data_reform(reform, refund, ctc_c, u6_bonus, ps)
        x_reform = x_reform['decile']
        y_reform = figure_data_reform(reform, refund, ctc_c, u6_bonus, ps)
        y_reform = y_reform['mean']
        fig = make_figure(x_base,y_base,x_reform,y_reform,title,axtitle,yaxis_range)
    elif tabs == "pcati_tab":
        title = 'Distributional Impact of All Child Tax Benefits, Households with Children'
        axtitle = 'Percent Change in After-Tax Income (%)'
        yaxis_range = [0,140]
        x_base = figure_data_base(base, refund, ctc_c, u6_bonus, ps)
        x_base = x_base['decile']
        y_base = figure_data_base(base, refund, ctc_c, u6_bonus, ps)
        y_base = y_base['pc_aftertaxinc']
        x_reform = figure_data_reform(reform, refund, ctc_c, u6_bonus, ps)
        x_reform = x_reform['decile']
        y_reform = figure_data_reform(reform, refund, ctc_c, u6_bonus, ps)
        y_reform = y_reform['pc_aftertaxinc']
        fig = make_figure(x_base,y_base,x_reform,y_reform,title,axtitle,yaxis_range)
    elif tabs == "emtr_tab":
        title = 'Person Weighted Effective Marginal Tax Rate (EMTR) on Labor Income, Households with Children'
        axtitle = 'EMTR (%)'
        yaxis_range = [-30,30]
        x_base = figure_data_base(base, refund, ctc_c, u6_bonus, ps)
        x_base = x_base['decile']
        y_base = figure_data_base(base, refund, ctc_c, u6_bonus, ps)
        y_base = y_base['metr_reform']
        x_reform = figure_data_reform(reform, refund, ctc_c, u6_bonus, ps)
        x_reform = x_reform['decile']
        y_reform = figure_data_reform(reform, refund, ctc_c, u6_bonus, ps)
        y_reform = y_reform['metr_reform']
        fig = make_figure(x_base,y_base,x_reform,y_reform,title,axtitle,yaxis_range)
    
    return fig

app = dash.Dash(
    url_base_pathname=os.environ.get("URL_BASE_PATHNAME", "/"),
    external_stylesheets=external_stylesheets,
)


# layout can be thought of as HTML elements
app.layout = html.Div(
    [
        html.Div([
                html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()),
                height=80)
              ]),
        dcc.Markdown(
            """
            ## The Tax Benefits Of Parenthood Interactive Dashboard
            *Modeling and design by <a href="https://github.com/grantseiter/" children="Grant M. Seiter" style="color:#4f5866;text-decoration:none" target="blank" />*
            """,
            style={"max-width": "1000", "padding-bottom": "10px", "color": "#4f5866"},
            dangerously_allow_html=True,
        ),
        dcc.Markdown(
            """
			This dashboard allows users to investigate various reforms to the child tax credit in the context of all tax 
			benefits currently afforded to filers with children (the child tax credit (CTC), the earned income tax credit, 
			the head-of-household filing status, and the child and dependent care tax credit). Users can select a baseline 
			policy — current law, President Joe Biden’s American Rescue Plan, recent legislation adopted by the House Committee on Ways 
			and Means, or Sen. Mitt Romney’s (R-UT) proposed Family Security Act — and a reform policy to analyze. In addition 
			to the three proposals already mentioned, users can specify their own child tax credit reform by selecting the 
			"Custom CTC Reform" option and adjusting the four parameters in grey — refundability, the maximum credit value, 
			the dollar bonus for children under six, and the threshold for which the credit begins phasing out.
            """,
            style={"max-width": "1000px","text-align":"justify"},
            dangerously_allow_html=True,
        ),    
        html.Div(
            [
                # baseline dropdown
                html.Label("Baseline Policy"),
                dcc.Dropdown(
                    id="base",
                    options=[
                        {"label": "Current Law", "value": "cl"},
                        {"label": "Biden Proposal", "value": "biden"},
                        {"label": "Ways & Means Proposal", "value": "wnm"},
                        {"label": "Family Security Act", "value": "fsa"},
                    ],
                    value="cl",
                    clearable=False
                ),
            ],
            style={"width": "450px", "display": "inline-block", "padding-left": "25px","padding-right": "25px","padding-top": "5px","padding-bottom": "20px"},
        ),  
        html.Div(
            [
                # reform dropdown
                html.Label("Reform Policy"),
                dcc.Dropdown(
                    id="reform",
                    options=[
                        {"label": "Biden Proposal", "value": "biden"},
                        {"label": "Ways & Means Proposal", "value": "wnm"},
                        {"label": "Family Security Act", "value": "fsa"},
                        {"label": "Custom CTC Reform", "value": "custom"},
                    ],
                    value="biden",
                    clearable=False
                ),
            ],
            style={"width": "450px", "display": "inline-block", "padding-left": "25px","padding-right": "25px","padding-top": "5px","padding-bottom": "20px"},
        ), 
        html.Div(
            [ # new line
            ],
            style={'whiteSpace': 'pre-wrap'},
        ),
        html.Div(id='custom_container',
        children= [
        html.Div(
            [
                # custom refundability dropdown
                html.Label("Refundability"),
                dcc.Dropdown(
                    id="refund",
                    options=[
                        {"label": "Current Law", "value": "Nonref"},
                        {"label": "Fully Refundable", "value": "Refund"},
                    ],
                    value= "Nonref",
                    clearable=False
                ),
            ],
            style={"width": "200px", "display": "inline-block","padding-left": "25px","padding-right": "25px","padding-top": "5px","padding-bottom": "20px","background-color": "#F9F9F9"},
        ),
        html.Div(
            [   # custom max credit value dropdown
                html.Label("Maximum Credit Value"),
                dcc.Dropdown(
                    id="ctc_c",
                    options=[
                        {"label": "$2000", "value": 2000},
                        {"label": "$2500", "value": 2500},
                        {"label": "$3000", "value": 3000},
                        {"label": "$3500", "value": 3500},
                    ],
                    value=2000,
                    clearable=False
                ),
            ],
            style={"width": "200px","display": "inline-block","padding-left": "25px","padding-right": "25px","padding-top": "5px","padding-bottom": "20px","background-color": "#F9F9F9"},
        ),
        html.Div(
            [   # custom under 6 dropdown
                html.Label("Bonus For Children Under 6"),
                dcc.Dropdown(
                    id="u6_bonus",
                    options=[
                        {"label": "$0", "value": 0},
                        {"label": "$500", "value": 500},
                        {"label": "$1000", "value": 1000},
                    ],
                    value=0,
                    clearable=False
                ),
            ],
            style={"width": "200px","display": "inline-block","padding-left": "25px","padding-right": "25px","padding-top": "5px","padding-bottom": "20px","background-color": "#F9F9F9"},
        ),
        html.Div(
            [   # custom phaseout start dropdown
                html.Label("Phaseout Start"),
                dcc.Dropdown(
                    id="ps",
                    options=[
                        {"label": "200K Single / 400K MFJ", "value": "CL"},
                        {"label": "Eliminate Phaseout", "value": "NO"},
                    ],
                    value="CL",
                    clearable=False
                ),
            ],
            style={"width": "200px","display": "inline-block","padding-left": "25px","padding-right": "25px","padding-top": "5px","padding-bottom": "20px","background-color": "#F9F9F9"},
        ),
        ]),
        html.Div(
            [
                dcc.Tabs(
                    id="tabs",
                    value="summary_tab",
                    children=[
                        dcc.Tab(label="Table: Summary Estimates", value="summary_tab", selected_style=tab_selected_style),
                        dcc.Tab(label="Graph: Average Value of All Child Tax Benefits", value="mean_tab", selected_style=tab_selected_style),
                        dcc.Tab(label="Graph: Percent Change in After-Tax Income", value="pcati_tab", selected_style=tab_selected_style),
                        dcc.Tab(label="Graph: Effective Marginal Tax Rate on Labor", value="emtr_tab", selected_style=tab_selected_style),
                        
                    ],
                )
            ],
            style={"max-width": "1000px","padding-top": "25px"},
        ),
        html.Div([dcc.Graph(id="content_tab")], style={"max-width": "1000px"}),
        dcc.Markdown(
            """
            **Note:** This dashboard accompanies <a href="https://www.aei.org/research-products/report/the-tax-benefits-of-parenthood-a-history-and-analysis-of-current-proposals/"
            children="The Tax Benefits of Parenthood: A History and Analysis of
            Current Proposals" style="color:#008CCC" target="blank"/> (Brill, Pomerleau, and Seiter 2021). 
            Data for this project are generated using the open-source
            <a href="https://github.com/PSLmodels/Tax-Calculator#README" children="Tax-Calculator" style="color:#008CCC" target="blank"/> project. 
            The code that modifies the underlying models to produce these estimates
            can be found <a href="https://github.com/grantseiter/Tax-Benefits-Of-Parenthood" children="here" style="color:#008CCC" target="blank"/>
            and <a href="https://github.com/grantseiter/Child-Tax-Credit-App" children="here" style="color:#008CCC" target="blank" />.
            The code that powers this data visualization can be found
            <a href="https://github.com/grantseiter/Child-Tax-Credit-App" children="here" style="color:#008CCC" target="blank" />.
            """,
            style={"max-width": "1000px","text-align":"justify"},
            dangerously_allow_html=True,
        ),    
    ]
)

@app.callback(
    # output toggles custom parameters
    Output("custom_container","style"),
    Input("reform","value")
)
def toggle_custom(reform):
    # call function that defines html display
    if reform == 'custom':
        return {'display': 'block'}
    else:
        return {'display': 'none'}

@app.callback(
    # output is figure
        Output("content_tab", "figure"),
        Input("base", "value"),
        Input("reform", "value"),
        Input("refund", "value"),
        Input("ctc_c", "value"),
        Input("u6_bonus", "value"),
        Input("ps", "value"),
        Input("tabs", "value"),
)
def update(base, reform, refund, ctc_c, u6_bonus, ps, tabs):
    # call function that constructs figure and table
    fig = make_content(base, reform, refund, ctc_c, u6_bonus, ps, tabs)
    return fig

server = app.server
# turn debug=False for production
if __name__ == "__main__":
    app.run_server(debug=True, use_reloader=True)
