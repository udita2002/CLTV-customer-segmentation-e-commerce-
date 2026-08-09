# CLTV-customer-segmentation-e-commerce-
Segments e-commerce customers into High/Medium/Low value tiers so a business can prioritize retention spend and marketing on the customers who actually drive revenue.
Problem

Not all customers are worth the same to a business. Without a value score, marketing teams treat a one-time buyer the same as a loyal repeat customer. This project ranks and segments customers so stakeholders can act on it.

Dataset

8,878 customer records from e-commerce transaction history (order value, order frequency, purchase recency).

Approach
Cleaned and analyzed the raw transaction data with Pandas
Computed CLTV (Customer Lifetime Value) as: avg. order value × purchase frequency × 3-year lifespan
Computed Frequency-Monetary (FM) scores using quantile-based binning (pd.qcut) to rank customers relative to each other rather than on raw thresholds
Segmented customers into High / Medium / Low value tiers using combined CLTV + FM_Score thresholds
Visualized the segmentation across 4 charts for stakeholder reporting
Results
Tier	Customers	Share
High-value	1,262	14.2%
Medium-value	2,471	27.8%
Low-value	5,145	58.0%
Tech Stack

Python · Pandas · Matplotlib · (dashboard workflow adaptable to Power BI / Tableau)

How to Run

Written and run in Spyder. To reproduce:

Download or clone this repo
Open the project folder in Spyder (File → Open Project)
Install dependencies: pip install -r requirements.txt (run in Spyder's IPython console, or in a terminal)
Open cltv_segmentation.py and run it (green ▶ Run button, or F5) — it will regenerate the 4 charts in outputs/
Project Structure
├── data/                    # raw + cleaned transaction data
├── cleaning.py               # data cleaning + preprocessing
├── cltv.py                   # CLTV + FM score calculation
├── cltv_segmentation.py      # tiering logic + chart generation — main script to run
├── outputs/                  # the 4 stakeholder charts
├── requirements.txt
└── README.md
Future Improvements
Turn the static charts into a live Power BI / Tableau dashboard
Add a churn-risk flag alongside the value tier
Author

Udita Gayen — LinkedIn · uditagayen2002@gmail.com
