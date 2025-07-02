def send_wait_list_html_email(name: str) -> str:
    """
    Generates the HTML content for the wait list email.

    Args:
        name (str): The name of the recipient.

    Returns:
        str: The HTML content for the wait list email.
    """
    return f"""
    <html>
        <head>
            <title>Wait List Confirmation</title>
        </head>
        <body>
            <h1>Thank you for your interest, {name}!</h1>
            <p>We have received your request to join our wait list.</p>
            <p>We will notify you as soon as a spot becomes available.</p>
            <p>If you have any questions, feel free to contact us at <a href="mailto:info@gregthe.ai"></p>
        </body>
    </html>
"""