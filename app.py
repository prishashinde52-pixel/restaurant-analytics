
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Restaurant Analytics Lab",
    page_icon="🍽️",
    layout="wide"
)

st.title("🍽️ Restaurant Analytics Lab")
st.caption(
    "Interactive restaurant analytics prototype. "
    "All sample records are fictional."
)


# --------------------------------------------------
# 1. GENERATE SAMPLE DATA FOR FIVE RESTAURANTS
# --------------------------------------------------

@st.cache_data
def generate_data():
    rng = np.random.default_rng(42)

    restaurants = {
        "R01": {
            "name": "Goregaon Kitchen",
            "cuisine": "North Indian",
            "factor": 1.10
        },
        "R02": {
            "name": "Coastal Table",
            "cuisine": "South Indian",
            "factor": 0.90
        },
        "R03": {
            "name": "Urban Tandoor",
            "cuisine": "North Indian",
            "factor": 1.20
        },
        "R04": {
            "name": "The Pasta Room",
            "cuisine": "Italian",
            "factor": 0.95
        },
        "R05": {
            "name": "Spice Route",
            "cuisine": "Multi-cuisine",
            "factor": 1.00
        }
    }

    menus = {
        "North Indian": [
            ("Paneer Tikka", 280),
            ("Butter Chicken", 340),
            ("Dal Makhani", 240),
            ("Jeera Rice", 160)
        ],
        "South Indian": [
            ("Masala Dosa", 180),
            ("Idli Plate", 100),
            ("Filter Coffee", 70),
            ("Meals Thali", 260)
        ],
        "Italian": [
            ("Margherita Pizza", 320),
            ("Penne Alfredo", 350),
            ("Garlic Bread", 150),
            ("Cold Coffee", 140)
        ],
        "Multi-cuisine": [
            ("Veg Biryani", 250),
            ("Hakka Noodles", 220),
            ("Paneer Wrap", 190),
            ("Brownie", 130)
        ]
    }

    dates = pd.date_range(
        end=pd.Timestamp.today().normalize()
        - pd.Timedelta(days=1),
        periods=84,
        freq="D"
    )

    daily_records = []
    item_records = []

    for rid, info in restaurants.items():
        menu = menus[info["cuisine"]]

        for day_number, date in enumerate(dates):

            # Simulate higher demand on weekends
            weekend_factor = (
                1.30 if date.dayofweek >= 5 else 1.0
            )

            # Small gradual trend over time
            trend_factor = 1 + 0.0015 * day_number

            order_count = max(
                5,
                int(
                    rng.normal(48, 7)
                    * info["factor"]
                    * weekend_factor
                )
            )

            daily_revenue = 0

            for item_name, price in menu:

                average_demand = (
                    order_count
                    / len(menu)
                    * weekend_factor
                    * trend_factor
                )

                quantity = int(
                    rng.poisson(average_demand)
                )

                quantity = max(0, quantity)

                item_revenue = quantity * price
                daily_revenue += item_revenue

                if quantity > 0:
                    item_records.append({
                        "date": date,
                        "restaurant_id": rid,
                        "restaurant_name": info["name"],
                        "cuisine": info["cuisine"],
                        "item_name": item_name,
                        "quantity_sold": quantity,
                        "unit_price": price,
                        "item_revenue": item_revenue
                    })

            discount = int(
                rng.uniform(0, 0.04) * daily_revenue
            )

            daily_records.append({
                "date": date,
                "restaurant_id": rid,
                "restaurant_name": info["name"],
                "cuisine": info["cuisine"],
                "total_revenue": max(
                    0, daily_revenue - discount
                ),
                "order_count": order_count,
                "discount_total": discount
            })

    daily = pd.DataFrame(daily_records)
    items = pd.DataFrame(item_records)

    return daily, items


daily, items = generate_data()


# --------------------------------------------------
# 2. RESTAURANT FILTER
# --------------------------------------------------

st.sidebar.header("Restaurant filters")

restaurant_options = [
    "All restaurants"
] + sorted(daily["restaurant_name"].unique().tolist())

