import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from model import ModelPriceOfferInputs, ModelExchangeInputs
from model import ModelAdjusterInputs
from model import ModelPriceInputs
from model import ModelTechnicalInputs
from model import ModelMacroInputs
from function import convert_price_to_currency, calculate_total_steel_adjustment, calculate_total_bunker_adjustment, calculate_total_material_adjustment,calculate_total_cpi_adjustment




# Sidebar Inputs
st.sidebar.header("User Input Parameters")


# Input for the number of turbines
turbine_mw = st.sidebar.number_input("Enter the MW per Turbine", min_value=1, value=15, step=1)
No_of_Turbine = st.sidebar.number_input("Enter the Number of Turbines", min_value=1, value=34, step=1)


# Dropdown for target currency
target_currency = st.sidebar.selectbox("Select Target Currency", options=["USD", "EUR"])
st.sidebar.markdown("<hr>", unsafe_allow_html=True)

st.sidebar.header("Input the Price Offer")


with st.sidebar:
    col1, col2, col3 = st.columns(3)  # Create 3 columns

    # Price input in USD
    with col1:
        st.header("in USD")
        price_in_usd = st.number_input(
            " ",  # Empty label to avoid clutter
            min_value=0.0,
            value=502500000.0,
            step=10000.0,
            format="%.2f",
            key="price_usd",
            label_visibility="collapsed"  # Hide label to make input more compact
        )

    # Price input in EUR
    with col2:
        st.header("in EUR")
        price_in_eur = st.number_input(
            " ",
            min_value=0.0,
            value=252000000.0,
            step=10000.0,
            format="%.2f",
            key="price_eur",
            label_visibility="collapsed"
        )

    # Price input in KRW
    with col3:
        st.header("in KRW")
        price_in_krw = st.number_input(
            " ",
            min_value=0.0,
            value=109746422435.0,
            step=1000000.0,
            format="%.2f",
            key="price_krw",
            label_visibility="collapsed"
        )

    # Display the inputs as a table in a box
    st.sidebar.write("### Breakdown of Price Offer")
    st.sidebar.table({
        "Currency": ["USD", "EUR", "KRW"],
        "Price": [
            f"${price_in_usd:,.2f}",
            f"€{price_in_eur:,.2f}",
            f"₩{price_in_krw:,.2f}"
        ]
    })

    model_price_offer_data =ModelPriceOfferInputs(price_in_usd,price_in_eur,price_in_krw)

    # Sidebar - Exchange Rate Box
st.sidebar.header("Input the Exchange Rates")
st.sidebar.markdown("<hr>", unsafe_allow_html=True)

# Create another container for exchange rates input
with st.sidebar:
    # Input exchange rate for EUR to USD
    eur_to_usd = st.number_input(
        "EUR to USD",
        min_value=0.0,
        value=1.06319,
        step=0.0001,
        format="%.5f",
        key="eur_to_usd"
    )

    # Input exchange rate for EUR to KRW
    eur_to_krw = st.number_input(
        "EUR to KRW",
        min_value=0.0,
        value=1428.57,
        step=1.0,
        format="%.2f",
        key="eur_to_krw"
    )

    # Input exchange rate for USD to KRW
    usd_to_krw = st.number_input(
        "USD to KRW",
        min_value=0.0,
        value=1343.66,
        step=1.0,
        format="%.2f",
        key="usd_to_krw"
    )

    # Instantiate the class with the user input values
    model_exchange_data = ModelExchangeInputs(eur_to_usd, eur_to_krw, usd_to_krw)        








# Sidebar Inputs for Adjusters
st.sidebar.header("Adjuster Inputs")

# Create sliders for adjuster values in the sidebar
weight_flange_adjuster = st.sidebar.slider(
    "Weight Flange (%)",
    min_value=0,
    max_value=100,
    value=7,  # Default value
    step=1
)

weight_shell_adjuster = st.sidebar.slider(
    "Weight Shell (%)",
    min_value=0,
    max_value=100,
    value=7,  # Default value
    step=1
)

weight_bunker_adjuster = st.sidebar.slider(
    "Weight Bunker (%)",
    min_value=0,
    max_value=100,
    value=7,  # Default value
    step=1
)

steel_price_adjuster = st.sidebar.slider(
    "Steel Price (%)",
    min_value=0,
    max_value=100,
    value=7,  # Default value
    step=1
)

