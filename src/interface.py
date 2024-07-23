import dearpygui.dearpygui as dpg
import requests

from config import *
dpg.create_context()

def get_exchange_rate(from_currency, to_currency):
    url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{from_currency}"
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200 and "conversion_rates" in data:
        return data["conversion_rates"].get(to_currency)
    else:
        return None

def update_output(sender, app_data, user_data):
    amount_from = float(dpg.get_value("amount_from"))
    cur_from = dpg.get_value("cur_from")
    cur_to = dpg.get_value("cur_to")

    conversion_rate = get_exchange_rate(cur_from, cur_to)
    if conversion_rate:
        converted_amount = amount_from * conversion_rate
        dpg.set_value("output_text", f"{amount_from} {cur_from} = {converted_amount:.2f} {cur_to}")
    else:
        dpg.set_value("output_text", "Conversion rate not available.")

def menu():
    with dpg.window(tag="Primary Window"):
        dpg.add_text("From")
        dpg.add_combo(tag="cur_from", items=("USD", "EUR", "JPY", "GBP", "AUD", "CAD", "CHF", "CNH", "HKD", "NZD"))
        dpg.add_input_text(tag="amount_from")
        dpg.add_text("To")
        dpg.add_combo(tag="cur_to", items=("USD", "EUR", "JPY", "GBP", "AUD", "CAD", "CHF", "CNH", "HKD", "NZD"))
        dpg.add_button(label="Convert", callback=update_output)
        dpg.add_text("", tag="output_text")
        dpg.add_text("----------------------------")
        dpg.add_text("Exchange Rates updated daily")

    dpg.create_viewport(title='CurrenC', width=400, height=280)

    dpg.set_viewport_small_icon("../img/icon.ico")
    dpg.set_viewport_large_icon("../img/icon.ico")

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.set_primary_window("Primary Window", True)
    dpg.start_dearpygui()
    dpg.destroy_context()