selected_restaurant = st.sidebar.selectbox(
    "Choose a restaurant",
    restaurant_options
)

if selected_restaurant == "All restaurants":
    sales = daily.copy()
    menu_sales = items.copy()
else:
    sales = daily[
        daily["restaurant_name"] == selected_restaurant
    ].copy()

    menu_sales = items[
        items["restaurant_name"] == selected_restaurant
    ].copy()

st.sidebar.info(
    "Demo mode: these are generated sample records, "
    "not actual restaurant data."
)


# --------------------------------------------------
# 3. KEY PERFORMANCE INDICATORS
# --------------------------------------------------

total_revenue = sales["total_revenue"].sum()
total_orders = sales["order_count"].sum()

average_order_value = (
    total_revenue / total_orders
    if total_orders > 0 else 0
)

if not menu_sales.empty:
    item_totals = (
        menu_sales.groupby("item_name")["quantity_sold"]
        .sum()
        .sort_values(ascending=False)
    )

    best_seller = item_totals.index[0]
else:
    best_seller = "N/A"

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Revenue",
    f"₹{total_revenue:,.0f}"
)

col2.metric(
    "Total Orders",
    f"{total_orders:,}"
)

col3.metric(
    "Revenue per Order",
    f"₹{average_order_value:,.0f}"
)

col4.metric(
    "Most-Sold Item",
    best_seller
)

st.caption(
    "Revenue per order is an approximate metric based on "
    "the generated records."
)


# --------------------------------------------------
# 4. DASHBOARD TABS
# --------------------------------------------------

sales_tab, menu_tab, forecast_tab, data_tab = st.tabs([
    "📈 Sales Analytics",
    "🍛 Menu Insights",
    "🔮 Revenue Forecast",
    "🗂️ Data Explorer"
])


# --------------------------------------------------
# 5. SALES ANALYTICS
# --------------------------------------------------

with sales_tab:

    st.subheader("Daily Revenue Trend")

    revenue_by_date = (
        sales.groupby("date", as_index=False)
        ["total_revenue"].sum()
    )

    fig = px.line(
        revenue_by_date,
        x="date",
        y="total_revenue",
        markers=True,
        title="Daily Revenue",
        labels={
            "date": "Date",
            "total_revenue": "Revenue (₹)"
        }
    )

    st.plotly_chart(fig, use_container_width=True)

    left, right = st.columns(2)

    with left:
        st.subheader("Weekday vs Weekend")

        day_comparison = sales.copy()

        day_comparison["day_type"] = np.where(
            day_comparison["date"].dt.dayofweek >= 5,
            "Weekend",
            "Weekday"
        )

        day_comparison = (
            day_comparison.groupby("day_type", as_index=False)
            ["total_revenue"].mean()
        )

        fig = px.bar(
            day_comparison,
            x="day_type",
            y="total_revenue",
            labels={
                "day_type": "Day Type",
                "total_revenue": "Average Daily Revenue (₹)"
            }
        )

        st.plotly_chart(fig, use_container_width=True)

    with right:
        st.subheader("Restaurant Comparison")

        if selected_restaurant == "All restaurants":

            comparison = (
                sales.groupby("restaurant_name", as_index=False)
                ["total_revenue"].sum()
                .sort_values("total_revenue", ascending=False)
            )

            fig = px.bar(
                comparison,
                x="restaurant_name",
                y="total_revenue",
                labels={
                    "restaurant_name": "Restaurant",
                    "total_revenue": "Revenue (₹)"
                }
            )

            st.plotly_chart(fig, use_container_width=True)

        else:
            st.write("Most recent sales records")

            st.dataframe(
                sales.sort_values(
                    "date", ascending=False
                ).head(10),
                use_container_width=True,
                hide_index=True
            )


# --------------------------------------------------
# 6. MENU ITEM ANALYTICS
# --------------------------------------------------

