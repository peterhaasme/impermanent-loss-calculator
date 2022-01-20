# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash_html_components as html
from datetime import date
import pandas as pd
import plotly.express as px
from pycoingecko import CoinGeckoAPI

#############
# Instances #
#############
# Dash Instance and server
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SIMPLEX])
server = app.server

# Instantiate Coingecko API object
cg = CoinGeckoAPI()

##########
# Layout #
##########

# Layout components #

# Get list of coins from Coingecko and format into dropdown
token_list = cg.get_coins_list()
drop_down_values = []
for token in token_list:
    token_id = token['id']
    token_symbol = token['symbol'].upper()
    token_name = token['name']
    entry = {'label': token_symbol + ' - ' + token_name, 'value': token_id}
    drop_down_values.append(entry)

dropdown_1 = dbc.Select(
    id='token-dropdown-1',
    options=drop_down_values,
    placeholder='Select Token 1',
    class_name=''
)

dropdown_2 = dbc.Select(
    id='token-dropdown-2',
    options=drop_down_values,
    placeholder='Select Token 2'
)

# Datepicker

datepicker_start = dbc.InputGroup(
    children=[
        dbc.InputGroupText(
            children=['Select Start Date'],
            class_name='w-50'
        ),
        dcc.DatePickerSingle(
            id='date-picker-start',
            min_date_allowed=date(1995, 8, 5),
            max_date_allowed=date(2022, 1, 30),
            initial_visible_month=date(2022, 1, 5),
            date=date(2022, 1, 8),
        )
    ],
    class_name=''
)

# APR vs APY select
apr_v_apy = html.Div(
    [
        # dbc.Label("Choose one", html_for='radio-items-apr-v-apy'),
        dbc.RadioItems(
            options=[
                {"label": "APR", "value": 1},
                {"label": "APY", "value": 2},
            ],
            value=1,
            id="radio-items-apr-v-apy",
            inline=True,
        ),
    ]
)

# Page Layout #
app.layout = dbc.Container([
    # Title Row
    dbc.Row(
        children=dbc.Col(html.H1('Impermanent Loss Calculator')),
        class_name='text-center mt-3'
    ),
    # Main column row
    dbc.Row(
        children=[
            # Initial Values column
            dbc.Col(
                children=[
                    # Header row
                    dbc.Row(
                        children=[
                            dbc.Col(
                                children=html.H2('Initial Values'),
                                class_name='text-center'
                            )
                        ],
                        class_name=''
                    ),
                    # Date row
                    dbc.Row(
                        children=[
                            dbc.Col(
                                children=[
                                    datepicker_start
                                ],
                                class_name=''
                            ),
                        ],
                        class_name=''
                    ),
                    # Token 1 row
                    dbc.Row(
                        children=[
                            dbc.Col(
                                children=[
                                    dbc.InputGroup(
                                        children=[
                                            dbc.InputGroupText(
                                                children=dropdown_1,
                                                class_name='w-50'
                                            ),
                                            dbc.Input(id="token1_input", type="number"),
                                            dbc.InputGroupText("Qty"),
                                        ],
                                        class_name='flex-nowrap'
                                    ),
                                ],
                                width=12,
                                class_name=''
                            ),
                        ],
                        class_name=''
                    ),
                    # Token Row
                    dbc.Row(
                        children=[
                            dbc.Col(
                                children=[
                                    # TODO: Add tooltip
                                    #dbc.Label('Token 1', html_for="token-dropdown-1", class_name='h4'),
                                    #dropdown_1,
                                    # dbc.InputGroup(
                                    #     children=[
                                    #         dbc.InputGroupText(dropdown_1),
                                    #         dbc.Input(id="token1_input", type="number"),
                                    #         dbc.InputGroupText("Qty"),
                                    #     ],
                                    #     class_name=''
                                    # ),
                                ],
                                class_name=''
                            ),
                            dbc.Col(
                                children=[
                                    dbc.Label('Token 2', html_for="token-dropdown-2", class_name='h4'),
                                    dropdown_2
                                ],
                                class_name='',
                            ),
                        ],
                        class_name='text-center'
                    ),
                    # Start Date and APR Row
                    dbc.Row(
                        children=[
                            # dbc.Col(
                            #     children=[
                            #         datepicker_start
                            #     ],
                            #     class_name=''
                            # ),
                            dbc.Col(
                                children=[
                                    dbc.InputGroup(
                                        children=[
                                            dbc.InputGroupText(apr_v_apy),
                                            dbc.Input(id="apr_input", type="number"),
                                            dbc.InputGroupText("%"),
                                        ],
                                        class_name=''
                                    ),
                                ],
                                class_name=''
                            ),
                        ],
                        class_name='text-center'
                    ),
                ],
                class_name='border rounded'
            ),
            # Future Values Column
            dbc.Col(
                children=html.H2('Future Values'),
                class_name='text-center p-2 border rounded'
            ),
        ],
        class_name=''
    ),
])

# # Page Layout #
# app.layout = dbc.Container([
#     dbc.Row(
#         children=dbc.Col(html.H1('Impermanent Loss Calculator')),
#         class_name='text-center mt-3'
#     ),
#     dbc.Row(
#         children=[
#             dbc.Col(
#                 children=dropdown_1,
#                 class_name=''
#             ),
#         ],
#         class_name=''
#     ),
#     dbc.Row(
#         children=[
#             dbc.Col(
#                 children=datepicker,
#                 class_name=''
#             ),
#         ],
#         class_name=''
#     ),
#     dbc.Row(
#         children=[
#             dbc.Col(
#                 children=html.Div(id='output-container-date-picker-single'),
#                 class_name=''
#             ),
#         ],
#         class_name=''
#     ),
#     # dbc.Row(
#     #     children=[
#     #         dbc.Col(
#     #             children=apr_v_apy,
#     #             class_name=''
#     #         ),
#     #     ],
#     #     class_name=''
#     # ),
# ])

#############
# Callbacks #
#############

# def get_coin_price(coin_id, date):
#     coin_price = cg.get_coin_history_by_id(
#         id=coin_id,
#         date=date,
#         localization=False
#     )
#     return coin_price['market_data']['current_price']['usd']
#
# @app.callback(
#     Output('output-container-date-picker-single', 'children'),
#     Input('token-dropdown-1', 'value'),
#     Input('date-picker-single', 'date'),
# )
# def update_output(coin_name, date_value):
#     string_prefix = 'You have selected: '
#     if date_value and coin_name is not None:
#         date_object = date.fromisoformat(date_value)
#         date_string = date_object.strftime('%d-%m-%Y')
#         coin_price = get_coin_price(coin_id=coin_name, date=date_string)
#         return f'{coin_name} is ${coin_price:.2f}'