castiron_price_adjuster = st.sidebar.slider(
    "CastIron Price (%)",
    min_value=0,
    max_value=100,
    value=7,  # Default value
    step=1
)

resin_price_adjuster = st.sidebar.slider(
    "Resin Price (%)",
    min_value=0,
    max_value=100,
    value=7,  # Default value
    step=1
)

HotRolledCoils_price_adjuster = st.sidebar.slider(
    "Hot Rolled Coils Price (%)",
    min_value=0,
    max_value=100,
    value=2,  # Default value
    step=1
)

bunker_price_adjuster = st.sidebar.slider(
    "Bunker Price (%)",
    min_value=0,
    max_value=100,
    value=2,  # Default value
    step=1
)

cpi_eur_adjuster = st.sidebar.slider(
    "CPI EUR (%)",
    min_value=0,
    max_value=100,
    value=3,  # Default value
    step=1
)

cpi_us_adjuster = st.sidebar.slider(
    "CPI US (%)",
    min_value=0,
    max_value=100,
    value=5,  # Default value
    step=1
)

# Convert sliders' percentage values into decimal form for internal calculations
weight_flange_adjuster = weight_flange_adjuster / 100
weight_shell_adjuster = weight_shell_adjuster / 100
weight_bunker_adjuster = weight_bunker_adjuster / 100
steel_price_adjuster = steel_price_adjuster / 100
castiron_price_adjuster = castiron_price_adjuster / 100
resin_price_adjuster = resin_price_adjuster / 100
HotRolledCoils_price_adjuster = HotRolledCoils_price_adjuster / 100
bunker_price_adjuster = bunker_price_adjuster / 100
cpi_eur_adjuster = cpi_eur_adjuster / 100
cpi_us_adjuster = cpi_us_adjuster / 100


# Now, instantiate the ModelAdjusterInputs class with the values from sliders
model_adjuster_data = ModelAdjusterInputs(
    weight_flange_adjuster,
    weight_shell_adjuster,
    weight_bunker_adjuster,
    steel_price_adjuster,
    castiron_price_adjuster,
    resin_price_adjuster,
    HotRolledCoils_price_adjuster,
    bunker_price_adjuster,
    cpi_eur_adjuster,
    cpi_us_adjuster
)

# Display the adjusted values in the sidebar for the user to confirm
adjuster_names = [
    "Weight Flange", "Weight Shell", "Weight Bunker", 
    "Steel Price", "CastIron Price", "Resin Price", 
    "Hot Rolled Coils Price", "Bunker Price", 
    "CPI EUR", "CPI US"
]

adjuster_values = [
    weight_flange_adjuster, weight_shell_adjuster, weight_bunker_adjuster, 
    steel_price_adjuster, castiron_price_adjuster, resin_price_adjuster, 
    HotRolledCoils_price_adjuster, bunker_price_adjuster, 
    cpi_eur_adjuster, cpi_us_adjuster
]

# Create a DataFrame
df_adjusters = pd.DataFrame({
    "Adjuster": adjuster_names,
    "Value (%)": adjuster_values
})

# Create a high-resolution bar chart using matplotlib

plt.figure(figsize=(12, 7), dpi=300) # Increase figure size and resolution

# Bar chart with dynamic color
plt.bar(df_adjusters['Adjuster'], df_adjusters['Value (%)'], color='blue')

# Set axis labels and title
plt.xlabel('Adjusters', fontsize=14, fontweight='bold')
plt.ylabel('Value (%)', fontsize=14, fontweight='bold')
plt.title('Adjuster Values in Percentage', fontsize=16, fontweight='bold')

# Rotate x-axis labels for better readability
plt.xticks(rotation=45, ha='right', fontsize=12)

# Remove surrounding box (spines)
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.gca().spines['left'].set_visible(False)
plt.gca().spines['bottom'].set_visible(False)


# Display the chart in the sidebar
st.sidebar.pyplot(plt)

st.sidebar.write("### Input Model Price Data")

# Create number inputs in the sidebar for each price
flange_steel_manufacturing_price = st.sidebar.number_input(
    "Flange Steel Manufacturing Price", 
    min_value=0.0, 
    value=3200.0,  # Default value
    step=10.0
)

