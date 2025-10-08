from app.services.indicators_manager import indicators_manager


def transform_data_to_response(pairs_data, indicators, df):
    is_uptrend = indicators_manager.define_uptrend_by_lows(df=df)
    res_dict = {
        'symbol': pairs_data['quote'],
        'volume': pairs_data['volume'],
        'change': pairs_data['change'],
        'trend': {'uptrend': is_uptrend},
        'indicators': {'numerical': [], 'binary': []}
    }
    # print(payload.indicators)
    for ind in indicators:
        if ind in ['rsi', 'dema']:
            res_dict['indicators']['numerical'].append(
                {'name': ind, 'value': float(df[ind].iloc[-1])})
        else:
            if float(df[ind].iloc[-1]) > 0:
                res_dict['indicators']['binary'].append(
                {'name': ind, 'value': float(df[ind].iloc[-1])})
            
    # print(res_dict)
    return res_dict
