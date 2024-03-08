import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st 

DF = pd.read_csv('CleanData.csv')
usTotals = DF[DF['STATE'] == 'US-TOTAL']

colorDict = {'Total':'Plasma', 
            'Coal': 'Thermal', 
            'Hydroelectric Conventional': 'Ice', 
            'Natural Gas':'Dense_r',
            'Wind':'Mint_r', 
            'Nuclear': 'Speed_r',
            'Solar Thermal and Photovoltaic':'Solar'
            }

st.title('US Energy Geneartion')
totalProduction, sourcePercents, usTrends, dataSource = st.tabs(['Total Generation', 
                                                                'Source Percentages',
                                                                'US Trends',
                                                                'Data Source'
                                                                 ])
with totalProduction:

    st.markdown('The chloropleth map displayed below visualizes the total energy produced by each state for the selected energy source and year.')

    source1 = st.selectbox('Energy Source', DF['ENERGY SOURCE'].unique(), key='source1')
    scaleMax1 = DF[DF['STATE'] != 'US-TOTAL'].copy()
    scaleMax1 = scaleMax1[(scaleMax1['ENERGY SOURCE'] == source1)]['MWh'].max()


    year1 = st.slider('Select a Year', 
                    min_value=1990,
                    max_value=2022,
                    value=2000,
                    key='year1'
                    )


    dfGraph1 = DF[(DF['YEAR'] == year1) & (DF['ENERGY SOURCE'] == source1)]

    graph1 = px.choropleth(dfGraph1, 
                        color='MWh', 
                        locations='STATE',  
                        locationmode='USA-states', 
                        scope='usa', 
                        range_color=[0,scaleMax1],
                        color_continuous_scale=colorDict[source1],
                        )

    graph1.update_layout(geo=dict(bgcolor='rgba(0,0,0,0)'))

    st.plotly_chart(graph1)

with sourcePercents:

    st.markdown("The chloropleth map below displays the percentage of each state's energy generation derived from the selected energy source for the chosen year.")

    sourceList = DF['ENERGY SOURCE'].unique()
    sourceList = sourceList[sourceList != 'Total']
    source2 = st.selectbox('Energy Source', 
                            sourceList, 
                            key='source2'
                            )
    year2 = st.slider('Select a Year', 
                    min_value=1990,
                    max_value=2022,
                    value=2000,
                    key='year2'
                    )

    dfGraph2 = DF[(DF['YEAR'] == year2) & (DF['ENERGY SOURCE'] == source2)]

    graph2 = px.choropleth(dfGraph2, 
                        color='Percent', 
                        locations='STATE',  
                        locationmode='USA-states', 
                        scope='usa', 
                        range_color=[0,100],
                        color_continuous_scale=colorDict[source2],
                        )

    graph2.update_layout(geo=dict(bgcolor='rgba(0,0,0,0)'))

    st.plotly_chart(graph2)

with usTrends:
    st.markdown('The graph below illustrates how the selected energy sources contribute to the total energy production of the United States for the chosen year, expressed as percentages.')

    usLeft, usRight = st.columns(2)
    with usLeft:
        coalBox = st.checkbox('Coal')
        gasBox = st.checkbox('Natural Gas')
        nuclearBox = st.checkbox('Nuclear')
    with usRight:    
        windBox = st.checkbox('Wind')
        hydroBox = st.checkbox('Hydroelectric')
        solarBox = st.checkbox('Solar')

    st.markdown('---')
    lineSources = []
    if windBox: lineSources.append('Wind')
    if solarBox: lineSources.append('Solar Thermal and Photovoltaic')
    if gasBox: lineSources.append('Natural Gas')
    if nuclearBox: lineSources.append('Nuclear')
    if coalBox: lineSources.append('Coal')
    if hydroBox: lineSources.append('Hydroelectric Conventional')

    line1ColorMap = {'Wind' : 'cyan',
                     'Solar Thermal and Photovoltaic' : 'yellow',
                     'Natural Gas' : 'purple',
                     'Nuclear' : 'green',
                     'Coal' : 'gray',
                     'Hydroelectric Conventional' : 'blue'
                     }

    usTotalsFiltered = usTotals[usTotals['ENERGY SOURCE'].isin(lineSources)]

  

    line1=px.line(usTotalsFiltered, 
                  x='YEAR',
                  y='Percent',
                  color=('ENERGY SOURCE'),
                  color_discrete_map=line1ColorMap,
                  )
    
    line1.update_layout(yaxis_range=[0, 100],
                        legend=dict(orientation='h',
                                     y=105,
                                    ),          
                        )

    st.plotly_chart(line1)

    st.markdown('---')
    st.markdown('DISCLAIMER: there are some eneregy sources not covered in this project, so the totals will not add up to 100%')

with dataSource:
    st.markdown('''I used the "Net Generation by State by Type of Producer by Energy Source" XLS file 
                from the [EIA website](https://www.eia.gov/electricity/data/state/).''')