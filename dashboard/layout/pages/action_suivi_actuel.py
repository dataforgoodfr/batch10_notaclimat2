from dash import html, dcc

import dash_bootstrap_components as dbc
import dash_daq as daq

from utils import card_style
from utils import dataviz_df

import plotly.graph_objects as go
import plotly.figure_factory as ff

import numpy as np
import pandas as pd

# Colorbars for bullet gauge
color_bars = ['#820000', '#C00000', '#FF8939', '#FEC800', '#8CDF41', '#0DB800']


def get_filtered_data(df, selected_company):
    df_filtered = df[df['company_name'] == selected_company].reset_index(drop=True)
    df_filtered = df_filtered.replace('n.a.', np.nan)
    return df_filtered


def get_data(df, column_name):
    '''
    Extracts info from a dataframe. Used to improve code lisibility.
    '''
    value = df.loc[0, column_name]
    return value


def build_bullet_gauge(engagement, accomplishment, color_accomplishment):
    '''
    Builds the custom Bullet Gauge for the dashboard.
    Takes 2 values for the engagement & accomplishment from the selected_company
    Returns the gauge with colors varying from green to dark red, with cursors on both sides representing:
    - in white, on the right side: the engagement from the company, expressed as a score
    - in color, on the left side: the actual accomplishments from the same company, expressed as a score
    '''

    # Building custom bullet gauge
    data = [{"ranges": [1, 7, 6], "measures": [x for x in range(1, 7)]}]
    width = 0.5

    traces = []
    fig = go.Figure()

    for i in range(0, 6):
        trace = go.Bar(x=[0],
                       y=[1],
                       orientation='v',
                       width=width,
                       marker_color=color_bars[i],
                       showlegend=False,
                       hoverinfo='skip')
        traces.insert(0, trace)

    fig.add_traces(traces)
    fig.update_layout(barmode='stack')

    # Building left cursor: accomplishment
    trace1 = go.Scatter(x=[-0.1 - width],
                        y=[7 - accomplishment],
                        marker={
                            'symbol': 'arrow-right',
                            'color': color_accomplishment,
                            'size': 25,
                        },
                        name='Accomplishment',
                        xaxis='x1',
                        yaxis='y1',
                        hovertemplate='Niveau de réduction observé<extra></extra>',
                        showlegend=False)

    # Building right cursor: engagement
    trace2 = go.Scatter(x=[0.1 + width],
                        y=[7 - engagement],
                        marker={
                            'symbol': 'arrow-left',
                            'color': 'white',
                            'line': {
                                'color': 'black',
                                'width': 1
                            },
                            'size': 20
                        },
                        name='Engagement',
                        xaxis='x1',
                        yaxis='y1',
                        hovertemplate='Engagement',
                        showlegend=False)

    # Fixing ticks
    #fig.update_xaxes(ticks="outside", nticks=3)
    fig.update_xaxes(visible=False)
    fig.update_yaxes(layer="below traces",
                     tickmode='array',
                     tickvals=[1, 2, 3, 4, 5, 6],
                     ticktext=['+1.5°', '', '+2°C', '', '+4°C', ''])

    # Deleting the background
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=20, r=50, t=2, b=50))

    # Adding cursors
    fig.add_traces([trace1, trace2])

    return fig


def top_left(selected_company):
    df = get_filtered_data(dataviz_df, selected_company)
    value = get_data(df, 'direct_score_short_label')
    color = get_data(df, 'direct_score_hexa_color_code')
    pic = 'assets/frames/Picto_usine.png'
    return value, color, pic


def generate_topleft_item(selected_company):
    value_topleft, color_topleft, pic_topleft = top_left(selected_company)
    return html.Div([
        html.Table([
            html.Tbody([
                html.Tr([
                    html.Td(html.Img(src=pic_topleft), rowSpan=1, className="me-1"),
                    html.Td('Evolution de ses propres émissions (scopes 1 & 2)', className="fw-bold"),
                ]),
                html.Tr([
                    daq.Indicator(color=color_topleft, value=True),
                    html.Td('Compatible : \u279c ' + value_topleft, className="px-2"),
                ],
                        className="align-baseline")
            ])
        ],
                   className="align-middle table table-borderless text-left mb-0")
    ])


def top_right(selected_company):
    df = get_filtered_data(dataviz_df, selected_company)
    value = get_data(df, 'complete_score_short_label')
    color = get_data(df, 'complete_score_hexa_color_code')
    pic = 'assets/frames/Picto_lifecycle.png'
    return value, color, pic


def generate_topright_item(selected_company):
    value_topright, color_topright, pic_topright = top_right(selected_company)
    return html.Div([
        html.Table([
            html.Tbody([
                html.Tr([
                    html.Td(html.Img(src=pic_topright), rowSpan=1, className="me-1"),
                    html.Td('Evolution de son empreinte carbone complète (scopes 1, 2 & 3)', className="fw-bold"),
                ]),
                html.Tr([
                    daq.Indicator(color=color_topright, value=True),
                    html.Td('Compatible : \u279c ' + value_topright, className="px-2"),
                ],
                        className="align-baseline")
            ])
        ],
                   className="align-middle table table-borderless mb-0")
    ])


