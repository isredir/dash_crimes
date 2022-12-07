from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd

df = pd.read_csv('crimedata.csv')
df['medFamInc_with_step'] = df['medFamInc'] - df['medFamInc'] % 1000

states_df = df.groupby(['state']).agg({"racepctblack": 'mean', 'racePctWhite': 'mean',
                                       'racePctAsian': 'mean', 'racePctHisp': 'mean',
                                       'murders': 'sum', 'rapes': 'sum', 'robberies': 'sum',
                                       'assaults': 'sum', 'burglaries': 'sum', 'larcenies': 'sum', 'autoTheft': 'sum',
                                       'arsons': 'sum'}).reset_index()

df['crimes'] = df['murders'] + df['rapes'] + df['robberies'] + df['assaults'] + df['burglaries'] + df['autoTheft'] + df[
    'arsons']

autoThefts_incomes_state_df = df.groupby(['state', 'medFamInc_with_step']).agg({"autoTheft": 'mean'}).reset_index()

crime_names = ['Murders', 'Rapes', 'Robberies', 'Assaults', 'Burglaries', 'Larcenies', 'Arsons', 'Auto Thefts']


def get_crime(user_selected_crime):
    if user_selected_crime == 'Murders':
        selected_crime = 'murders'
    elif user_selected_crime == 'Rapes':
        selected_crime = 'rapes'
    elif user_selected_crime == 'Robberies':
        selected_crime = 'robberies'
    elif user_selected_crime == 'Assaults':
        selected_crime = 'assaults'
    elif user_selected_crime == 'Burglaries':
        selected_crime = 'burglaries'
    elif user_selected_crime == 'Larcenies':
        selected_crime = 'larcenies'
    elif user_selected_crime == 'Auto Thefts':
        selected_crime = 'autoTheft'
    elif user_selected_crime == 'Arsons':
        selected_crime = 'arsons'
    return selected_crime


colors = {
    'black': '#111111',
    'white': '#FFFFFF',
    'text': '#7FDBFF',
    'paper_bgcolor_1': '#008B92',
    'plot_bgcolor_1': '#B7D5FE',
    'paper_bgcolor_2': '#D01120',
    'plot_bgcolor_2': '#E7C5C6',
    'plot_bgcolor_3': '#E9F4FF',
    'plot_bgcolor_4': '#FFF1FA'
}

app = Dash(__name__)

app.layout = html.Div([
    html.Br(),
    html.Label(['City:'], style={'font-weight': 'bold', "text-align": "center"}),
    dcc.Dropdown(df['communityName'], df['communityName'][0], id='city_races_in'),
    dcc.Graph(id='city_races_out'),

    html.Br(),
    html.Label(['State:'], style={'font-weight': 'bold', "text-align": "center"}),
    dcc.Dropdown(states_df['state'], states_df['state'][0], id='state_races_in'),
    dcc.Graph(id='state_races_out'),

    html.Br(),
    html.Label(['City:'], style={'font-weight': 'bold', "text-align": "center"}),
    dcc.Dropdown(df['communityName'], df['communityName'][0], id='city_crimes_in'),
    dcc.Graph(id='city_crimes_out'),

    html.Br(),
    html.Label(['State:'], style={'font-weight': 'bold', "text-align": "center"}),
    dcc.Dropdown(states_df['state'], states_df['state'][0], id='states_crimes_in'),
    dcc.Graph(id='states_crimes_out'),

    html.Br(),
    html.Label(['Crime:'], style={'font-weight': 'bold', "text-align": "center"}),
    dcc.Dropdown(crime_names, crime_names[0], id='crimes_states_in'),
    dcc.Graph(id='crimes_states_out'),

    html.Br(),
    html.Label(['Crime:'], style={'font-weight': 'bold', "text-align": "center"}),
    dcc.Dropdown(crime_names, crime_names[0], id='crimes_population_in'),
    dcc.Graph(id='crimes_population_out'),

    html.Br(),
    html.Label(['Crime:'], style={'font-weight': 'bold', "text-align": "center"}),
    dcc.Dropdown(crime_names, crime_names[0], id='crimes_income_in'),
    dcc.Graph(id='crimes_income_out'),

    html.Br(),
    html.Label(['Crime:'], style={'font-weight': 'bold', "text-align": "center"}),
    dcc.Dropdown(crime_names, crime_names[0], id='crimes_urban_in'),
    dcc.Graph(id='crimes_urban_out')
])


@app.callback(
    Output(component_id='city_races_out', component_property='figure'),
    [Input(component_id='city_races_in', component_property='value')]
)
def update_output(selected_community):
    community_df = df[df.communityName == selected_community]
    community_df = community_df.iloc[0]
    fig = px.pie(community_df, names=['Black', 'White', 'Asian', 'Hisp'],
                 values=[community_df['racepctblack'], community_df['racePctWhite'],
                         community_df['racePctAsian'], community_df['racePctHisp']])

    fig.update_layout(title=f"Race ratio in {selected_community}",
                      plot_bgcolor=colors['plot_bgcolor_3'],
                      paper_bgcolor=colors['plot_bgcolor_3'],
                      font_color=colors['black'])
    return fig


