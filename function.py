from model import ModelPriceOfferInputs, ModelExchangeInputs, ModelMacroInputs


def convert_price_to_currency(price_offer: ModelPriceOfferInputs, exchange_data: ModelExchangeInputs, target_currency):
    if target_currency == "USD":
        # Convert EUR and KRW components to USD
        eur_to_usd = price_offer.initial_price_in_EUR * exchange_data.initial_eur_to_usd
        krw_to_usd = price_offer.initial_price_in_KRW / exchange_data.initial_usd_to_krw
        total_in_usd = price_offer.initial_price_in_USD + eur_to_usd + krw_to_usd
        return total_in_usd
    
    elif target_currency == "EUR":
        # Convert USD and KRW components to EUR
        usd_to_eur = price_offer.initial_price_in_USD / exchange_data.initial_eur_to_usd
        krw_to_eur = price_offer.initial_price_in_KRW / exchange_data.initial_eur_to_krw
        total_in_eur = price_offer.initial_price_in_EUR + usd_to_eur + krw_to_eur
        return total_in_eur
    
    else:
        raise ValueError(f"Unsupported target currency: {target_currency}")


def adjustment(initial_value, adjusted_percentage):
    return initial_value * (1 + adjusted_percentage)


def calculate_total_steel_adjustment(technical_data, price_data, adjustment_data, exchange_data, target_currency: str):
    # Step 1: Calculate adjusted weights
    primary_flange_weight_after_adjustment = adjustment(
        technical_data.initial_Weight_flange_mass_per_WTG, adjustment_data.weight_flange_adjuster
    )
    primary_shell_weight_after_adjustment = adjustment(
        technical_data.initial_Weight_shell_mass_per_WTG, adjustment_data.weight_shell_adjuster
    )
    
    # Step 2: Calculate total flange and shell weight adjustments
    total_flange_weight_value_after_adjustment = (
        (primary_flange_weight_after_adjustment - technical_data.initial_Weight_flange_mass_per_WTG)
        * (price_data.flange_steel_manufacturing_price + price_data.initial_steel_price)
    )

    total_shell_weight_value_after_adjustment = (
        (primary_shell_weight_after_adjustment - technical_data.initial_Weight_shell_mass_per_WTG)
        * (price_data.shell_steel_manufacturing_price + price_data.initial_steel_price)
    )

    # Step 3: Adjusted steel price
    primary_steel_price_after_adjustment = adjustment(price_data.initial_steel_price, adjustment_data.steel_price_adjuster)

    # Step 4: Calculate total flange and shell weight after adjustment
    total_flange_and_shell_weight_after_adjustment = (
        primary_flange_weight_after_adjustment + primary_shell_weight_after_adjustment
    )

    # Step 5: Calculate total steel price value after adjustment
    total_steel_price_value_after_adjustment = (
        total_flange_and_shell_weight_after_adjustment 
        * (primary_steel_price_after_adjustment - price_data.initial_steel_price)
    )

    # Step 6: Sum up all adjustments
    total_steel_adjustment_in_usd = (
        total_flange_weight_value_after_adjustment 
        + total_shell_weight_value_after_adjustment 
        + total_steel_price_value_after_adjustment
    )

    # Step 7: Convert to target currency if necessary
    if target_currency == "USD":
        return total_steel_adjustment_in_usd
    elif target_currency == "EUR":
        total_steel_adjustment_in_eur = total_steel_adjustment_in_usd / exchange_data.initial_eur_to_usd
        return total_steel_adjustment_in_eur
    else:
        raise ValueError(f"Unsupported target currency: {target_currency}")   
    
def calculate_total_bunker_adjustment(technical_data, price_data, adjustment_data, exchange_data, target_currency: str):
    # Step 1: Adjust bunker weight and price
    bunker_weight_after_adjustment = adjustment(
        technical_data.initial_bunker_Weight, adjustment_data.weight_bunker_adjuster
    )
    bunker_price_after_adjustment = adjustment(
        price_data.initial_bunker_price, adjustment_data.bunker_price_adjuster
    )
    
    # Step 2: Calculate total bunker value adjustment in USD
    total_bunker_value_after_adjustment_in_usd = (
        bunker_price_after_adjustment * (bunker_weight_after_adjustment + technical_data.initial_bunker_Weight)
        - technical_data.initial_bunker_Weight * (price_data.initial_bunker_price + bunker_price_after_adjustment)
    )

    # Step 3: Convert to target currency if necessary
    if target_currency == "USD":
        return total_bunker_value_after_adjustment_in_usd
    elif target_currency == "EUR":
        total_bunker_value_after_adjustment_in_eur = (
            total_bunker_value_after_adjustment_in_usd / exchange_data.initial_eur_to_usd
        )
        return total_bunker_value_after_adjustment_in_eur
    else:
        raise ValueError(f"Unsupported target currency: {target_currency}")