def bottom_left(selected_company):
    df = get_filtered_data(dataviz_df, selected_company)
    values = []
    col_list = ['c1_final_value', 'c1_2_deg_final', 'c1_1_8_deg_final', 'c1_1_5_deg_final']

    for col in col_list:
        val = get_data(df, col)
        if val != np.nan:
            values.append(val - 1)
        else:
            values.append(0)

    engagement = get_data(df, 'direct_score_commitments')
    accomplishment_level = get_data(df, 'direct_level')
    accomplishment_score = get_data(df, 'direct_score')
    color_accomplishment = get_data(df, 'direct_score_hexa_color_code')
    colors = [color_accomplishment, '#FEC800', '#8CDF41', '#0DB800']
    accomplishment_initial_year = get_data(df, 'c1_initial_date')
    accomplishment_final_year = get_data(df, 'c1_final_date')

    return values, colors, engagement, accomplishment_level, accomplishment_score, color_accomplishment, accomplishment_initial_year, accomplishment_final_year


def get_bottomleft_title(accomplishment_initial_year, accomplishment_final_year):
    if pd.isna(accomplishment_initial_year) or pd.isna(accomplishment_final_year):
        return "Réduction de ses propres émissions de CO2e"
    else:
        initial_year = str(accomplishment_initial_year)
        final_year = str(accomplishment_final_year)
        return "Réduction de ses propres émissions de CO2e entre " + initial_year + " et " + final_year


def generate_bottomleft_left_column(scenarios, values, colors, accomplishment_score):
    if accomplishment_score == 1:
        return dbc.Col(html.Div(['Pas de mesure/reporting.',
                                 html.Br(), 'Trajectoire critique >4°C.']),
                       className="d-flex align-items-center justify-content-center",
                       style={
                           'text-align': 'center',
                           'width': '60%',
                           'minWidth': '60%',
                           'maxWidth': '60%',
                           'height': 'inherit'
                       })
    elif accomplishment_score == 99:
        return dbc.Col(
            html.Div(['Mesure seulement récente.',
                     html.Br(),'Trajectoire business-as-usual : vers +4°C.']),
            className="d-flex align-items-center justify-content-center",
            style={
                'text-align': 'center',
                'width': '60%',
                'minWidth': '60%',
                'maxWidth': '60%',
                'height': 'inherit'
            })
    else:
        fig = go.Figure([
            go.Bar(x=scenarios,
                   y=values,
                   text=values,
                   marker_color=colors,
                   hovertemplate="%{x} : %{y:.0%}<extra></extra>")
        ])
        fig.update_traces(texttemplate='%{text:.0%}', textposition='outside')
        fig.update_layout(showlegend=False,
                          paper_bgcolor='rgba(0,0,0,0)',
                          plot_bgcolor='rgba(0,0,0,0)',
                          margin=dict(l=20, r=20, t=50, b=0))
        #fig.update_yaxes(title=get_bottomleft_title(accomplishment_initial_year, accomplishment_final_year), tickformat=".0%")
        fig.update_yaxes(tickformat=".0%", range=[-0.6, 0.6], tick0=-0.5, dtick=0.25)
        fig.update_xaxes(tickangle=90, automargin=True)

        return dbc.Col(
            dcc.Graph(figure=fig, config={'displayModeBar': False}),
            style={
                'width': '60%',
                'minWidth': '60%',
                'maxWidth': '60%',
                #'height': '100%'
            })


def generate_bottomleft_item(selected_company):
    scenarios = ['Réduction observée', 'Reco 2°C', 'Reco 1.8°C', 'Reco 1.5°C']
    values, colors, engagement, accomplishment_level, accomplishment_score, color_accomplishment, accomplishment_initial_year, accomplishment_final_year = bottom_left(
        selected_company)

    return html.Div(
        [
            dbc.Row([
                html.Div(get_bottomleft_title(accomplishment_initial_year, accomplishment_final_year),
                         style={'text-align': 'center'}),
                generate_bottomleft_left_column(scenarios, values, colors, accomplishment_score),
                dbc.Col(
                    [
                        html.Div('Compatibilité climatique actuelle vs. ses engagements annoncés',
                                 style={
                                     'text-align': 'center',
                                     'font-size': '0.75em',
                                     'margin': '10px'
                                 }),
                        dcc.Graph(figure=build_bullet_gauge(engagement, accomplishment_level, color_accomplishment),
                                  config={'displayModeBar': False})
                    ],
                    style={
                        'width': '40%',
                        'minWidth': '40%',
                        'maxWidth': '40%',
                        #'height': '100%'
                    },
                    className="p-0")
            ])
        ],
        className="d-flex flex-column border")


