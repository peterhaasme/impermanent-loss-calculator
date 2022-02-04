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
############
# Dash Instance and server
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SPACELAB])
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
            class_name='w-50',
        ),
        dcc.DatePickerSingle(
            id='date-picker-start',
            min_date_allowed=date(1995, 8, 5),
            max_date_allowed=date.today(),
            date=date.today(),
        )
    ],
    class_name=''
)

datepicker_future = dbc.InputGroup(
    children=[
        dbc.InputGroupText(
            children=['Select Future Date'],
            class_name='w-50',
        ),
        dcc.DatePickerSingle(
            id='date-picker-future',
            min_date_allowed=date.today(),
            date=date.today(),
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
        children=dbc.Col(html.H1('Impermanent Loss Calculator', className='text-white'), class_name='bg-primary border rounded'),
        class_name='text-center p-1'
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
                                children='Initial Values',
                                class_name='h2 text-center'
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
                        class_name='m-1'
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
                                            dbc.Input(id="token-1-qty", type="number"),
                                            dbc.InputGroupText("Qty"),
                                        ],
                                        #class_name='flex-nowrap'
                                    ),
                                ],
                                class_name=''
                            ),
                        ],
                        class_name='m-1'
                    ),
                    # Token 2 row
                    dbc.Row(
                        children=[
                            dbc.Col(
                                children=[
                                    dbc.InputGroup(
                                        children=[
                                            dbc.InputGroupText(
                                                children=dropdown_2,
                                                class_name='w-50'
                                            ),
                                            dbc.Input(id="token-2-qty", disabled=True),
                                            dbc.InputGroupText("Qty"),
                                        ],
                                        #class_name='flex-nowrap'
                                    ),
                                ],
                                class_name=''
                            ),
                        ],
                        class_name='m-1'
                    ),
                    # Token price row
                    dbc.Row(
                        children=[
                            dbc.Col(
                                children=[
                                    dbc.InputGroup(
                                        children=[
                                            dbc.InputGroupText(
                                                children='Token 1 Price',
                                                class_name=''
                                            ),
                                            dbc.Input(id="token-1-price", disabled=True),
                                            dbc.InputGroupText(
                                                children='Token 2 Price',
                                                class_name=''
                                            ),
                                            dbc.Input(id="token-2-price", disabled=True),
                                        ],
                                    ),
                                ],
                                class_name=''
                            ),
                        ],
                        class_name='m-1'
                    ),
                    # Start Date and APR Row
                    dbc.Row(
                        children=[
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
                        class_name='m-1'
                    ),
                    # Total Value Row
                    dbc.Row(
                        children=[
                            dbc.Col(
                                children=[
                                    dbc.InputGroup(
                                        children=[
                                            dbc.InputGroupText('Total Value'),
                                            #dbc.InputGroupText('$'),
                                            dbc.Input(id="total-value", disabled=True),
                                        ],
                                        class_name=''
                                    ),
                                ],
                                class_name=''
                            ),
                        ],
                        class_name='mx-1 mb-2'
                    ),
                ],
                class_name='m-1 p-1 border rounded bg-secondary',
                md=6
            ),
            # Future Values Column
            dbc.Col(
                children=[
                    # Header row
                    dbc.Row(
                        children=[
                            dbc.Col(
                                children=html.H2('Future Values'),
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
                                    datepicker_future
                                ],
                                class_name=''
                            ),
                        ],
                        class_name='m-1'
                    ),
                    # Token 1 row
                    dbc.Row(
                        children=[
                            dbc.Col(
                                children=[
                                    dbc.InputGroup(
                                        children=[
                                            dbc.InputGroupText(
                                                children='Future Quantity Token 1',
                                                class_name='w-50'
                                            ),
                                            dbc.Input(id="token-1-future-qty", type="number", disabled=True),
                                        ],
                                    ),
                                ],
                                class_name=''
                            ),
                        ],
                        class_name='m-1'
                    ),
                    # Token 2 row
                    dbc.Row(
                        children=[
                            dbc.Col(
                                children=[
                                    dbc.InputGroup(
                                        children=[
                                            dbc.InputGroupText(
                                                children='Future Quantity Token 2',
                                                class_name='w-50'
                                            ),
                                            dbc.Input(id="token-2-future-qty", type="number", disabled=True),
                                        ],
                                    ),
                                ],
                                class_name=''
                            ),
                        ],
                        class_name='m-1'
                    ),
                    # Future token price row
                    dbc.Row(
                        children=[
                            dbc.Col(
                                children=[
                                    dbc.InputGroup(
                                        children=[
                                            dbc.InputGroupText(
                                                children='Token 1 Price',
                                                class_name=''
                                            ),
                                            dbc.Input(id="token-1-future-price", type='number'),
                                            dbc.InputGroupText(
                                                children='Token 2 Price',
                                                class_name=''
                                            ),
                                            dbc.Input(id="token-2-future-price", type='number'),
                                        ],
                                    ),
                                ],
                                class_name=''
                            ),
                        ],
                        class_name='m-1'
                    ),
                    # Total Value Before Interest Row
                    dbc.Row(
                        children=[
                            dbc.Col(
                                children=[
                                    dbc.InputGroup(
                                        children=[
                                            dbc.InputGroupText('Total Value Before Interest'),
                                            #dbc.InputGroupText('$'),
                                            dbc.Input(id="total-value-before-interest", disabled=True),
                                        ],
                                        class_name=''
                                    ),
                                ],
                                class_name=''
                            ),
                        ],
                        class_name='m-1'
                    ),
                    # Value if held row
                    dbc.Row(
                        children=[
                            dbc.Col(
                                children=[
                                    dbc.InputGroup(
                                        children=[
                                            dbc.InputGroupText(
                                                children='Token 1 If Held',
                                                class_name=''
                                            ),
                                            dbc.Input(id="token-1-held", disabled=True),
                                            dbc.InputGroupText(
                                                children='Token 2 If Held',
                                                class_name=''
                                            ),
                                            dbc.Input(id="token-2-held", disabled=True),
                                            dbc.InputGroupText(
                                                children='Total If Held',
                                                class_name=''
                                            ),
                                            dbc.Input(id="total-held", disabled=True),
                                        ],
                                    ),
                                ],
                                class_name=''
                            ),
                        ],
                        class_name='m-1'
                    ),
                    # Impermanent Loss row
                    dbc.Row(
                        children=[
                            dbc.Col(
                                children=[
                                    dbc.InputGroup(
                                        children=[
                                            dbc.InputGroupText(
                                                children='Impermanent Loss',
                                                class_name=''
                                            ),
                                            dbc.Input(id="il-percent", disabled=True),
                                            dbc.InputGroupText(
                                                children='%',
                                                class_name=''
                                            ),
                                            dbc.InputGroupText(
                                                children='$',
                                                class_name=''
                                            ),
                                            dbc.Input(id="il-dollar", disabled=True),

                                        ],
                                    ),
                                ],
                                class_name=''
                            ),
                        ],
                        class_name='m-1'
                    ),
                    # Interest Earned row
                    dbc.Row(
                        children=[
                            dbc.Col(
                                children=[
                                    dbc.InputGroup(
                                        children=[
                                            dbc.InputGroupText(
                                                children='Interest Earned',
                                                class_name=''
                                            ),
                                            dbc.Input(id="int-percent", disabled=True),
                                            dbc.InputGroupText(
                                                children='%',
                                                class_name=''
                                            ),
                                            dbc.InputGroupText(
                                                children='$',
                                                class_name=''
                                            ),
                                            dbc.Input(id="int-dollar", disabled=True),

                                        ],
                                    ),
                                ],
                                class_name=''
                            ),
                        ],
                        class_name='m-1'
                    ),
                    # Total Value w/ interest + Difference row
                    dbc.Row(
                        children=[
                            dbc.Col(
                                children=[
                                    dbc.InputGroup(
                                        children=[
                                            dbc.InputGroupText(
                                                children='Total Value + Interest',
                                                class_name=''
                                            ),
                                            dbc.Input(id="value-interest", disabled=True),
                                            dbc.InputGroupText(
                                                children='Difference Vs Holding',
                                                class_name=''
                                            ),
                                            dbc.Input(id="diff-vs-hold", disabled=True),
                                        ],
                                    ),
                                ],
                                class_name=''
                            ),
                        ],
                        class_name='m-1'
                    ),
                ],
                class_name='m-1 p-1 border rounded bg-secondary',
            ),
        ],
        class_name=''
    ),
])

