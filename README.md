# VSourceCode

Code by using VS code

請確認虛擬環境位於根目錄位置運行

路徑已更改為相對路徑

只需將.csv , .db 丟進datasets資料夾即可

各資料夾說明:
BlackScholesModel:

 BlackScholeQuantlib.py     用Quantlib 計算Black Scholes得到的結果
 
 BlackScholebyContract.py   用Black Scholes formula計算得到的結果

CRRmodel:

 crr_binomial_tree.py       用CRR binomial tree 計算得到的結果


HestomModel:

 hestom_formula.ipynb        By using hestom formula 計算結果
 
 hestom_formula.py           
 
 heston_analytical.ipynb     By using analytical hestom (半封閉解) 計算結果
 
 heston_quantlib.py          By using quantlib hestom 計算結果


SABR_model:

 SABRFormula.py              By using SABR formula計算波動率並用Black scholes 計算結果
 
 SABRQuantlib.py             By using SABR quantlib計算波動率並用Black scholes 計算結果
 
 
OptionGetPip:

 包含yfinace option 爬蟲   stock 爬蟲  讀取csv等


SqliteGUI:

GUI_target_db_output.py

GUI_target_db_xlxs.py     For 古嚴寺_分表.db 和 古嚴寺_總表.db 進行搜尋並可存成xlxs   須將兩張表放在同資料夾中

SQL_GUI_query.py          For Query any .db By using SQL


 
