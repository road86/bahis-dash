from dash import html, dcc

Form = html.Div([
    dcc.Graph(id="Map"),
        dcc.Slider(
            min=1,
            max=3,
            step=1,
            marks={
                1: "Division",
                2: "District",
                3: "Upazila",
            },
            value=3,
            id="geoSlider",
        )
    ])