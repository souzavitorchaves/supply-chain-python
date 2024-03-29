# importing libraries for data and graph
import pandas as pd
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go
pio.templates.deafult = "plotly_white"
     

# mounting drive files and loading data
from google.colab import drive

drive.mount('/content/drive', force_remount=True)
data = pd.read_csv('/content/drive/My Drive/Projects/supply_chain/supply_chain_data.csv')
print(data.head())
     

# generate stats from the data topics
print(data.describe())

# grafico de dispersão
# generates a Scatter Graph with some stats, the goal is to know who generates more revenue as the price increase
fig = px.scatter(data, x='Price',
                 y='Revenue generated',
                 color="Product type",
                 hover_data=['Number of products sold'],
                 trendline="ols")
fig.show()
#plot1.png
     

# grafico de pizza
# pie chart to look which type of product sells the most
sales_data = data.groupby('Product type')['Number of products sold'].sum().reset_index()
pie_chart = px.pie(sales_data, values='Number of products sold', names='Product type',
                  title='Sales by Producy Type',
                  hover_data=['Number of products sold'],
                  hole=0.4,
                  color_discrete_sequence=px.colors.qualitative.Pastel)
pie_chart.update_traces(textposition='inside', textinfo='percent+label')
pie_chart.show()
#plot2.png
     

# grafico de barra
# this graph shows which carrier generates more revenue
total_revenue = data.groupby('Shipping carriers')['Revenue generated'].sum().reset_index()
print(total_revenue.head())
fig = go.Figure()
fig.add_trace(go.Bar(x=total_revenue['Shipping carriers'], #acess df and look to the column with the name 'Shipping carriers'
                     y=total_revenue['Revenue generated']))
fig.update_layout(title='Total Revenue by Shipping Carrier',
                  xaxis_title='Shipping Carrier',
                  yaxis_title='Revenue Generated')
fig.show()
#plot3.png


# shows the avg time of whuch product and your avg cost
avg_lead_time = data.groupby('Product type')['Lead time'].mean().reset_index() #media - procv
avg_manufacturing_costs = data.groupby('Product type')['Manufacturing costs'].mean().reset_index() #media - procv
result = pd.merge(avg_lead_time, avg_manufacturing_costs, on='Product type')
# the row below change the name of the columns of the df generated
result.rename(columns={'Lead time': 'Average Lead Time', 'Manufacturing costs': 'Average Manufacturing costs'}, inplace=True)
print(result)


# line graph that shows the revenue by SKU
revenue_chart = px.line(data, x='SKU', # stock keeping units
                        y='Revenue generated',
                        title='Revenue Generated by SKU')
revenue_chart.show()
#plot4.png
     

# descending revenue by SKU chart, i've sorted to see tendencies easily
sorted_data = data.sort_values(by=['Revenue generated'],ascending=False)
revenue_chart = px.line(sorted_data, x='SKU', # stock keeping units
                        y='Revenue generated',
                        title='Sorted Revenue Generated by SKU')
revenue_chart.show()
#plot5.png
     

# line graph to show stock level by SKU
stock_chart = px.line(data, x='SKU',
                      y='Stock levels',
                      title='Stock Levels by SKU')
stock_chart.show()
#plot6.png
     

# order by SKU
order_quantity_chart = px.bar(data, x='SKU',
                              y='Order quantities',
                              title='Order Quantity by SKU')
order_quantity_chart.show()
#plot7.png
     

# ascending order by sku
sorted_data = data.sort_values(by=['Order quantities'],ascending=True)
order_quantity_chart = px.bar(sorted_data, x='SKU',
                              y='Order quantities',
                              title='Sorted Order Quantity by SKU')
order_quantity_chart.show()
#plot8.png
     

# shipping cost by carrier, we've found out that the most prolific carrier it's also the most expensive
shipping_cost_chart = px.bar(data, x='Shipping carriers',
                             y='Shipping costs',
                             title='Shipping Costs by Carrier')
shipping_cost_chart.show()
#plot9.png
     

# cost distribution by transporation mode in a pie chart
transportation_chart = px.pie(data,
                              values='Costs',
                              names='Transportation modes',
                              title='Cost Distribuition by Transportation Mode',
                              hole=0.3,
                              color_discrete_sequence=px.colors.qualitative.Pastel1)
transportation_chart.show()
#plot10.png
     

# right here we get to know the defect rate for each product that we have
defect_rates_by_product = data.groupby('Product type')['Defect rates'].mean().reset_index()
fig = px.bar(defect_rates_by_product,
             x='Product type',
             y='Defect rates',
             title='Average  Defect Rates by Product Type')
fig.show()
#plot11.png
     

# pie chart with Defect rate by transportation mode
pivot_table = pd.pivot_table(data, values='Defect rates', #column 1
                             index=['Transportation modes'], #column 0 (i've printed below)
                             aggfunc='mean')
transportation_chart = px.pie(values=pivot_table['Defect rates'],
                              names=pivot_table.index, # index will gonna be 'Transporation modes
                              title='Defect Rates by Transporatation Modes',
                              hole=0.4,
                              color_discrete_sequence=px.colors.qualitative.Pastel)
print(pivot_table.head())
transportation_chart.show()
#plot12.png