def bottom_right(selected_company):
    df = get_filtered_data(dataviz_df, selected_company)
    values = []
    col_list = ['c2_final_value', 'c2_2_deg_final', 'c2_1_8_deg_final', 'c2_1_5_deg_final']

    for col in col_list:
        val = get_data(df, col)
        if val != np.nan:
            values.append(val - 1)
        else:
            values.append(0)

    engagement = get_data(df, 'complete_score_commitments')
    accomplishment_level = get_data(df, 'complete_level')
    accomplishment_score = get_data(df, 'complete_score')
    color_accomplishment = get_data(df, 'complete_score_hexa_color_code')
    colors = [color_accomplishment, '#FEC800', '#8CDF41', '#0DB800']
    accomplishment_initial_year = get_data(df, 'c2_initial_date')
    accomplishment_final_year = get_data(df, 'c2_final_date')

    return values, colors, engagement, accomplishment_level, accomplishment_score, color_accomplishment, accomplishment_initial_year, accomplishment_final_year


def get_bottomright_title(accomplishment_initial_year, accomplishment_final_year):
    if pd.isna(accomplishment_initial_year) or pd.isna(accomplishment_final_year):
        return "Réduction de l'empreinte carbone"
    else:
        initial_year = str(accomplishment_initial_year)
        final_year = str(accomplishment_final_year)
        return "Réduction de l'empreinte carbone entre " + initial_year + " et " + final_year


def generate_bottomright_left_column(scenarios, values, colors, accomplishment_score):
    if accomplishment_score == 1:
        return dbc.Col(html.Div(['Pas de mesure/reporting.',
                                 html.Br(), 'Trajectoire critique >4°C.']),
                       className="d-flex align-items-center justify-content-center",
                       style={
                           'text-align': 'center',
                           'width': '60%',
                           'min-width': '60%',
                           'max-width': '60%',
                           'height': 'inherit'
                       })
    elif accomplishment_score == 99:
        return dbc.Col(
            html.Div(['Mesure seulement récente.',
                     html.Br(),'Trajectoire business-as-usual : vers +4°C.']),
            className="d-flex align-items-center justify-content-center",
            style={
                'text-align': 'center',
                'width': '60%',
                'min-width': '60%',
                'max-width': '60%',
                'height': 'inherit'
            })
    else:
        fig = go.Figure([
            go.Bar(x=scenarios,
                   y=values,
                   text=values,
                   marker_color=colors,
                   hovertemplate="%{x} : %{y:.0%}<extra></extra>")
        ])
        fig.update_traces(texttemplate='%{text:.0%}', textposition='outside')
        fig.update_layout(showlegend=False,
                          paper_bgcolor='rgba(0,0,0,0)',
                          plot_bgcolor='rgba(0,0,0,0)',
                          margin=dict(l=20, r=20, t=50, b=0))
        #fig.update_yaxes(title=get_bottomright_title(accomplishment_initial_year, accomplishment_final_year),
        #    tickformat=".0%")
        fig.update_yaxes(tickformat=".0%", range=[-0.6, 0.6], tick0=-0.5, dtick=0.25)
        fig.update_xaxes(tickangle=90, automargin=True)

        return dbc.Col(
            dcc.Graph(figure=fig, config={'displayModeBar': False}),
            style={
                'width': '60%',
                'min-width': '60%',
                'max-width': '60%',
                #'height': '100%'
            })


def generate_bottomright_item(selected_company):
    scenarios = ['Réduction observée', 'Reco 2°C', 'Reco 1.8°C', 'Reco 1.5°C']
    values, colors, engagement, accomplishment_level, accomplishment_score, color_accomplishment, accomplishment_initial_year, accomplishment_final_year = bottom_right(
        selected_company)

    return html.Div(
        [
            dbc.Row([
                html.Div(get_bottomright_title(accomplishment_initial_year, accomplishment_final_year),
                         style={'text-align': 'center'}),
                generate_bottomright_left_column(scenarios, values, colors, accomplishment_score),
                dbc.Col(
                    [
                        html.Div('Compatibilité climatique actuelle vs. ses engagements annoncés',
                                 style={
                                     'text-align': 'center',
                                     'font-size': '0.75em',
                                     'margin': '10px'
                                 }),
                        dcc.Graph(figure=build_bullet_gauge(engagement, accomplishment_level, color_accomplishment),
                                  config={'displayModeBar': False})
                    ],
                    style={
                        'width': '40%',
                        'min-width': '40%',
                        'max-width': '40%',
                        #'height': '100%'
                    },
                    className="p-0")
            ]),
        ],
        className="d-flex flex-column border")


def action_suivi_actuel(selected_company):
    return dbc.Container([
        html.Div("Réductions observées et compatibilités climatiques actuelles", className="h5"),
        html.Div(
            dbc.Row([
                dbc.Col(generate_topleft_item(selected_company), className='d-inline p-2', style={'width': '49%'}),
                dbc.Col(generate_topright_item(selected_company), className='d-inline p-2', style={'width': '49%'}),
            ],
                    style={
                        'width': '80%',
                        'verticalAlign': 'middle'
                    })),
        html.Div(
            dbc.Row([
                dbc.Col(generate_bottomleft_item(selected_company), className='d-inline p-2', style={'width': '49%'}),
                dbc.Col(generate_bottomright_item(selected_company), className='d-inline p-2', style={'width': '49%'}),
            ],
                    style={'verticalAlign': 'middle'}))
    ],
                         className="d-flex flex-column")
