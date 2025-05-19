def show_settings(**kwargs):
    for k, v in kwargs.items():
        print(f"{k}: {v}")
show_settings(debug=True, port=8080)