shell_steel_manufacturing_price = st.sidebar.number_input(
    "Shell Steel Manufacturing Price", 
    min_value=0.0, 
    value=870.0,  # Default value
    step=10.0
)

initial_steel_price = st.sidebar.number_input(
    "Steel Price", 
    min_value=0.0, 
    value=645.0,  # Default value
    step=10.0
)

initial_castiron_price = st.sidebar.number_input(
    "Cast Iron Price", 
    min_value=0.0, 
    value=424.0,  # Default value
    step=10.0
)

initial_resin_price = st.sidebar.number_input(
    "Resin Price", 
    min_value=0.0, 
    value=2371.0,  # Default value
    step=10.0
)

initial_HotRolledCoils_price = st.sidebar.number_input(
    "Hot Rolled Coils Price", 
    min_value=0.0, 
    value=843.0,  # Default value
    step=10.0
)

initial_bunker_price = st.sidebar.number_input(
    "Bunker Price", 
    min_value=0.0, 
    value=650.0,  # Default value
    step=10.0
)

# Create an instance of ModelPriceInputs with the updated values
model_price_data = ModelPriceInputs(
    flange_steel_manufacturing_price,
    shell_steel_manufacturing_price,
    initial_steel_price,
    initial_castiron_price,
    initial_resin_price,
    initial_HotRolledCoils_price,
    initial_bunker_price
)

# Create sidebar inputs for the technical data
st.sidebar.write("### Input Model Technical Data")

# Create number inputs in the sidebar for each technical parameter
initial_Weight_flange_mass_per_WTG = st.sidebar.number_input(
    "Weight Flange Mass per WTG", 
    min_value=0.0, 
    value=59.3,  # Default value
    step=0.1
)

initial_Weight_shell_mass_per_WTG = st.sidebar.number_input(
    "Weight Shell Mass per WTG", 
    min_value=0.0, 
    value=616.5,  # Default value
    step=0.1
)

initial_CastIron_Weight = st.sidebar.number_input(
    "Cast Iron Weight", 
    min_value=0.0, 
    value=268.8,  # Default value
    step=0.1
)

initial_Resin_Weight = st.sidebar.number_input(
    "Resin Weight", 
    min_value=0.0, 
    value=41.6,  # Default value
    step=0.1
)

initial_HotRolledCoils_Weight = st.sidebar.number_input(
    "Hot Rolled Coils Weight", 
    min_value=0.0, 
    value=122.6,  # Default value
    step=0.1
)

initial_bunker_Weight = st.sidebar.number_input(
    "Bunker Weight", 
    min_value=0.0, 
    value=2988.0,  # Default value
    step=10.0
)

weighted_CPI_Price = st.sidebar.number_input(
    "Weighted CPI Price", 
    min_value=0.0, 
    value=0.7,  # Default value
    step=0.01
)

# Create an instance of ModelTechnicalInputs with the updated values
model_technical_data = ModelTechnicalInputs(
    initial_Weight_flange_mass_per_WTG,
    initial_Weight_shell_mass_per_WTG,
    initial_CastIron_Weight,
    initial_Resin_Weight,
    initial_HotRolledCoils_Weight,
    initial_bunker_Weight,
    weighted_CPI_Price
)

st.sidebar.title("Model Macro Inputs")

# Add input fields for the user to enter the CPI values
st.sidebar.write("### Input Model Macro Data")

# Use number input for CPI values
initial_cpi_eur = st.sidebar.number_input(
    "CPI EUR (%)", 
    min_value=0.0, 
    max_value=1000.0,  # You can adjust this range as needed
    value=126.31,  # Default value from your model
    step=0.01
)

initial_cpi_us = st.sidebar.number_input(
    "CPI US (%)", 
    min_value=0.0, 
    max_value=1000.0,  # You can adjust this range as needed
    value=303.363,  # Default value from your model
    step=0.01
)

# Create an instance of ModelMacroInputs with the user inputs
model_macro_data = ModelMacroInputs(initial_cpi_eur, initial_cpi_us)



st.header(f"WTG Indexation")

total_offer_price = convert_price_to_currency(model_price_offer_data, model_exchange_data, target_currency)
total_offer_price_per_turbine = total_offer_price / No_of_Turbine
total_offer_price_per_MW = total_offer_price_per_turbine / turbine_mw