def calculate_total_material_adjustment(technical_data, price_data, adjustment_data , exchange_data, target_currency: str):
    # Step 1: Calculate adjusted prices
    castIron_price_after_adjustment = adjustment(price_data.initial_castiron_price, adjustment_data.castiron_price_adjuster)
    resin_price_after_adjustment = adjustment(price_data.initial_resin_price, adjustment_data.resin_price_adjuster)
    HotRolledCoils_price_after_adjustment = adjustment(price_data.initial_HotRolledCoils_price, adjustment_data.HotRolledCoils_price_adjuster)
    
    # Step 2: Calculate total value adjustments
    castIron_total_value_after_adjustment = (
        technical_data.initial_CastIron_Weight 
        * (castIron_price_after_adjustment - price_data.initial_castiron_price)
    )

    resin_total_value_after_adjustment = (
        technical_data.initial_Resin_Weight 
        * (resin_price_after_adjustment - price_data.initial_resin_price)
    )

    HotRolledCoils_total_value_after_adjustment_in_eur = (
        technical_data.initial_HotRolledCoils_Weight 
        * (HotRolledCoils_price_after_adjustment - price_data.initial_HotRolledCoils_price)
    )

    # Step 3: Convert EUR component to target currency if necessary
    if target_currency == "USD":
        HotRolledCoils_total_value_after_adjustment_in_usd = (
            HotRolledCoils_total_value_after_adjustment_in_eur * exchange_data.initial_eur_to_usd
        )
        total_material_adjustment = (
            castIron_total_value_after_adjustment 
            + resin_total_value_after_adjustment 
            + HotRolledCoils_total_value_after_adjustment_in_usd
        )
    elif target_currency == "EUR":
        castIron_total_value_after_adjustment_in_eur = (
            castIron_total_value_after_adjustment / exchange_data.initial_eur_to_usd
        )
        resin_total_value_after_adjustment_in_eur = (
            resin_total_value_after_adjustment / exchange_data.initial_eur_to_usd
        )
        total_material_adjustment = (
            castIron_total_value_after_adjustment_in_eur 
            + resin_total_value_after_adjustment_in_eur 
            + HotRolledCoils_total_value_after_adjustment_in_eur
        )
    else:
        raise ValueError(f"Unsupported target currency: {target_currency}")

    return total_material_adjustment


def calculate_total_cpi_adjustment(technical_data,
                                   price_offer: ModelPriceOfferInputs, 
                                   adjustment_data, 
                                   macro_data: ModelMacroInputs, 
                                   exchange_data,  
                                   target_currency= str):
    # Step 1: Calculate adjusted CPI for EUR and USD
    cpi_eur_after_adjustment = adjustment(macro_data.initial_cpi_eur, adjustment_data.cpi_eur_adjuster)
    cpi_us_after_adjustment = adjustment(macro_data.initial_cpi_us, adjustment_data.cpi_us_adjuster)

    # Step 2: Calculate total value CPI adjustments for EUR and USD components
    total_value_cpi_eur_adjustment = (
        price_offer.initial_price_in_EUR 
        * technical_data.weighted_CPI_Price 
        * (cpi_eur_after_adjustment / macro_data.initial_cpi_eur - 1)
    )

    total_value_cpi_us_adjustment = (
        price_offer.initial_price_in_USD 
        * technical_data.weighted_CPI_Price 
        * (cpi_us_after_adjustment / macro_data.initial_cpi_us - 1)
    )

    # Step 3: Convert EUR adjustment to target currency if necessary
    if target_currency == "USD":
        total_value_cpi_eur_adjustment_in_usd = total_value_cpi_eur_adjustment * exchange_data.initial_eur_to_usd
        total_cpi_adjustment = total_value_cpi_eur_adjustment_in_usd + total_value_cpi_us_adjustment
    elif target_currency == "EUR":
        total_value_cpi_us_adjustment_in_eur = total_value_cpi_us_adjustment / exchange_data.initial_eur_to_usd
        total_cpi_adjustment = total_value_cpi_eur_adjustment + total_value_cpi_us_adjustment_in_eur
    else:
        raise ValueError(f"Unsupported target currency: {target_currency}")

    return total_cpi_adjustment
