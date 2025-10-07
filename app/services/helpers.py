from app.services.indicators_manager import indicators_manager

def transform_data_to_response(pairs_data,indicators, df): 
        is_uptrend = indicators_manager.define_uptrend_by_lows(df=df)
        res_dict = {
            'symbol': pairs_data['quote'],
            'volume': pairs_data['volume'],
            'change': pairs_data['change'],
            'trend': {'uptrend': is_uptrend},
            'indicators': {}      
        }
        # print(payload.indicators)
        for ind in indicators:
            # print(ind)
            res_dict['indicators'][ind] = float(df[ind].iloc[-1])
            
        # print(res_dict)
        return res_dict