from starlette.responses import HTMLResponse


async def index():
    html_content = """
    <html>
        <head>
            <title>INDEX HTML </title>
        </head>
        <body>
            <h1>FastAPI server work!</h1>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)
