from dash import html
from utils import card_style, dataviz_df

import dash_bootstrap_components as dbc


def get_company_global_information(df_companies_global_information, selected_company):
    df_company = df_companies_global_information[df_companies_global_information['company_name'] == selected_company]
    df_company = df_company.reset_index(drop=True)

    company_global_information = {}
    company_global_information['company_name'] = df_company['company_name'][0]
    company_global_information['global_score_short_label'] = df_company['global_score_short_label'][0]
    company_global_information['global_score_hexa_color_code'] = df_company['global_score_hexa_color_code'][0]
    company_global_information['direct_score_short_label'] = df_company['direct_score_short_label'][0]
    company_global_information['direct_score_hexa_color_code'] = df_company['direct_score_hexa_color_code'][0]
    company_global_information['complete_score_short_label'] = df_company['complete_score_short_label'][0]
    company_global_information['complete_score_hexa_color_code'] = df_company['complete_score_hexa_color_code'][0]
    company_global_information['global_score_logo_path'] = df_company['global_score_logo_path'][0]
    company_global_information['comment'] = df_company['comment'][0]

    return company_global_information

def action_suivi_global(selected_company):
    company_global_information = get_company_global_information(dataviz_df, selected_company)

    return dbc.Container([
        dbc.Row(dbc.Col(html.Div("Au global", className="h5"))),
        dbc.Row(
            dbc.Col(html.Img(src=company_global_information['global_score_logo_path'])),
            className="pb-3 text-center"
        ),
        dbc.Row([
            dbc.Col([
                html.Div('Réduction de ses'),
                html.Div('propres émissions')
            ], className="col-3"),
            dbc.Col([
                html.Div('Réduction de son'),
                html.Div('empreinte carbone')
            ], className="col-3"),
            dbc.Col([
                html.Div('Commentaire'),
                html.Div('Nota Climat')
            ], className="col-6")
        ], className="fw-bold text-center"),
        dbc.Row([
            dbc.Col(
                html.Div('\u279c ' + company_global_information['direct_score_short_label']),
                className="text-center col-3",
                style={'color': company_global_information['direct_score_hexa_color_code']}
            ),
            dbc.Col(
                html.Div('\u279c ' + company_global_information['complete_score_short_label']),
                className="text-center col-3",
                style={'color': company_global_information['complete_score_hexa_color_code']}
            ),
            dbc.Col(html.Div(company_global_information['comment']), className="col-6")
        ])
    ], className="d-flex flex-column border rounded p-3 mx-2 w-auto")