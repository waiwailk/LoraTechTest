select a.ticker, a.month, a.trading_day, a.total_return_index
	from (
			select ticker, date_part('month', trading_day) as month, trading_day, total_return_index, 
			row_number() over (partition by ticker, date_part('year', trading_day), date_part('month', trading_day) order by trading_day desc) as rownum
			from data_price
			where trading_day between '2019-12-31' AND '2020-12-31'
		 ) a 
	ORDER BY trading_day ASC
	--order by ticker,MONTH,trading_day ASC
