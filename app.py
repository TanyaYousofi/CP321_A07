import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

app = Dash(__name__)
server = app.server  # for deployment

# Full dataset
data = [
    {'Year': 1930, 'Winner': 'Uruguay', 'RunnerUp': 'Argentina'},
    {'Year': 1934, 'Winner': 'Italy', 'RunnerUp': 'Czechoslovakia'},
    {'Year': 1938, 'Winner': 'Italy', 'RunnerUp': 'Hungary'},
    {'Year': 1950, 'Winner': 'Uruguay', 'RunnerUp': 'Brazil'},
    {'Year': 1954, 'Winner': 'Germany', 'RunnerUp': 'Hungary'},
    {'Year': 1958, 'Winner': 'Brazil', 'RunnerUp': 'Sweden'},
    {'Year': 1962, 'Winner': 'Brazil', 'RunnerUp': 'Czechoslovakia'},
    {'Year': 1966, 'Winner': 'England', 'RunnerUp': 'Germany'},
    {'Year': 1970, 'Winner': 'Brazil', 'RunnerUp': 'Italy'},
    {'Year': 1974, 'Winner': 'Germany', 'RunnerUp': 'Netherlands'},
    {'Year': 1978, 'Winner': 'Argentina', 'RunnerUp': 'Netherlands'},
    {'Year': 1982, 'Winner': 'Italy', 'RunnerUp': 'Germany'},
    {'Year': 1986, 'Winner': 'Argentina', 'RunnerUp': 'Germany'},
    {'Year': 1990, 'Winner': 'Germany', 'RunnerUp': 'Argentina'},
    {'Year': 1994, 'Winner': 'Brazil', 'RunnerUp': 'Italy'},
    {'Year': 1998, 'Winner': 'France', 'RunnerUp': 'Brazil'},
    {'Year': 2002, 'Winner': 'Brazil', 'RunnerUp': 'Germany'},
    {'Year': 2006, 'Winner': 'Italy', 'RunnerUp': 'France'},
    {'Year': 2010, 'Winner': 'Spain', 'RunnerUp': 'Netherlands'},
    {'Year': 2014, 'Winner': 'Germany', 'RunnerUp': 'Argentina'},
    {'Year': 2018, 'Winner': 'France', 'RunnerUp': 'Croatia'},
    {'Year': 2022, 'Winner': 'Argentina', 'RunnerUp': 'France'}
]

df = pd.DataFrame(data)
df['Winner'] = df['Winner'].replace('West Germany', 'Germany')
df['RunnerUp'] = df['RunnerUp'].replace('West Germany', 'Germany')

winners_count = df['Winner'].value_counts().reset_index()
winners_count.columns = ['Country', 'Wins']

app.layout = html.Div([
    html.H1("FIFA World Cup Dashboard", style={'textAlign': 'center'}),

    dcc.Dropdown(
        id='country-dropdown',
        options=[{'label': c, 'value': c} for c in winners_count['Country']],
        placeholder="Select a country"
    ),
    html.Div(id='country-output', style={'margin': '10px'}),

    dcc.Dropdown(
        id='year-dropdown',
        options=[{'label': y, 'value': y} for y in sorted(df['Year'].unique())],
        placeholder="Select a year"
    ),
    html.Div(id='year-output', style={'margin': '10px'}),

    dcc.Graph(id='choropleth-map')
])

@app.callback(
    Output('country-output', 'children'),
    Input('country-dropdown', 'value')
)
def show_wins(country):
    if country:
        wins = winners_count[winners_count['Country'] == country]['Wins'].values[0]
        return f"{country} has won the World Cup {wins} times."
    return ""

@app.callback(
    Output('year-output', 'children'),
    Input('year-dropdown', 'value')
)
def show_year_result(year):
    if year:
        row = df[df['Year'] == year].iloc[0]
        return f"In {year}, {row['Winner']} won and {row['RunnerUp']} was runner-up."
    return ""

@app.callback(
    Output('choropleth-map', 'figure'),
    Input('country-dropdown', 'value')
)
def update_map(selected_country):
    fig = px.choropleth(
        winners_count,
        locations='Country',
        locationmode='country names',
        color='Wins',
        hover_name='Country',
        color_continuous_scale='Blues',
        title='World Cup Wins by Country'
    )
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
