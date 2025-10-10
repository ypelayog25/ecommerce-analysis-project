try:
    import src.visualization.save_figures as viz
    viz.main()
except Exception as e:
    print("No figures generated (maybe not enough data):", e)