total_steel_adjustment = calculate_total_steel_adjustment(model_technical_data,model_price_data,model_adjuster_data,model_exchange_data,target_currency)
st.write(f"Total Steel Adjustment is {total_steel_adjustment:,.2f}")
total_bunker_adjustment = calculate_total_bunker_adjustment(model_technical_data,model_price_data,model_adjuster_data,model_exchange_data,target_currency)
st.write(f"Total Steel Adjustment is {total_bunker_adjustment:,.2f}")
total_material_adjustment = calculate_total_material_adjustment(model_technical_data, model_price_data,model_adjuster_data,model_exchange_data,target_currency)
st.write(f"Total Steel Adjustment is {total_material_adjustment:,.2f}")
total_cpi_adjustment = calculate_total_cpi_adjustment(model_technical_data, model_price_offer_data, model_adjuster_data,model_macro_data,model_exchange_data,target_currency)
st.write(f"Total Steel Adjustment is {total_cpi_adjustment:,.2f}")
total_value_adjustment = total_cpi_adjustment + total_bunker_adjustment +  (total_material_adjustment + total_steel_adjustment ) * No_of_Turbine
st.write(f"Total Steel Adjustment is {total_value_adjustment:,.2f}")

total_price_offer_after_adjustmet = total_value_adjustment + total_offer_price
total_price_offer_after_adjustmet_per_turbine = total_price_offer_after_adjustmet / No_of_Turbine
total_price_offer_after_adjustmet_per_MW = total_price_offer_after_adjustmet_per_turbine / turbine_mw

# Display the total offer price with the target currency
# Create two columns for the layout
col1, col2 = st.columns(2)

# Column 1: Total Offer Price
with col1:
    # Title and box for total offer price
    st.write(f"##### Total Offer Price in {target_currency}:")
    st.markdown(
        f"""
        <div class="box">
            <h2>{target_currency} {total_offer_price:,.2f}</h2>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Title and box for total offer price per turbine
    st.write(f"##### Total Offer Price in {target_currency} per turbine:")
    st.markdown(
        f"""
        <div class="box">
            <h2>{target_currency} {total_offer_price_per_turbine:,.2f}</h2>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Title and box for total offer price per MW
    st.write(f"##### Total Offer Price in {target_currency} per MW:")
    st.markdown(
        f"""
        <div class="box">
            <h2>{target_currency} {total_offer_price_per_MW:,.2f}</h2>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Column 2: Price After Adjustment
with col2:
    # Title and box for adjusted offer price
    st.write(f"##### Adjusted Offer Price in {target_currency}:")
    st.markdown(
        f"""
        <div class="box">
            <h2>{target_currency} {total_price_offer_after_adjustmet:,.2f}</h2>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Title and box for adjusted price per turbine
    st.write(f"##### Adjusted Price in {target_currency} per turbine:")
    st.markdown(
        f"""
        <div class="box">
            <h2>{target_currency} {total_price_offer_after_adjustmet_per_turbine:,.2f}</h2>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Title and box for adjusted price per MW
    st.write(f"##### Adjusted Price in {target_currency} per MW:")
    st.markdown(
        f"""
        <div class="box">
            <h2>{target_currency} {total_price_offer_after_adjustmet_per_MW:,.2f}</h2>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Waterfall indexation 
st.write(f"##### Indexation waterfall in {target_currency}")
# Create a waterfall chart
fig = go.Figure(go.Waterfall(
    name="Price",
    orientation="v",
    measure=["absolute", "relative", "relative", "relative", "relative", "total"],
    x=["Base Offer Price", "Steel Adjustment", "Bunker Adjustment", "Material Adjustment", "CPI Adjustment", "Total Offer Price After Adjustment"],
    textposition="outside",
    y=[
        total_offer_price_per_turbine,
        total_steel_adjustment,
        total_bunker_adjustment,
        total_material_adjustment,
        total_cpi_adjustment,
        total_price_offer_after_adjustmet_per_turbine
    ],
    connector={"line": {"color": "rgb(63, 63, 63)"}},
))

# Update layout for the waterfall chart
fig.update_layout(
    title="Waterfall Chart of Offer Price Per Turbine Adjustments",
    showlegend=False
)

# Display the waterfall chart in Streamlit
st.plotly_chart(fig)