#############
# Callbacks #
#############

def get_coin_price(coin_id, date):
    coin_price = cg.get_coin_history_by_id(
        id=coin_id,
        date=date,
        localization=False
    )
    return coin_price['market_data']['current_price']['usd']


@app.callback(
    Output('token-1-price', 'value'),
    Output('token-2-price', 'value'),
    Output('token-2-qty', 'value'),
    Output('total-value', 'value'),
    Input('date-picker-start', 'date'),
    Input('token-dropdown-1', 'value'),
    Input('token-dropdown-2', 'value'),
    Input('token-1-qty', 'value'),
    #prevent_initial_call=True
)
# TODO: what if date is before token existed?
def update_token_1_price(date_value, token_1_name, token_2_name, token_1_qty):
    date_object = date.fromisoformat(date_value)
    date_string = date_object.strftime('%d-%m-%Y')
    if token_1_name is not None and token_2_name is None and token_1_qty is None:
        token_1_price = round(get_coin_price(coin_id=token_1_name, date=date_string), 2)
        return f'${token_1_price:,.2f}', '$0.00', '0', '$0.00'
    elif token_1_name is not None and token_2_name is not None and token_1_qty is None:
        token_1_price = round(get_coin_price(coin_id=token_1_name, date=date_string), 2)
        token_2_price = round(get_coin_price(coin_id=token_2_name, date=date_string), 2)
        return f'${token_1_price:,.2f}', f'${token_2_price:,.2f}', '0', '$0.00'
    elif token_1_name is not None and token_2_name is not None and token_1_qty is not None:
        token_1_price = round(get_coin_price(coin_id=token_1_name, date=date_string), 2)
        token_2_price = round(get_coin_price(coin_id=token_2_name, date=date_string), 2)
        token_2_qty = (token_1_price * token_1_qty) / token_2_price
        total_value = (token_1_price * token_1_qty) + (token_2_price * token_2_qty)
        return f'${token_1_price:,.2f}', f'${token_2_price:,.2f}', f'{token_2_qty:,.2f}', f'${total_value:,.2f}'
    else:
        return '$0.00', '$0.00', '0', '$0.00'

