from win11toast import notify as toast

icon = {"src": "https://unsplash.it/64?image=669", "placement": "appLogoOverride"}

toast("Hello", "Hello from Python", icon=icon, app_id="MSEdge")
