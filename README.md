# Child-Tax-Credit-App
*The Tax Benefits Of Parenthood Interactive Dashboard*

Project GitHub Repo: https://github.com/grantseiter/Child-Tax-Credit-App

Deployed Application: https://compute.studio/AEIEconomics/CTC-App/viz/

### Note:
This repository contains a Dash application that allows users to investigate various reforms to the child tax credit in the context of all tax benefits currently afforded to filers with children. Users can select a baseline policy — current law, President Joe Biden’s American Rescue Plan, recent legislation adopted by the House Committee on Ways and Means, or Sen. Mitt Romney’s (R-UT) proposed Family Security Act — and a reform policy to analyze. In addition to the three proposals already mentioned, users can specify their own child tax credit reform by selecting the "Custom CTC Reform" option and adjusting four CTC parameters — refundability, the maximum credit value, the dollar bonus for children under six, and the threshold for which the credit begins phasing out.

This application accompanies:

“[The Tax Benefits of Parenthood: A History and Analysis of Current Proposals](https://www.aei.org/research-products/report/the-tax-benefits-of-parenthood-a-history-and-analysis-of-current-proposals/),” Alex Brill, Kyle Pomerleau, and Grant M. Seiter, AEI Report, American Enterprise Institute (February 23, 2021).

Data for this project are generated using the open-source [Tax-Calculator](https://github.com/PSLmodels/Tax-Calculator) project. The code that modifies the underlying models to produce these estimates can be found [here](https://github.com/grantseiter/Tax-Benefits-Of-Parenthood). The code that powers this data visualization can be found [here](https://github.com/grantseiter/Child-Tax-Credit-App).

To run locally:
```
git clone https://github.com/grantseiter/Child-Tax-Credit-App
cd Child-Tax-Credit-App
conda env create
conda activate widget-dev
python app.py
```          
### Languages
*Python*

### Authors
* **Grant M. Seiter** - *American Enterprise Institute (AEI)*, Washington, D.C.
 
Disclaimer: The American Enterprise Institute for Public Policy Research (AEI) is a nonpartisan, nonprofit, 501(c)(3) educational organization and does not take institutional positions on any issues. The views expressed here are those of the author(s).