@app.callback(
    Output(component_id='state_races_out', component_property='figure'),
    [Input(component_id='state_races_in', component_property='value')]
)
def update_output(selected_state):
    state_df = states_df[states_df.state == selected_state]
    state_df = state_df.iloc[0]
    fig = px.pie(state_df, names=['Black', 'White', 'Asian', 'Hisp'],
                 values=[state_df['racepctblack'], state_df['racePctWhite'],
                         state_df['racePctAsian'], state_df['racePctHisp']])

    fig.update_layout(title=f"Race ratio {selected_state}",
                      plot_bgcolor=colors['plot_bgcolor_4'],
                      paper_bgcolor=colors['plot_bgcolor_4'],
                      font_color=colors['black'])
    return fig


@app.callback(
    Output(component_id='city_crimes_out', component_property='figure'),
    [Input(component_id='city_crimes_in', component_property='value')]
)
def update_output(selected_community):
    community_df = df[df.communityName == selected_community]
    community_df = community_df.iloc[0]
    fig = px.histogram(community_df,
                       x=['Murders', 'Rapes', 'Robberies', 'Assaults', 'Burglaries', 'Larcenies',
                          'Auto Thefts', 'Arsons'],
                       y=[community_df['murders'], community_df['rapes'], community_df['robberies'],
                          community_df['assaults'], community_df['burglaries'], community_df['larcenies'],
                          community_df['autoTheft'], community_df['arsons']])

    fig.update_layout(yaxis_title="Crime number",
                      xaxis_title="Crimes",
                      title=f"Crime ratio in {selected_community}",
                      plot_bgcolor=colors['plot_bgcolor_3'],
                      paper_bgcolor=colors['plot_bgcolor_3'],
                      font_color=colors['black'])
    return fig


@app.callback(
    Output(component_id='states_crimes_out', component_property='figure'),
    [Input(component_id='states_crimes_in', component_property='value')]
)
def update_output(selected_state):
    state_df = states_df[states_df.state == selected_state]
    state_df = state_df.iloc[0]
    fig = px.histogram(state_df,
                       x=['Murders', 'Rapes', 'Robberies', 'Assaults', 'Burglaries', 'Larcenies',
                          'Auto Thefts', 'Arsons'],
                       y=[state_df['murders'], state_df['rapes'], state_df['robberies'],
                          state_df['assaults'], state_df['burglaries'], state_df['larcenies'],
                          state_df['autoTheft'], state_df['arsons']])

    fig.update_layout(yaxis_title="Crime number",
                      xaxis_title="Crimes",
                      title=f"Crime ratio in {selected_state}",
                      plot_bgcolor=colors['plot_bgcolor_4'],
                      paper_bgcolor=colors['plot_bgcolor_4'],
                      font_color=colors['black'])
    return fig


@app.callback(
    Output(component_id='crimes_states_out', component_property='figure'),
    [Input(component_id='crimes_states_in', component_property='value')]
)
def update_output(user_selected_crime):
    selected_crime = get_crime(user_selected_crime)
    crimes_data = df.groupby(['state']).agg({selected_crime: 'sum'}).reset_index()
    fig = px.histogram(crimes_data, x='state', y=selected_crime)
    fig.update_layout(xaxis_title="State",
                      yaxis_title=f"{user_selected_crime}",
                      title=f"{user_selected_crime} number in different states",
                      plot_bgcolor=colors['plot_bgcolor_1'],
                      paper_bgcolor=colors['paper_bgcolor_1'],
                      font_color=colors['white']
                      )
    return fig


df = df.sort_values('population')


@app.callback(
    Output(component_id='crimes_population_out', component_property='figure'),
    [Input(component_id='crimes_population_in', component_property='value')]
)
def update_output(user_selected_crime):
    selected_crime = get_crime(user_selected_crime)
    fig = px.line(df, x='population', y=selected_crime)
    fig.update_layout(xaxis_title="Population",
                      yaxis_title=f"{user_selected_crime} number",
                      title=f"{user_selected_crime} number to population ratio",
                      xaxis_range=[0, 1000000],
                      plot_bgcolor=colors['plot_bgcolor_2'],
                      paper_bgcolor=colors['paper_bgcolor_2'],
                      font_color=colors['white']
                      )
    return fig


@app.callback(
    Output(component_id='crimes_income_out', component_property='figure'),
    [Input(component_id='crimes_income_in', component_property='value')]
)
def update_output(user_selected_crime):
    selected_crime = get_crime(user_selected_crime)
    crimes_data = df.groupby(['medFamInc_with_step']).agg({selected_crime: 'mean'}).reset_index()
    fig = px.line(crimes_data, x='medFamInc_with_step', y=selected_crime)
    fig.update_layout(xaxis_title="Income (with step of 1000 USD)",
                      yaxis_title=f"Mean {user_selected_crime} number",
                      title=f"{user_selected_crime} number to family income ratio",
                      plot_bgcolor=colors['plot_bgcolor_2'],
                      paper_bgcolor=colors['paper_bgcolor_2'],
                      font_color=colors['white']
                      )
    return fig


@app.callback(
    Output(component_id='crimes_urban_out', component_property='figure'),
    [Input(component_id='crimes_urban_in', component_property='value')]
)
def update_output(user_selected_crime):
    selected_crime = get_crime(user_selected_crime)
    crimes_data = df.groupby(['pctUrban']).agg({selected_crime: 'mean'}).reset_index()
    fig = px.line(crimes_data, x='pctUrban', y=selected_crime)
    fig.update_layout(xaxis_title="Urban population percent",
                      yaxis_title=f"Mean {user_selected_crime} number",
                      title=f"{user_selected_crime} number to urban population percent ratio",
                      plot_bgcolor=colors['plot_bgcolor_1'],
                      paper_bgcolor=colors['paper_bgcolor_1'],
                      font_color=colors['white']
                      )
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