with menu_tab:

    st.subheader("Which Dishes Sell the Most?")

    if not menu_sales.empty:

        menu_summary = (
            menu_sales.groupby("item_name", as_index=False)
            .agg(
                quantity_sold=("quantity_sold", "sum"),
                item_revenue=("item_revenue", "sum")
            )
            .sort_values("quantity_sold", ascending=False)
        )

        fig = px.bar(
            menu_summary,
            x="item_name",
            y="quantity_sold",
            title="Total Units Sold by Menu Item",
            labels={
                "item_name": "Menu Item",
                "quantity_sold": "Units Sold"
            }
        )

        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Menu Performance Table")

        st.dataframe(
            menu_summary,
            use_container_width=True,
            hide_index=True
        )

    else:
        st.warning("No item-level data is available.")


# --------------------------------------------------
# 7. SIMPLE SEVEN-DAY REVENUE FORECAST
# --------------------------------------------------

with forecast_tab:

    st.subheader("Forecast the Next Seven Days")

    st.write(
        "This baseline predicts revenue using the average "
        "revenue for each weekday over the latest 28 days. "
        "It is a starting point, not an advanced AI model."
    )

    historical = (
        sales.groupby("date", as_index=False)
        ["total_revenue"].sum()
        .sort_values("date")
    )

    if len(historical) >= 28:

        recent = historical.tail(28).copy()

        recent["weekday"] = (
            recent["date"].dt.dayofweek
        )

        weekday_averages = (
            recent.groupby("weekday")["total_revenue"].mean()
        )

        last_date = historical["date"].max()

        future_dates = pd.date_range(
            start=last_date + pd.Timedelta(days=1),
            periods=7,
            freq="D"
        )

        forecast = pd.DataFrame({
            "date": future_dates
        })

        forecast["predicted_revenue"] = (
            forecast["date"].dt.dayofweek
            .map(weekday_averages)
        )

        forecast["predicted_revenue"] = (
            forecast["predicted_revenue"]
            .fillna(recent["total_revenue"].mean())
            .round(0)
        )

        history_plot = historical.tail(28).copy()

        history_plot = history_plot.rename(
            columns={"total_revenue": "revenue"}
        )

        history_plot["type"] = "Historical"

        forecast_plot = forecast.rename(
            columns={"predicted_revenue": "revenue"}
        )

        forecast_plot["type"] = "Baseline Forecast"

        plot_data = pd.concat([
            history_plot[["date", "revenue", "type"]],
            forecast_plot[["date", "revenue", "type"]]
        ], ignore_index=True)

        fig = px.line(
            plot_data,
            x="date",
            y="revenue",
            color="type",
            markers=True,
            title="Historical vs Predicted Revenue",
            labels={
                "date": "Date",
                "revenue": "Revenue (₹)",
                "type": "Series"
            }
        )

        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Forecast Results")

        st.dataframe(
            forecast,
            use_container_width=True,
            hide_index=True
        )

        st.download_button(
            "Download forecast CSV",
            forecast.to_csv(index=False).encode("utf-8"),
            file_name="revenue_forecast.csv",
            mime="text/csv"
        )

    else:
        st.warning(
            "At least 28 days of historical data is required."
        )


# --------------------------------------------------
# 8. VIEW AND DOWNLOAD SAMPLE DATA
# --------------------------------------------------

with data_tab:

    st.subheader("Daily Sales Dataset")

    st.dataframe(
        sales.head(50),
        use_container_width=True,
        hide_index=True
    )

    st.download_button(
        "Download daily_sales.csv",
        sales.to_csv(index=False).encode("utf-8"),
        file_name="daily_sales.csv",
        mime="text/csv"
    )

    st.subheader("Item-Level Sales Dataset")

    st.dataframe(
        menu_sales.head(50),
        use_container_width=True,
        hide_index=True
    )

    st.download_button(
        "Download item_sales.csv",
        menu_sales.to_csv(index=False).encode("utf-8"),
        file_name="item_sales.csv",
        mime="text/csv"
    )


# --------------------------------------------------
# 9. FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "Restaurant Analytics Lab | Educational prototype. "
    "Sample data and forecasts are fictional and should "
    "not be used for business decisions."
)
