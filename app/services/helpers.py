def transform_data_to_response(symbol,payload, df): 
        res_dict = {
            'symbol': symbol,
            'volume': payload.volume,
            'change': payload.change,
            'indicators': {}      
        }
        print(payload.indicators)
        for ind in payload.indicators:
            # print(ind)
            res_dict['indicators'][ind] = float(df[ind][-1])
            
        # print(res_dict)
        return res_dict