@app.callback(
    Output('token-1-future-qty', 'value'),
    Output('token-2-future-qty', 'value'),
    Output('total-value-before-interest', 'value'),
    Output('token-1-held', 'value'),
    Output('token-2-held', 'value'),
    Output('total-held', 'value'),
    Input('token-1-qty', 'value'),
    Input('token-2-qty', 'value'),
    Input('token-1-future-price', 'value'),
    Input('token-2-future-price', 'value'),
)
def calc_future_qty(token_1_qty, token_2_qty, token_1_future_price, token_2_future_price):
    if (token_1_qty is not None
        and token_2_qty is not None
        and token_1_future_price is not None
        and token_2_future_price is not None
    ):
        product_constant = token_1_qty * float(token_2_qty)
        future_price_ratio = float(token_1_future_price) / float(token_2_future_price)
        token_1_future_qty = (product_constant / future_price_ratio) ** 0.5
        token_2_future_qty = (product_constant * future_price_ratio) ** 0.5
        total_val_before_int = (token_1_future_price * token_1_future_qty) + (token_2_future_price * token_2_future_qty)
        token_1_held = float(token_1_qty) * token_1_future_price
        token_2_held = float(token_2_qty) * token_2_future_price
        total_if_held = token_1_held + token_2_held
        return (token_1_future_qty, token_2_future_qty, f'${total_val_before_int:.2f}', f'${token_1_held:.2f}',
                f'${token_2_held:.2f}', f'${total_if_held:.2f}')
    else:
        return 0, 0, 0, 0, 0, 0
