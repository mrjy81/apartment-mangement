def format_float(value):
    value = round(int(value))
    # Convert the value to a float and format it
    formatted_value = f"{value:,.2f}"  # Format with commas and two decimal places

    # Remove leading zero if present
    formatted_value = formatted_value.lstrip('0')

    # If the formatted value is a decimal point (e.g., ".12"), ensure it shows correctly
    if formatted_value.startswith('.'):
        formatted_value = '0' + formatted_value  # Add leading zero back for proper representation

    index_comma = formatted_value.index('.')
    return formatted_value[:index_comma]
