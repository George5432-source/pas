import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def generate_charts(df, rf_pred=None, gb_pred=None, feature_importances=None):
    import io
    import base64
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

    charts = {}

    # Crime time series
    fig1, ax1 = plt.subplots(figsize=(14, 5))
    df['crime_count'].resample('D').sum().plot(ax=ax1)
    ax1.set_title("Crime Count Time Series (Daily)")
    ax1.set_xlabel("Date")
    ax1.set_ylabel("Count")
    ax1.grid(True)
    canvas = FigureCanvas(fig1)
    img1 = io.BytesIO()
    canvas.print_png(img1)
    charts['crime_timeseries'] = base64.b64encode(img1.getvalue()).decode()

    # Feature importances
    if feature_importances is not None:
        fig2, ax2 = plt.subplots(figsize=(12, 6))
        top = feature_importances.sort_values(ascending=False).head(10)
        sns.barplot(x=top.values, y=top.index, ax=ax2, palette="viridis")
        ax2.set_title("Top Features")
        ax2.set_xlabel("Importance")
        ax2.set_ylabel("Feature")
        ax2.grid(True, axis='x')
        canvas = FigureCanvas(fig2)
        img2 = io.BytesIO()
        canvas.print_png(img2)
        charts['feature_importances'] = base64.b64encode(img2.getvalue()).decode()

    # Predictions vs actual
    if rf_pred is not None and gb_pred is not None:
        fig3, ax3 = plt.subplots(figsize=(15, 6))
        agg = df[['is_violent_crime']].copy()
        agg['rf_pred'] = rf_pred
        agg['gb_pred'] = gb_pred
        agg = agg.resample('h').sum()
        ax3.plot(agg.index, agg['is_violent_crime'], label='Actual', color='blue')
        ax3.plot(agg.index, agg['rf_pred'], label='RF Prediction', color='green', alpha=0.7)
        ax3.plot(agg.index, agg['gb_pred'], label='GB Prediction', color='red', alpha=0.7)
        ax3.set_title("Predictions vs Actual (Violent Crimes)")
        ax3.set_xlabel("Date")
        ax3.set_ylabel("Count")
        ax3.legend()
        ax3.grid(True)
        canvas = FigureCanvas(fig3)
        img3 = io.BytesIO()
        canvas.print_png(img3)
        charts['predictions_vs_actual'] = base64.b64encode(img3.getvalue()).decode()

    return charts
